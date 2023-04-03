from balle import RAYON
import tkinter as tk
import balle
import utilitaire
from utilitaire import Vector2
import random
import csv
from datetime import datetime
import math # pour pouvoir utiliser math.inf

class FenetresJeu:
    
    def __init__(self, racine, niveau: str) -> None:
        """Initialise la fenetre de jeu avec le niveau choisi."""

        self.niveau=niveau
        
        if niveau=="facile":
            self.fichier='init_jeu_f.csv'
            
        if niveau=="moyen":
            self.fichier='init_jeu_m.csv'
        
        if niveau=="difficile":
            self.fichier='init_jeu_d.csv'

        self.racine = tk.Toplevel(racine)        
        self.racine.title("Jeu en cours")
        self.racine.config(width=300, height=300)
        self.racine.resizable(height = False, width = False)
        
        self.canevas_height=700
        self.canevas_width=500
        self.canevas = tk.Canvas(self.racine, bg="light blue", height=self.canevas_height, width=self.canevas_width)
        self.canevas.pack()
        
        self.init_jeu_dico={}
        self._init_niveau()
        
        self.souris = Vector2(0,0)
        self.racine.bind("<Motion>", self.movement_souris)

        self._creer_widgets()
    
        self.creer_balle_canon()
    
    def _init_niveau(self) -> None:
        """Lecture et chargement du niveau."""
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
            self.canevas.create_oval(x,y, x+RAYON, y+RAYON, fill=color)
            
            
    def _creer_widgets(self) -> None:
        """Ajoute l'interface du jeu et ses donnees/statistiques : score, temps écoule, nombre de billes eclatees..."""

        self.timer = tk.Label(self.racine, text = "\nTemps écoulé :", font = 'Helvetica 11 bold')
        self.timer.pack(side=tk.RIGHT, fill='x')
        
        compteur = math.inf # pour le chronometre 
        running = False

        self.nbr_billes_eclatees = tk.Label(self.racine, text = "\nNombre de billes éclatées", font = 'Helvetica 11 bold')
        self.nbr_billes_eclatees.pack(side=tk.RIGHT, fill='x')

        self.score = tk.Label(self.racine, text = "\nScore", font = 'Helvetica 11 bold')
        self.score.pack(side=tk.RIGHT, fill='x')

    #def calcul_score(self,event):
        #il faudrait faire un timer pour actualiser le score apres chaque lancer ? ou meme toutes les secondes ?
        #"""Calcule le score du joueur tel que score = nombre de billes eclatees / temps ecoule depuis le debut de la partie."""
        #nbr_billes_eclatees = _eclate_bille(self) + eclate_billes_adjacentes(self)
        #nbr_billes_eclatees / temps
    
    def creer_balle_canon(self):
        """crée la balle au niveau du canon à balles (en bas de la fenêtre) et choisi sa couleur aléatoirement """
        couleurs = ["red", "green", "blue", "yellow", "magenta", "cyan", "white", "purple"]
        couleur = couleurs[random.randint(0,1)]
        canon =balle.Balle(utilitaire.Vector2(250,675),utilitaire.Vector2(1,1), couleur)
        self.balle_canon = self.canevas.create_oval(canon.position.x,canon.position.y,canon.position.x+RAYON,canon.position.y+RAYON, fill= canon.couleur)
    

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

    def movement_souris(self, event: tk.Event) -> None:
        """Récupère la position de la souris."""
        self.souris.x = event.x
        self.souris.y = event.y

    def update(self) -> None:
        """
        Appelée plusieurs fois par seconde.
        Appellere toutes les fonctions liées au mouvement de la balle (timer) et du jeu.
        """

    def _update_trajectoire(self) -> None:
        """Simule la trajectoire de la balle et l'affiche pour guider le joueur."""
        point=balle.Balle(utilitaire.Vector2(250,675),utilitaire.Vector2(1,1),'white')
        dt_trajectoire=10
        self.deplacer_balle(point, dt_trajectoire)
        self.pointille = self.canevas.create_oval(point.position.x,point.position.y,point.position.x+5,point.position.y+5, fill=point.couleur)


    def envoi_balle(self, event) : 
        """Envoie la balle dans la direction de la souris"""
       

    def _update_balle(self) -> None:
        """Controlle le déplacement de la balle."""


    def deplacer_balle(self, balle: balle.Balle, dt: float) -> None:
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

    def collision_bille(self, balle: balle.Balle) -> int:
        """Renvoie l'id de la bille touchée ou None si la balle ne touche pas de bille."""

        if balle.position.x + RAYON or balle.position.y + RAYON == self.x_bille + RAYON or self.y_bille + RAYON : # teste s'il y a collision entre la balle et une bille déjà placée
           x_touche = self.x_bille
           y_touche = self.y_bille
           id = (x_touche,y_touche)
   
        else : # si on ne touche rien
           id = None
           
        return int(id) # renvoie les coordonnées de la bille touchée
           
    # ? changer la fonction pour qu'elle retourne tous les voisins de la même couleur et faire le test du nombre dans une autre fonction ou lors de la collision de la balle
    def recherche_voisins(self, balle: balle.Balle, nombre: int = 3) -> bool:
        """
        Renvoie `True` s'il y a plus de `nombre` billes adjacentes de la même couleur a `balle`.
        Stocke les coordonnées de la balle qui reste alors sur le caneva si ce n'est pas le cas.
        """
        for bille in self.billes:
            coords = self.canevas.coords(bille)
            position = Vector2(coords[0]+coords[RAYON], coords[1]+coords[RAYON])
            if(self.canevas.coords(bille)):
                pass
            

    def eclate_billes_adjacentes(self,  balle: balle.Balle) : 
        """Eclates toutes les billes adjacentes de la même couleur que la balle."""

    def _eclate_bille(self, bille: int):
        """Eclate une bille."""

    def test_fin_de_partie (self) -> bool: 
        """Arrête le jeu (sortir de la fonction update) si il n'y a plus de billes et affiche le score dans une messagebox."""
        if compter_billes == 0 :
