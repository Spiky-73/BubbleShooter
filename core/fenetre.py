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
    """
    Crée une fenêtre comportant une grille hexagonale et un canon à balles.
    Utilisez les fonctions `start`, `stop`, `set_etat` pour contrôler la fenêtre.
    """

    RAYON = 10 # rayon des billes, recalculé pour ajuster l'échelle du jeu
    DIMENSIONS = Vector2Int(25, 42)
    POSITION_CANNON = Vector2Int(DIMENSIONS.x//2, DIMENSIONS.y-3)
    HAUTEUR = 2 * RAYON * math.cos(math.pi/6)

    FPS = 60
    DELTA = 1/FPS
    
    def __init__(self):
        """Initialise la fenêtre de jeu."""

        # création de la racine
        self.racine = tk.Tk()        
        self.racine.title(f"Bubbleshooter") # pour la fenêtre de menu
        self.racine.resizable(height = False, width = False)

        # positionnement de la fenêtre et détermination de la taille des billes
        screenx_x, screen_y = (self.racine.winfo_screenwidth(), self.racine.winfo_screenheight())
        self.RAYON = int(screen_y/math.cos(math.pi/6)/(2*self.DIMENSIONS.y))-1
        self.HAUTEUR = 2*self.RAYON*math.cos(math.pi/6)
        self.racine.geometry(f'+{(screenx_x-self.DIMENSIONS.x*2*self.RAYON)//2}+0') # centre la fenêtre sur l'écran

        # ajout du canevas
        self.canevas = tk.Canvas(self.racine, width=self.DIMENSIONS.x*2*self.RAYON, height=self.DIMENSIONS.y*self.HAUTEUR, bd=0, highlightthickness=0, bg=theme.fond)
        self.canevas.pack()
        
        # création des éléments de jeu
        self.grille = GrilleHexagonale(self.canevas, self.DIMENSIONS, self.RAYON)
        self.balles: list[Balle] = [] # stocké dans une liste pour que le canon puisse ajouter et supprimer des balles directement
        self.canon = Canon(self.canevas, self.grille.coordonees_to_position(self.POSITION_CANNON), self.grille, self.RAYON, [0], self.balles)

        # variables de la boucle update
        self._etats: dict[str, Etat] = {}
        self.etat: Etat = None

        self.running = False
        self.temps_update: float = 0


    def start(self, etat: str, *args):
        """Lance programme sur etat Etat."""

        self.set_etat(etat, *args)
        self.running = True
        self.update()
        self.racine.mainloop()


    def stop(self):
        """Arrête le jeu."""

        self.running = False


    def ajout_etat(self, etat: Etat):
        """Enregistre un état."""

        self._etats[etat.__class__.__name__] = etat


    def set_etat(self, etat: str, *args):
        """
        Change l'état du jeu actuel.
        Appelez `stop` pour quitter le jeu.
        """

        if(self.etat != None): # pour éviter une erreur s'il n'y a pas déjà un état
            self.etat.clear()

        self.etat = self._etats[etat]
        self.grille.reset()
        self.canon.reset()
        self.canevas.configure(bg=theme.fond)
        self.etat.init(*args)
        self.canon.charge_balle()


    def update(self):
        """Appelée `FPS` fois par seconde pendant le fonctionement de la fenêtre."""
        
        if(not self.running):
            self.racine.destroy()
            return

        # calcul du delta avec le dernier appel de la fonction
        temps_update = time.time()
        delta = temps_update - self.temps_update
        self.temps_update = temps_update

        # actualise la balle si elle est lancée
        if(len(self.balles) == 1):
            etat, billes = self.etat.__class__.__name__, self.grille.nb_billes
            self.balles[0].update(delta)
            eclates = billes - self.grille.nb_billes
            if(etat == self.etat.__class__.__name__ and eclates > 0):
                self.etat.on_eclatement_bille(eclates+1)

            if(len(self.balles) == 0):
                self.canon.charge_balle()

        # actualise le canon
        self.canon.update(delta)

        # actualise l'état actuel
        self.etat.update(delta)

        # FPS en fonction du temps de la fonction
        temps = time.time()
        tps_update = temps-temps_update
        delai = int((self.DELTA-tps_update)*1000)
        if(delai <= 0):
            if(tps_update > 2*self.DELTA): # on fixe une valeur au delà de laquelle on considère qu'on a une trop faible valeur d'images par seconde
                print(f"LOW FPS ({int(1/tps_update)}/{self.FPS})")
            delai = 1
        self.racine.after(delai, self.update)


# idéalement, chaque état aurait une réference a la fenêtre principale, et elle ne serait pas stockée dans les variables globales
# ce n'est malheureusement pas possible car cela causerait un import circulaire (etat -> fenetre -> etat)
fenetre = Fenetre()
