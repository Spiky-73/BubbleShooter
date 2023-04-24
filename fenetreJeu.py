import time # pour le chronomètre
import tkinter as tk
import random # pour générer les couleurs des billes
import csv # pour charger les niveaux
import math

from balle import Balle, RAYON
from utilitaire import Vector2, Vector2Int

class FenetresJeu:
    
    def __init__(self, niveau: str):
        """Initialise la fenêtre de jeu avec le niveau choisi."""

        self.niveau = niveau
        self.couleurs = ["red", "green", "blue", "yellow", "magenta", "cyan", "white", "purple"]

        self.racine = tk.Tk()        
        self.racine.title(f"Niveau {niveau}")
        self.racine.resizable(height = False, width = False)

        self.img_eclats = tk.PhotoImage(file="images/eclats.png").subsample(6)
        self.img_nuages = tk.PhotoImage(file="images/fond.png").zoom(2)

        self.position_souris = Vector2(0,0)
        self.racine.bind("<Motion>", self._mouvement_souris)

        self._creer_widgets()

        self._init_niveau()
    
        self.balle = None
        self.creer_balle_canon()

        self.delta = 1000//30 # floor division, pour s'actualiser toutes les 1000/30 msec
        self.update()


    def _creer_widgets(self):
        """Ajoute l'interface du jeu et ses données/statistiques : score, temps écoulé, nombre de billes éclatées..."""

        self.canevas = tk.Canvas(self.racine, bg="light blue", height=700, width=500)
        self.canevas.pack()

        self.canevas.create_image(0, -60, image = self.img_nuages, anchor=tk.NW)

        self.timer = tk.Label(self.racine, text = "\nTemps écoulé ", font = 'Helvetica 11 bold')
        self.timer.pack(side=tk.RIGHT, fill='x')
        
        compteur = math.inf # pour le chronomètre 
        running = False

        self.nbr_billes_eclatees = tk.Label(self.racine, text = "\nNombre de billes éclatées ", font = 'Helvetica 11 bold')
        self.nbr_billes_eclatees.pack(side=tk.RIGHT, fill='x')

        self.score = tk.Label(self.racine, text = "\nScore ", font = 'Helvetica 11 bold')
        self.score.pack(side=tk.RIGHT, fill='x')


    def _init_niveau(self):
        """Lecture et chargement du niveau."""

        self.fichier = f"niveaux/{self.niveau}.csv"

        self.billes: list[list[int]] = []
        self.voisins = [
            Vector2Int(-1,0), Vector2Int(1,0),
            Vector2Int(0,-1), Vector2Int(0,1)
        ]
        self.init_jeu_dico = {}
        with open(self.fichier, encoding='utf-8') as csvfile: # lecture du fichier csv contenant le niveau choisi
            reader = csv.reader(csvfile,  delimiter=",")
            self.dico_color = {}
            for j, ligne in enumerate(reader):
                for i, c in enumerate(ligne): 
                    if c!="0": # guillemets car chaîne de caractères
                        if c not in self.dico_color.keys() : 
                            x = random.randint(0, len(self.couleurs)-1) # -1 car le len est inclusif, pour ne pas avoir une erreur out of bound
                            self.dico_color[c] = self.couleurs[x]
                            self.couleurs.pop(x) # pour n'avoir que les couleurs du niveau
                        color = self.dico_color[c]
                        self.place_bille(Vector2Int(i,j), color)

        self.position_canon = Vector2(250,675) # là où on tire la balle, en bas au centre

    
    def place_bille(self, bille: Vector2Int, color: str):
        """Ajoute une bille sur le caneva."""
        position = self.coordonees_to_position(bille)
        while bille.y>=len(self.billes) #tant qu'on ne dépasse pas le cadre
            self.billes.append([])
        while bille.x>=len(self.billes[bille.y]):
            self.billes[bille.y].append(-1)
        self.billes[bille.y][bille.x] = self.canevas.create_oval(position.x-RAYON,position.y-RAYON, position.x+RAYON, position.y+RAYON, fill=color)
              

    #def calcul_score(self,event):
        #il faudrait faire un timer pour actualiser le score apres chaque lancer ? ou même toutes les secondes ? comment on calcule le score ?
        #"""Calcule le score du joueur tel que score = nombre de billes eclatees / temps ecoule depuis le debut de la partie."""
        #nbr_billes_eclatees = _eclate_bille(self) + eclate_billes_adjacentes(self)
        #nbr_billes_eclatees / temps
    

    def creer_balle_canon(self):
        """Crée la balle au niveau du canon à balles (en bas de la fenêtre) et choisi sa couleur aléatoirement."""
        couleur = random.choice(list(self.dico_color.values()))
        self.balle_canon = Balle(self.position_canon, Vector2(1,1), couleur, -1)
        id = self.canevas.create_oval(self.balle_canon.position.x,self.balle_canon.position.y,self.balle_canon.position.x+2*RAYON,self.balle_canon.position.y+2*RAYON, fill= self.balle_canon.couleur)
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
        self._prediction_trajectoire()
        self._update_balle()
        self._update_score()

        self.racine.after(self.delta, self.update)


    def _prediction_trajectoire(self):
        """Simule la trajectoire de la balle et l'affiche pour guider le joueur."""

        if(self.balle is not None): return # on ne fait rien si la balle est lancée et est en mouvement

        rayon = 2
        point = Balle(self.position_canon, Vector2(1,1), 'black', -1) # pointillés noirs qui simulent la trajectoire
        while self.collision_bille(point) == None: # tant qu'on a pas rencontré de bille et donc que la balle est en mouvement
            self.deplacer_balle(point, 15 * self.delta)
            self.pointille = self.canevas.create_oval(point.position.x-rayon, point.position.y-rayon, point.position.x+rayon, point.position.y+rayon, fill=point.couleur)


    def envoi_balle(self, event) : 
        """Envoie la balle dans la direction de la souris"""
       

    def _update_balle(self):
        """Contrôle le déplacement de la balle."""
        if(self.balle is None): return

        self.deplacer_balle(self.balle, self.delta)
        self.canevas.moveto(self.balle.id, self.balle.position.x+RAYON, self.balle.position.y+RAYON)

        bille = self.collision_bille(self.balle)
        if(bille is None) : return

        color: str = self.canevas.itemcget(self.billes[bille.y][bille.x], "fill")
        if(color != self.balle.couleur): # si la balle touche une bille qui n'est pas de la même couleur
            self.place_balle(self.balle) # alors rien n'explose et la balle se place à l'endroit de la collision, collée à la bille touchée. La balle devient une bille.
        else:
            groupe = self.get_groupe(bille)
            if(len(groupe) < 2): # si la chaine de billes de même couleur ainsi formée est < 2
                self.place_balle(self.balle) # la balle se place et devient une bille
            else:
                anim = self.canevas.create_image(self.balle.position.x,self.balle.position.y, image = self.img_eclats, anchor=tk.CENTER) # animation
                self.racine.after(1000+random.randint(-250, 250), self._eclate_bille_fin, anim)
                for b in groupe:
                    time.sleep(0.1)
                    self.eclate_bille(b) # on éclate car le chaîne ainsi formée comporte au minimum 3 billes de la même couleur

                self.canevas.delete(self.balle.id)
                self.balle = None
                self.creer_balle_canon()


    def _update_score(self):
        """Actualise le temps total de jeu et le score."""
        

    def deplacer_balle(self, balle: Balle, dt: float):
        """Déplace une balle sur dt secondes et prend en compte les collisions."""
        balle.position.x += balle.vitesse.x * dt
        balle.position.y += balle.vitesse.y * dt

        if balle.position.x < 0 : # si la bille sort de la fenetre
            balle.position.x = 0
            
            balle.vitesse.x = -balle.vitesse.x # elle rebondit contre le mur
        elif balle.position.x + RAYON > 500 : # position de la bille et position du bord
            balle.position.x = 500 - RAYON # bord - bille car la fenetre fait 500x700
            balle.vitesse.x = - balle.vitesse.x
        
        if balle.position.y < 0 : # on fait pour toutes les directions
            balle.position.y = 0
            balle.vitesse.y = - balle.vitesse.y  
        elif balle.position.y + RAYON > 700 : # bille - bord
            balle.position.y = 700 - RAYON # bord - bille
            balle.vitesse.y = - balle.vitesse.y  


    def collision_bille(self, balle: Balle):
        """Renvoie les coordonnées de la bille touchée ou None si la balle ne touche pas de bille."""
        coord = self.position_to_coordonees(balle.position)
        bille = None
        voisins = [
            Vector2Int(-1,-1), Vector2Int(0,-1), Vector2Int(1,-1), # les 8 voisins autour de la balle
            Vector2Int(-1,0),                    Vector2Int(1,0),
            Vector2Int(-1,1),  Vector2Int(0,1),  Vector2Int(1,1)
        ]
        i = 0
        while i < 9 and bille is None:
            n_pos = voisins[i]+coord
            if 0 <= n_pos.y and n_pos.y < len(self.billes) and 0 <= n_pos.x and n_pos.x < len(self.billes[n_pos.y]):
                id = self.billes[n_pos.y][n_pos.x]
                if(id != -1 and balle.position.distance(self.coordonees_to_position(n_pos)) <= 2*RAYON): # teste s'il y a contact
                    bille = n_pos
            i+=1
        
        return bille


    def place_balle(self, balle: Balle):
        """Place la balle dans la cellule la plus proche."""
        bille = self.position_to_coordonees(balle.position)
        self.place_bille(bille, balle.couleur)
        

    def get_groupe(self, bille: Vector2Int) -> list[Vector2Int]:
        """ Renvoie les coordonnées des billes formant un groupe de couleur."""
        
        groupe = [bille]
        attente = [bille]
        color: str = self.canevas.itemcget(self.billes[bille.y][bille.x], "fill")
        while len(attente) != 0:
            pos = attente.pop()
            for delta in self.voisins:
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
        self.racine.after(1000+random.randint(-250, 250), self._eclate_bille_fin, anim)

    def _eclate_bille_fin(self, anim_id: int):
        self.canevas.delete(anim_id)


    def test_fin_de_partie(self) -> bool: 
        """Arrête le jeu (sortir de la fonction update) s'il n'y a plus de billes et affiche le score dans une messagebox."""
        pass


    def position_to_coordonees(self, position: Vector2) -> Vector2Int:
        """Convertit la position du centre d'une bille du canevas en coordonnées dans la grille de bille."""
        position = (position - Vector2(RAYON, RAYON)) / (2*RAYON)
        return Vector2Int(round(position.x), round(position.y))

    def coordonees_to_position(self, coords: Vector2Int) -> Vector2:
        """Convertit des coordonnées dans la grille de bille en position sur le canevas"""
        coords = coords*2*RAYON
        coords += Vector2Int(RAYON, RAYON)
        return Vector2(coords.x, coords.y)
