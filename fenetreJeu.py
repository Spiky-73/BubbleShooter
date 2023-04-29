import copy
import time # pour le chronomètre
import tkinter as tk
import random # pour générer les couleurs des billes
import csv # pour charger les niveaux
import math

from balle import Balle
import gestionnaireDeTheme
from utilitaire import Vector2, Vector2Int

class FenetresJeu:
    
    def __init__(self, niveau: str):
        """ Initialise la fenêtre de jeu avec le niveau choisi. """

        self.niveau = niveau
        if self.niveau == 'aleatoire':
            self.niveau_aleatoire()

        self.rayon_billes = 10
        self.centre_bille = Vector2(self.rayon_billes, self.rayon_billes)

        self.racine = tk.Tk()        
        self.racine.title(f"Niveau {niveau}")
        self.racine.resizable(height = False, width = False)

        self.img_eclats = tk.PhotoImage(file="images/eclats.png").subsample(6)

        self.position_souris = Vector2(0,0)
        self.racine.bind("<Motion>", self._mouvement_souris)

        self._creer_widgets()

        self._init_niveau()

        self.balle: Balle = None
        self.creer_balle_canon()

        self.FPS = 60
        self.delta = 1/self.FPS # pour s'actualiser toutes les 1/60 sec
        self.update()


    def _creer_widgets(self):
        """Ajoute l'interface du jeu et ses données/statistiques : score, temps écoulé, nombre de billes éclatées..."""

        self.taille_canevas = Vector2Int(500, 700)
        self.canevas = tk.Canvas(self.racine, bg="light blue", height=self.taille_canevas.y, width=self.taille_canevas.x, bd=0, highlightthickness=0, background=gestionnaireDeTheme.fond)
        self.canevas.pack()
        self.canevas.bind('<Button-1>', self.envoi_balle)
        self.timer = tk.Label(self.racine, text = "\nTemps écoulé ", font = 'Helvetica 11 bold') # affichage des statistiques
        self.timer.pack(side=tk.RIGHT, fill='x')

        self.nbr_billes_eclatees = tk.Label(self.racine, text = "\nNombre de billes éclatées ", font = 'Helvetica 11 bold')
        self.nbr_billes_eclatees.pack(side=tk.RIGHT, fill='x')

        self.score = tk.Label(self.racine, text = "\nScore ", font = 'Helvetica 11 bold')
        self.score.pack(side=tk.RIGHT, fill='x')


        self.rayon_pointilles = 2
        self.pointilles_visibles = 0
        self.offset_pointilles = 0
        self.espacement_pointilles = 75
        self.pointilles: list[int] = [] # crée les pointillés a l'avance pour éviter de les recréer en permanace et augmenter les performances
        for _ in range(50):
            self.pointilles.append(self.canevas.create_oval(-self.rayon_pointilles, -self.rayon_pointilles, self.rayon_pointilles, self.rayon_pointilles, fill="", outline=""))
        self.pointilles.append(self.canevas.create_oval(*(self.centre_bille*-1), *(self.centre_bille), fill="", outline=""))


    def _init_niveau(self):
        """Lecture et chargement du niveau."""

        self.fichier = f"niveaux/{self.niveau}.csv"

        self.grande_ligne = 0
        self.voisins_gl = [
                    Vector2Int(-1,-1), Vector2Int(0,-1), # on place les billes dans une grille hexagonale
            Vector2Int(-1,0),  Vector2Int(0,0),  Vector2Int(1,0),
                    Vector2Int(-1,1),  Vector2Int(0,1)
        ]
        self.voisins_pl = [
                    Vector2Int(0,-1), Vector2Int(1,-1), 
            Vector2Int(-1,0),  Vector2Int(0,0),  Vector2Int(1,0),
                    Vector2Int(0,1),  Vector2Int(1,1)
        ]

        self.billes: list[list[int]] = []
        x = self.taille_canevas.x // (2*self.rayon_billes)
        self.hauteur = (2*self.rayon_billes)*math.cos(math.pi/6)
        self.taille_grille = (x, x-1, int(self.taille_canevas.y/self.hauteur))
        for y in range(self.taille_grille[2]):
            l = [-1 for _ in range(x - y%2)]
            self.billes.append(l)
        
        self.index_couleurs = []

        with open(self.fichier, encoding='utf-8') as csvfile: # lecture du fichier csv contenant le niveau choisi
            reader = csv.reader(csvfile,  delimiter=",")
            for j, ligne in enumerate(reader):
                if j == 0 and len(ligne)-self.taille_grille[0] == -1:
                    self.billes.pop()
                    self.billes.insert(0, self.billes[1].copy())
                    self.grande_ligne = 1
                for i, c in enumerate(ligne): 
                    if c != " ":
                        c = int(c)
                        if(not c in self.index_couleurs):
                            self.index_couleurs.append(c)
                        self.place_bille(Vector2Int(i,j), gestionnaireDeTheme.billes[c])

        self.vitesse_balle = 750 # pixels/s
        self.position_canon = Vector2(250,675) # là où on tire la balle, en bas au centre
    
    def place_bille(self, bille: Vector2Int, color: str):
        """Ajoute une bille sur le caneva."""

        y = max(0, min(bille.y, len(self.billes)-1))
        x = max(0, min(bille.x, len(self.billes[y])))
        position = self.coordonees_to_position(bille) # appel de coordonees_to_position pour la conversion
        self.billes[y][x] = self.canevas.create_oval(*(position-self.centre_bille), *(position+self.centre_bille), fill=color)
    

    def creer_balle_canon(self):
        """Crée la balle au niveau du canon à balles (en bas de la fenêtre) et choisi sa couleur aléatoirement."""
        couleur = gestionnaireDeTheme.billes[random.choice(self.index_couleurs)] # choix aléatoire parmi les couleurs proposées
        self.balle_canon = Balle(self.position_canon, self.rayon_billes, Vector2(0, -self.vitesse_balle), couleur, -1)
        id = self.canevas.create_oval(*self.balle_canon.coin_NW,*self.balle_canon.coin_SE, fill=self.balle_canon.couleur)
        self.balle_canon.id = id
    

    def _mouvement_souris(self, event: tk.Event):
        """Actualise la position de la souris."""
        self.position_souris.x = event.x
        self.position_souris.y = event.y


    def update(self):
        """
        Appelée plusieurs fois par seconde.
        Appelle toutes les fonctions liées au mouvement de la balle (timer) et du jeu.
        """

        temp_update = time.time() # pour le timer et le chrono
        self._prediction_trajectoire()
        self._update_balle()
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

        if(self.balle is not None): return # on ne fait rien si la balle est lancée
        delta: Vector2 = self.position_souris - self.position_canon
        angle = math.atan2(delta.y, delta.x)
        self.balle_canon.vitesse = Vector2(math.cos(angle), math.sin(angle)) * self.vitesse_balle
        balle = Balle(copy.copy(self.position_canon), self.balle_canon.rayon, copy.copy(self.balle_canon.vitesse), self.balle_canon.couleur, -1) # la balle simulant la balle lancée
        
        distance = self.offset_pointilles
        self.pointilles_visibles = 0
        dt = 1/(60*4)
        while (not self.collision_bille(balle)) & (not self.deplacer_balle(balle, dt)) and self.pointilles_visibles < len(self.pointilles)-1: # tant qu'on a pas rencontré de bille et donc que la balle est en mouvement
            distance += balle.vitesse.norme * dt
            if(distance >= self.espacement_pointilles): # affiche et bouge un pointillé a la place de la balle
                self.canevas.moveto(self.pointilles[self.pointilles_visibles], *balle.centre)
                self.canevas.itemconfigure(self.pointilles[self.pointilles_visibles], fill=balle.couleur)
                distance -= self.espacement_pointilles
                self.pointilles_visibles+=1

        # décale les pointillés avec le temps pour donner un effet annimé
        self.offset_pointilles = (self.offset_pointilles-balle.vitesse.norme * self.delta/2)%self.espacement_pointilles


        balle.vitesse *=-1
        while (self.collision_bille(balle) | self.deplacer_balle(balle, 1/1000)): # tant que on se placerais sur une case occupée ou en dehors de la grille
            pass

        for i in range(self.pointilles_visibles, len(self.pointilles)-1): # cache les pointillés inutilisés
            self.canevas.itemconfigure(self.pointilles[i], fill="")
        
        # affiche la balle simullée dans sa position finale
        self.canevas.moveto(self.pointilles[-1], * (self.coordonees_to_position(self.position_to_coordonees(balle.centre))-self.centre_bille))
        self.canevas.itemconfigure(self.pointilles[-1], outline=balle.couleur) # pointillés de la couleur de la balle qu'on lance
        

    def envoi_balle(self, event) : 
        """Envoie la balle dans la direction de la souris."""
        if(self.balle is not None): return

        # cache tout les pointillés
        for i in range(0, self.pointilles_visibles):
            self.canevas.itemconfigure(self.pointilles[i], fill="")
        self.canevas.itemconfigure(self.pointilles[-1], outline="")
        
        self.balle = self.balle_canon
        

    def _update_balle(self):
        """Contrôle le déplacement de la balle."""
        if(self.balle is None): return

        # bouge la balle et detecte les collisions
        place = self.deplacer_balle(self.balle, self.delta) or self.collision_bille(self.balle)
        self.canevas.moveto(self.balle.id, *self.balle.coin_NW)

        if(place): # si on touche quleque chose

            # recule la balle jusqu'à ce que elle se pose sur une case vide
            self.balle.vitesse *=-1
            while True:
                coords = self.position_to_coordonees(self.balle.centre)
                if(not(coords.y < 0 
                       or (0 <= coords.y and coords.y < len(self.billes) and 0 <= coords.x and coords.x < len(self.billes[coords.y])
                            and self.billes[coords.y][coords.x] != -1)
                )):
                    break
                self.deplacer_balle(self.balle, 1/1000)

            # place la balle
            col = self.balle.couleur
            bille = self.place_balle(self.balle)
            self.test_eclate_billes(bille, col)


    def test_eclate_billes(self, bille: Vector2Int, col: str):
        """Teste si la bille touchée appartient à un groupe d'au moins 2 billes de même couleur que la balle lancée."""

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
            balle.centre.x = balle.rayon - balle.coin_NW.x # North West
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
        # recupère la case de la balle et ses voisins
        coord = self.position_to_coordonees(balle.centre)
        voisins = self.voisins_gl if coord.y%2 == self.grande_ligne else self.voisins_pl

        for delta in voisins: # regarde si il y a une collision
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
        """ Renvoie les coordonnées des billes formant un groupe de couleur."""

        # initialise un BFS
        groupe = [bille]
        attente = [bille]
        color: str = self.canevas.itemcget(self.billes[bille.y][bille.x], "fill")

        while len(attente) != 0: # BFSD avec une condition
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

        # surpime la bille
        self.billes[bille.y][bille.x] = -1
        self.canevas.delete(id)

        # supression de l'image
        anim = self.canevas.create_image(pos.x,pos.y, image = self.img_eclats, anchor=tk.CENTER)
        self.racine.after(random.randint(100, 500), self._eclate_bille_fin, anim)


    def _eclate_bille_fin(self, anim_id: int):
        """Fin de l'animation."""
        self.canevas.delete(anim_id)


    def test_fin_de_partie(self) -> bool: 
        """Arrête le jeu (sortir de la fonction update) s'il n'y a plus de billes et affiche le score dans une messagebox."""

        pass


    def position_to_coordonees(self, position: Vector2) -> Vector2Int:
        """Convertit la position du centre d'une bille du canevas en coordonnées dans la grille de billes."""

        side = self.hauteur/(1+math.cos(math.pi/3))
        y, rem_y = divmod(position.y-self.rayon_billes+side/2, self.hauteur)

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
        """Convertit des coordonnées dans la grille de bille en position sur le canevas"""
        x = self.rayon_billes + coords.x*self.rayon_billes*2 + (self.rayon_billes * ((coords.y-self.grande_ligne)%2))
        y = self.rayon_billes + coords.y * self.hauteur
        return Vector2(x, y)
    
    
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
        