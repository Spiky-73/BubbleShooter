import time # pour le chronomètre
import tkinter as tk
import random # pour générer les couleurs des billes
import csv # pour charger les niveaux
import math

from balle import Balle
from canon import Canon
from grilleHexagonale import GrilleHexagonale

from gestionnaireDeTheme import theme
from utilitaire import Vector2, Vector2Int
import gestionnaireDeNiveaux


class FenetresJeu:

    RAYON = 10
    
    def __init__(self, niveau: str):
        """ Initialise la fenêtre de jeu avec le niveau choisi ainsi que tous les paramètres nécessaire au fonctionnement du programme. """

        self.niveau = niveau
        if self.niveau == 'aleatoire':
            self.niveau_aleatoire()

        self.racine = tk.Tk()        
        self.racine.title(f"Niveau {niveau}")
        self.racine.resizable(height = False, width = False)

        self._creer_widgets()

        self._init_niveau()

        self.FPS = 60
        self.delta = 1/self.FPS
        self.update()


    def _creer_widgets(self):
        """Ajoute l'interface du jeu et ses données/statistiques : score, temps écoulé, nombre de billes éclatées..."""

        self.taille_canevas = Vector2Int(500, 700)
        self.canevas = tk.Canvas(self.racine, bg="light blue", height=self.taille_canevas.y, width=self.taille_canevas.x, bd=0, highlightthickness=0, background=theme.fond)
        self.canevas.pack()
        self.timer = tk.Label(self.racine, text = "\nTemps écoulé ", font = 'Helvetica 11 bold') # affichage des statistiques
        self.timer.pack(side=tk.RIGHT, fill='x')

        self.nbr_billes_eclatees = tk.Label(self.racine, text = "\nNombre de billes éclatées ", font = 'Helvetica 11 bold')
        self.nbr_billes_eclatees.pack(side=tk.RIGHT, fill='x')

        self.score = tk.Label(self.racine, text = "\nScore ", font = 'Helvetica 11 bold')
        self.score.pack(side=tk.RIGHT, fill='x')


    def _init_niveau(self):
        """Lecture et chargement du niveau."""

        self.fichier = f"niveaux/{self.niveau}.csv"

        self.grille, couleurs = gestionnaireDeNiveaux.charge_niveau(self.niveau, self.canevas, self.RAYON)

        self.balles: list[Balle] = []
        self.canon = Canon(self.canevas, Vector2(250,655), self.grille, self.RAYON, couleurs, self.balles)


    def update(self):
        """
        Appelée plusieurs fois par seconde.
        Appelle toutes les fonctions liées au mouvement de la balle (timer) et du jeu.
        """

        temp_update = time.time() # pour le timer et le chrono
        self.canon.update(self.delta)
        if(len(self.balles) == 1):
            self.balles[0].update(self.delta)
        else:
            self.canon.charge_balle()
        self._update_score()

        # fps en fonction du temps de la fonction
        temps = time.time()
        tps_update = temps-temp_update
        delai = int((self.delta-tps_update)*1000)
        if(delai <= 0):
            if(tps_update > 2*self.delta): # on fixe une valeur au delà de laquelle on considère qu'on a une trop faible valeur d'images par seconde
                print(f"LOW FPS ({int(1/tps_update)}/{self.FPS})")
            delai = 1
        self.racine.after(delai, self.update)


    def _prediction_trajectoire(self):
        """Simule la trajectoire de la balle et l'affiche pour guider le joueur."""

        if(self.balle is not None): return # on ne fait rien si la balle est lancée et est en mouvement
        delta = self.position_souris - self.position_canon
        angle = math.atan2(delta.y, delta.x)
        self.balle_canon.vitesse = Vector2(math.cos(angle), math.sin(angle)) * self.vitesse_balle
        point = Balle(copy.copy(self.position_canon), self.balle_canon.rayon, copy.copy(self.balle_canon.vitesse), self.balle_canon.couleur, -1) # pointillés noirs qui simulent la trajectoire

        interval = 30
        step=0 #pointillés bougent
        p = 0
        while (not self.collision_bille(point)) & (not self.deplacer_balle(point, 1/(60*4))) and p < len(self.pointilles)-1: # tant qu'on a pas rencontré de bille et donc que la balle est en mouvement
            if(step%interval == self.offset_pointilles):
                self.canevas.moveto(self.pointilles[p], *point.centre)
                self.canevas.itemconfigure(self.pointilles[p], fill=point.couleur)
                p+=1
            step+=1
        self.offset_pointilles = (self.offset_pointilles+2)%interval
        point.vitesse *=-1
        while (self.collision_bille(point) | self.deplacer_balle(point, 1/1000)): # tant qu'on a pas rencontré de bille et donc que la balle est en mouvement
            pass
        for i in range(p, len(self.pointilles)-1):
            self.canevas.itemconfigure(self.pointilles[i], fill="")
        
        self.canevas.moveto(self.pointilles[-1], *(self.coordonees_to_position(self.position_to_coordonees(point.centre))-self.centre_bille))
        self.canevas.itemconfigure(self.pointilles[-1], fill=point.couleur)
        

    def envoi_balle(self, event) : 
        """Envoie la balle dans la direction de la souris"""
        if(self.balle is not None): return
        self.balle=self.balle_canon
        

    def _update_balle(self):
        """Contrôle le déplacement de la balle."""
        if(self.balle is None): return
        place = self.deplacer_balle(self.balle, self.delta) or self.collision_bille(self.balle)
        self.canevas.moveto(self.balle.id, *self.balle.coin_NW)

        if(place): # si on touche le haut du canevas
            self.balle.vitesse *=-1
            while True:
                coords = self.position_to_coordonees(self.balle.centre)
                if(not(coords.y < 0 
                       or (0 <= coords.y and coords.y < len(self.billes) and 0 <= coords.x and coords.x < len(self.billes[coords.y])
                            and self.billes[coords.y][coords.x] != -1)
                )):
                    break
                self.deplacer_balle(self.balle, 1/1000)
            col = self.balle.couleur
            bille = self.place_balle(self.balle)
            self.test_eclate_billes(bille, col)


    def test_eclate_billes(self, bille: Vector2Int, col: str):
        """regarde si la bille touchée appartient à un groupe de même couleur d’au moins deux billes, dans ce cas, appelle eclate_bille """
        groupe = self.get_groupe(bille)
        if(len(groupe) >=3): # si la chaine de billes de même couleur ainsi formée est < 2
            for b in groupe:
                self.eclate_bille(b) # on éclate car le chaîne ainsi formée comporte au minimum 3 billes de la même couleur


    def _update_score(self):
        """Actualise le temps total de jeu et le score."""

        

    def deplacer_balle(self, balle: Balle, dt: float) -> bool:
        """
        Déplace une balle sur dt secondes et prend en compte les collisions.
        Renvoie vrai si la balle touche le mur du haut
        """
        balle.centre += balle.vitesse * dt

        if balle.coin_NW.x < 0 : # si la bille sort de la fenetre
            balle.centre.x = balle.rayon - balle.coin_NW.x
            balle.vitesse.x *= -1 # elle rebondit contre le mur

        elif balle.coin_SE.x > self.taille_canevas.x : # position de la bille et position du bord
            balle.centre.x = self.taille_canevas.x-balle.rayon - (balle.coin_SE.x-self.taille_canevas.x)
            balle.vitesse.x *= -1
    
        if balle.coin_NW.y < 0 : # on fait pour toutes les directions
            return True
        elif balle.coin_SE.y > self.taille_canevas.y : # bille - bord
            balle.centre.y =  self.taille_canevas.y-balle.rayon - (balle.coin_SE.y-self.taille_canevas.y)
            balle.vitesse.y *= -1

        return False


    def collision_bille(self, balle: Balle) -> bool:
        """Renvoie les coordonnées de la bille touchée ou None si la balle ne touche pas de bille."""
        coord = self.position_to_coordonees(balle.centre)
        voisins = self.voisins_gl if coord.y%2 == self.grande_ligne else self.voisins_pl
        for delta in voisins:
            n_pos = delta + coord
            if 0 <= n_pos.y and n_pos.y < len(self.billes) and 0 <= n_pos.x and n_pos.x < len(self.billes[n_pos.y]):
                id = self.billes[n_pos.y][n_pos.x]
                if(id != -1 and balle.centre.distance(self.coordonees_to_position(n_pos)) <= balle.rayon + self.rayon_billes): # teste s'il y a contact
                    return True
        return False

    def place_balle(self, balle: Balle) -> Vector2Int:
        """Place la balle dans la cellule la plus proche."""
        coord = self.position_to_coordonees(balle.centre)
        self.canevas.delete(balle.id)
        self.place_bille(coord, balle.couleur)
        self.balle = None
        self.creer_balle_canon()
        return coord
        

    def get_groupe(self, bille: Vector2Int) -> list[Vector2Int]:
        """ Renvoie les coordonnées de la bille formant un groupe de couleur."""
        groupe = [bille]
        attente = [bille]
        color: str = self.canevas.itemcget(self.billes[bille.y][bille.x], "fill")
        while len(attente) != 0:
            pos = attente.pop()
            voisins = self.voisins_gl if pos.y%2 == self.grande_ligne else self.voisins_pl
            for delta in voisins:
                n_pos = pos + delta
                if 0 <= n_pos.y and n_pos.y < len(self.billes) and 0 <= n_pos.x and n_pos.x < len(self.billes[n_pos.y]) and not n_pos in groupe:
                    id = self.billes[n_pos.y][n_pos.x]
                    if(id != -1 and self.canevas.itemcget(id, "fill") == color):
                        attente.append(n_pos)
                        groupe.append(n_pos)
            
        return groupe
        

    def eclate_bille(self, bille: Vector2Int):
        """Eclate une bille."""
        id = self.billes[bille.y][bille.x]
        pos = self.coordonees_to_position(bille)
        self.billes[bille.y][bille.x] = -1
        self.canevas.delete(id)
        anim = self.canevas.create_image(pos.x,pos.y, image = self.img_eclats, anchor=tk.CENTER)
        self.racine.after(random.randint(100, 500), self._eclate_bille_fin, anim)

    def _eclate_bille_fin(self, anim_id: int):
        self.canevas.delete(anim_id)


    def test_fin_de_partie(self) -> bool: 
        """Arrête le jeu (sortir de la fonction update) s'il n'y a plus de billes et affiche le score dans une messagebox."""
        pass

    #    def _update_score(self):
