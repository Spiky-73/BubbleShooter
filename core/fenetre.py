import time # pour le chronomètre
import tkinter as tk
import math

from .balle import Balle
from .canon import Canon
from .grilleHexagonale import GrilleHexagonale
from .etat import Etat


from .gestionnaireDeTheme import theme
from utilitaire import Vector2Int


class Fenetre:

    RAYON = 10
    DIMENSIONS = Vector2Int(25, 42)
    HAUTEUR = 2*RAYON*math.cos(math.pi/6)

    FPS = 60
    DELTA = 1/FPS
    
    def __init__(self):
        """ Initialise la fenêtre de jeu avec le niveau choisi. """

        self._etats: dict[str, Etat] = {}

        self.racine = tk.Tk()        
        self.racine.title(f"Bubbleshooter")
        self.racine.resizable(height = False, width = False)

        self.canevas = tk.Canvas(self.racine, width=self.DIMENSIONS.x*2*self.RAYON, height=self.DIMENSIONS.y*self.HAUTEUR, bd=0, highlightthickness=0, bg=theme.fond)
        self.canevas.pack()
        
        self.grille = GrilleHexagonale(self.canevas, self.DIMENSIONS, self.RAYON)
        self.balles: list[Balle] = []
        self.canon = Canon(self.canevas, self.grille.coordonees_to_position(Vector2Int(13,39)), self.grille, self.RAYON, [0], self.balles)

        self.etat: Etat = None

        self.temp_update: float = 0

    def start(self, etat: str, *args):
        self.set_etat(etat, *args)
        self.update()
        self.racine.mainloop()


    def ajout_etat(self, etat: Etat):
        self._etats[etat.__class__.__name__] = etat

    def set_etat(self, etat: str, *args):
        if(self.etat != None):
            self.etat.clear()
        self.etat = self._etats[etat]
        self.grille.reset()
        self.canon.reset()
        self.canevas.configure(bg=theme.fond)
        self.etat.init(*args)
        self.canon.charge_balle()


    def update(self):
        """
        Appelée plusieurs fois par seconde.
        Appelle toutes les fonctions liées au mouvement de la balle (timer) et du jeu.
        """

        temp_update = time.time()
        delta = temp_update - self.temp_update
        self.temp_update = temp_update # pour le timer et le chrono
        if(len(self.balles) == 1):
            etat,  billes = self.etat.__class__.__name__, self.grille.compte_billes
            self.balles[0].update(delta)
            eclates = billes - self.grille.compte_billes
            if(etat == self.etat.__class__.__name__ and eclates > 0):
                self.etat.on_eclatement_bille(eclates+1)
        else: self.canon.charge_balle()
        self.canon.update(delta)
        self.etat.update(delta)

        # fps en fonction du temps de la fonction
        temps = time.time()
        tps_update = temps-temp_update
        delai = int((self.DELTA-tps_update)*1000)
        if(delai <= 0):
            if(tps_update > 2*self.DELTA): # on fixe une valeur au delà de laquelle on considère qu'on a une trop faible valeur d'images par seconde
                print(f"LOW FPS ({int(1/tps_update)}/{self.FPS})")
            delai = 1
        self.racine.after(delai, self.update)

        


# idéalement, chaque etat aurait une réference a la fenetre principale, et elle ne serait pas stoqués dans les variables globalles.
# ce n'ait malheureusement pas possible car cela causserait un import circulaire (etat -> fenetre -> etat)
fenetre = Fenetre()
