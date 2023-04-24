import time
import tkinter as tk
import random
import csv
import math

from balle import Balle, RAYON
from utilitaire import Vector2, Vector2Int


class FenetresJeu:
    
    def __init__(self, niveau: str):
        """Initialise la fenetre de jeu avec le niveau choisi."""

        self.niveau = niveau

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


        self.delta = 1000//30
        self.update()
      
    def _creer_widgets(self):
        """Ajoute l'interface du jeu et ses donnees/statistiques : score, temps écoule, nombre de billes eclatees..."""

        self.canevas = tk.Canvas(self.racine, bg="light blue", height=700, width=500)
        self.canevas.pack()

        self.canevas.create_image(0, -60, image = self.img_nuages, anchor=tk.NW)


        self.timer = tk.Label(self.racine, text = "\nTemps écoulé :", font = 'Helvetica 11 bold')
        self.timer.pack(side=tk.RIGHT, fill='x')
        
        compteur = math.inf # pour le chronometre 
        running = False

        self.nbr_billes_eclatees = tk.Label(self.racine, text = "\nNombre de billes éclatées", font = 'Helvetica 11 bold')
        self.nbr_billes_eclatees.pack(side=tk.RIGHT, fill='x')

        self.score = tk.Label(self.racine, text = "\nScore", font = 'Helvetica 11 bold')
        self.score.pack(side=tk.RIGHT, fill='x')

    def _init_niveau(self):
        """Lecture et chargement du niveau."""

        self.fichier=f"niveaux/{self.niveau}.csv"

        self.billes: list[list[int]] = []
        self.voisins = [
            Vector2Int(-1,0), Vector2Int(1,0),
            Vector2Int(0,-1), Vector2Int(0,1)
        ]
        self.init_jeu_dico={}
        with open(self.fichier, encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile,  delimiter=",")
            dicotemp = {}
            for ligne in reader:
                print(ligne)
                ident, x, y, color=ligne[0], ligne[1], ligne[2], ligne[3]
                if ident not in dicotemp: # si la clef n'existe pas encore
                    dicotemp[ident] = [float(x),float(y), str(color)] # on cree la liste des infos associées
        self.init_jeu_dico = dicotemp

        for x, y, color in self.init_jeu_dico.values():
            self.canevas.create_oval(x,y, x+2*RAYON, y+2*RAYON, fill=color)

    
    # TODO verification / ajout de listes en pour eviter les "out of bounds"
    def place_bille(self, bille: Vector2Int, color: str):
        """Ajoute une bille sur le canvevas"""
        position = self.coordonees_to_position(bille)
        self.billes[bille.y][bille.x] = self.canevas.create_oval(position.x,position.y, position.x+2*RAYON, position.y+2*RAYON, fill=color)
              

    #def calcul_score(self,event):
        #il faudrait faire un timer pour actualiser le score apres chaque lancer ? ou meme toutes les secondes ?
        #"""Calcule le score du joueur tel que score = nombre de billes eclatees / temps ecoule depuis le debut de la partie."""
        #nbr_billes_eclatees = _eclate_bille(self) + eclate_billes_adjacentes(self)
        #nbr_billes_eclatees / temps
    

    def creer_balle_canon(self):
        """crée la balle au niveau du canon à balles (en bas de la fenêtre) et choisi sa couleur aléatoirement """
        couleurs = ["red", "green", "blue", "yellow", "magenta", "cyan", "white", "purple"]
        couleur = couleurs[random.randint(0,1)] # BUG len(couleurs)
        canon = Balle(Vector2(250,675), Vector2(1,1), couleur, -1)
        self.balle_canon = self.canevas.create_oval(canon.position.x,canon.position.y,canon.position.x+2*RAYON,canon.position.y+2*RAYON, fill= canon.couleur)
    

    def counter_label(self, count) : # je vois pas trop comment faire le chronomètre
        def compter(self) :
            if running == True :
                global compteur
    
    def start_chrono(self, label) :
        global running
        running = True
        self.counter_label(label)
    
    def stop_chrono(self) : 
        global running
        running = False


    def _mouvement_souris(self, event: tk.Event):
        """Actualise la position de la souris."""
        self.position_souris.x = event.x
        self.position_souris.y = event.y

    def update(self):
        """
        Appelée plusieurs fois par seconde.
        Appellere toutes les fonctions liées au mouvement de la balle (timer) et du jeu.
        """
        self._prediction_trajectoire()
        self._update_balle()
        self._update_score()

        self.racine.after(self.delta, self.update)


    def _prediction_trajectoire(self):
        """Simule la trajectoire de la balle et l'affiche pour guider le joueur."""
        if(self.balle is not None): return
        point=Balle(Vector2(250,675),Vector2(1,1),'white', -1)
        dt_trajectoire=10
        self.deplacer_balle(point, dt_trajectoire)
        self.pointille = self.canevas.create_oval(point.position.x,point.position.y,point.position.x+5,point.position.y+5, fill=point.couleur)


    def envoi_balle(self, event) : 
        """Envoie la balle dans la direction de la souris"""
       

    def _update_balle(self):
        """Controlle le déplacement de la balle."""
        if(self.balle is None): return

        self.deplacer_balle(self.balle, self.delta)
        self.canevas.moveto(self.balle.id, self.balle.position.x+RAYON, self.balle.position.y+RAYON)

        bille = self.collision_bille(self.balle)
        if(bille is None) : return

        color: str = self.canevas.itemcget(self.billes[bille.y][bille.x], "fill")
        if(color != self.balle.couleur):
            self.place_balle(self.balle)
        else:
            groupe = self.get_groupe(bille)
            if(len(groupe) < 2):
                self.place_balle(self.balle)
            else:
                annim = self.canevas.create_image(self.balle.position.x,self.balle.position.y, image = self.img_eclats, anchor=tk.CENTER)
                self.racine.after(1000+random.randint(-250, 250), self._eclate_bille_fin, annim)
                for b in groupe:
                    time.sleep(0.1)
                    self.eclate_bille(b)

                self.canevas.delete(self.balle.id)
                self.balle = None
                self.creer_balle_canon()


    def _update_score(self):
        """Actualise le temps total de jeu et le score."""
        


    def deplacer_balle(self, balle: Balle, dt: float):
        """Deplace une balle sur dt secondes et prends en compte les collisions."""
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

        if balle.position.x + RAYON or balle.position.y + RAYON == self.x_bille + RAYON or self.y_bille + RAYON : # teste s'il y a collision entre la balle et une bille déjà placée
           x_touche = self.x_bille
           y_touche = self.y_bille
           id = (x_touche,y_touche)
   
        else : # si on ne touche rien
           id = None
           
        return id # renvoie l'id' de la bille touchée

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
        annim = self.canevas.create_image(pos.x,pos.y, image = self.img_eclats, anchor=tk.CENTER)
        self.racine.after(1000+random.randint(-250, 250), self._eclate_bille_fin, annim)

    def _eclate_bille_fin(self, annim_id: int):
        self.canevas.delete(annim_id)


    def test_fin_de_partie(self) -> bool: 
        """Arrête le jeu (sortir de la fonction update) si il n'y a plus de billes et affiche le score dans une messagebox."""
        pass


    def position_to_coordonees(self, position: Vector2) -> Vector2Int:
        """Convertit la position du centre d'une bille du canevas en coordonnées dans la grille de bille."""
        position = (position - Vector2(RAYON, RAYON)) / (2*RAYON)
        return Vector2Int(round(position.x), round(position.y))

    def coordonees_to_position(self, coords: Vector2Int) -> Vector2:
        """Convertit des coordonnées dans la grille de bille en position sur le canevas"""
        coords = coords*2*RAYON + Vector2Int(RAYON, RAYON)
        return Vector2(coords.x, coords.y)