#        """Actualise le temps total de jeu et le score. Calcule le score du joueur."""
#
#        # à appeler à chaque lancer
#        score = 0
#        if eclate == True : # rajouter un booleen dans la fonction test_eclate_groupe : on incrémente le score à partir du moment où le lancer éclate des billes
#            groupe = self.get_groupe(bille) + self.eclate_billes_detaches() # le nombre de billes éclatées = celles du groupe éclaté + celles qui étaient en dessous et qui tombent aussi car non connectées
#            if groupe == 3 : # nombre minimal pour éclater
#                score += 3
#            elif groupe > 3 and < 10 :
#                score += groupe * 1.2 # bonus : plus on éclate un grand groupe, plus on obtient de points : 1 point par bille éclatée + un coefficient bonus car grande chaîne formée
#            elif groupe >= 10 and < 15 :
#                score += groupe * 1.4
#            elif groupe >= 15 and < 20 :
#                score += groupe * 1.6
#            else :
#                score = score + groupe*2
#        
#        if fin_de_partie == True : # booléen dans test_fin_de_partie
#            if chrono > 180 : # à modifier quand on aura fait la fonction du chrono, si le joueur met plus de 3 minutes pour terminer le niveau (chrono affiché en fin de partie)
#                score = score # pas de bonus de rapidité
#            elif chrono > 120 and chrono <= 180 : # s'il met entre 2 et 3 minutes
#                score = score * 1.1 # léger bonus de rapidité
#            elif chrono >= 40 and chrono <= 120 :
#                score = score * 1.2
#            else : 
#                score = score * 1.5
#            
#        score = score * 10 # pour éviter d'avoir des tout petits scores
#        return score
#
#        # est-ce qu'on affiche le score à chaque lancer en bas ?
    def position_to_coordonees_square(self, position: Vector2) -> Vector2Int:
        """Convertit la position du centre d'une bille du canevas en coordonnées dans la grille de billes."""
        coords = (position - Vector2(self.rayon_billes, self.rayon_billes)) / (2*self.rayon_billes)
        return Vector2Int(round(coords.x), round(coords.y))

    def coordonees_to_position_square(self, coords: Vector2Int) -> Vector2:
        """Convertit des coordonnées dans la grille de bille en position sur le canevas"""
        position = coords*2*self.rayon_billes
        position += Vector2Int(self.rayon_billes, self.rayon_billes)
        return Vector2(position.x, position.y)
    
    def position_to_coordonees(self, position: Vector2) -> Vector2Int:
        """Convertit la position du centre d'une bille du canevas en coordonnées dans la grille de billes."""
        hauteur = (2*self.rayon_billes)*math.cos(math.pi/6)
        side = hauteur/(1+math.cos(math.pi/3))
        y, rem_y = divmod(position.y-self.rayon_billes+side/2, hauteur)

        correction = 0
        if(rem_y > side and y != -1): correction = (rem_y-side) * math.tan(math.pi/3)
        position_x = position.x - correction
        type_ligne = (y-self.grande_ligne)%2

        x, rem_x = divmod(position_x - (self.rayon_billes * type_ligne), self.rayon_billes*2)
        if(correction != 0):
            if(rem_x > (self.rayon_billes-correction)*2):
                y += 1
                x += type_ligne
                type_ligne = 1-type_ligne
        
        return Vector2Int(int(x), int(y))

    def coordonees_to_position(self, coords: Vector2Int) -> Vector2:
        """Convertit des coordonnées dans la grille de billes en position sur le canevas"""
        hauteur = (2*self.rayon_billes)*math.cos(math.pi/6)
        return Vector2(self.rayon_billes + coords.x*self.rayon_billes*2 + (self.rayon_billes if coords.y%2 != self.grande_ligne else 0), self.rayon_billes + coords.y * hauteur)
    
    def niveau_aleatoire(self, nb_color):
        """Génère une grille de jeu aléatoirement en respectant un nombre de couleurs de billes."""

        liste_ligne=[]
        import csv
        with open(self.fichier, encoding='utf-8') as fichiercsv: # lecture du fichier csv
            writer=csv.writer(fichiercsv)
            for i in range (19):
                for j in range(25):
                    nb=random.randint(0, len(self.index_couleurs))
                    liste_ligne.append(nb)
                writer.writerow(liste_ligne)
    