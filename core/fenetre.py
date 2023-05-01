import time # pour le chronomètre
import tkinter as tk
import math

from .balle import Balle
from .canon import Canon
from .grilleHexagonale import GrilleHexagonale
from .script import Script


from .gestionnaireDeTheme import theme
from utilitaire import Vector2, Vector2Int


class Fenetre:

    RAYON = 10
    DIMENSIONS = Vector2Int(25, 42)
    HAUTEUR = 2*RAYON*math.cos(math.pi/6)

    FPS = 60
    DELTA = 1/FPS
    
    def __init__(self):
        """ Initialise la fenêtre de jeu avec le niveau choisi. """

        self.racine = tk.Tk()        
        self.racine.title(f"Bubbleshooter")
        self.racine.resizable(height = False, width = False)

        self.canevas = tk.Canvas(self.racine, width=self.DIMENSIONS.x*2*self.RAYON, height=self.DIMENSIONS.y*self.HAUTEUR, bd=0, highlightthickness=0, bg=theme.fond)
        self.canevas.pack()
        
        self.grille = GrilleHexagonale(self.canevas, self.DIMENSIONS, self.RAYON)
        self.balles: list[Balle] = []
        self.canon = Canon(self.canevas, Vector2(250,655), self.grille, self.RAYON, [0], self.balles)

        self.scipt: Script = None

    def start(self, script: Script, *args):
        self.set_scipt(script, *args)
        self.update()
        self.racine.mainloop()


    def set_scipt(self, script: Script, *args):
        if(self.scipt != None):
            self.scipt.clear()
        self.scipt = script
        self.scipt.init(*args)
        self.canon.charge_balle()


    def update(self):
        """
        Appelée plusieurs fois par seconde.
        Appelle toutes les fonctions liées au mouvement de la balle (timer) et du jeu.
        """

        temp_update = time.time() # pour le timer et le chrono
        if(len(self.balles) == 1): self.balles[0].update(self.DELTA)
        else: self.canon.charge_balle()
        self.canon.update(self.DELTA)
        self.scipt.update(self.DELTA)

        # fps en fonction du temps de la fonction
        temps = time.time()
        tps_update = temps-temp_update
        delai = int((self.DELTA-tps_update)*1000)
        if(delai <= 0):
            if(tps_update > 2*self.DELTA): # on fixe une valeur au delà de laquelle on considère qu'on a une trop faible valeur d'images par seconde
                print(f"LOW FPS ({int(1/tps_update)}/{self.FPS})")
            delai = 1
        self.racine.after(delai, self.update)


# idéalement, chaque script aurait une réference a la fenetre principale, et elle ne serait pas stoqués dans les variables globalles.
# ce n'ait malheureusement pas possible car cela causserait un import circulaire (script -> fenetre -> script)
fenetre = Fenetre()