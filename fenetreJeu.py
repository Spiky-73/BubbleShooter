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
        """ Initialise la fenêtre de jeu avec le niveau choisi. """

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


    def _update_score(self):
        """Actualise le temps total de jeu et le score. Calcule le score du joueur."""
        score = 0
        #if 


    def test_fin_de_partie(self) -> bool: 
        """Arrête le jeu (sortir de la fonction update) s'il n'y a plus de billes et affiche le score dans une messagebox."""
        pass


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
        