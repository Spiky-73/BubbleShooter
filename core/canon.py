import copy
import math
import random
import tkinter
from utilitaire import Vector2

from .balle import Balle
from .grilleHexagonale import GrilleHexagonale
from .gestionnaireDeTheme import theme

class Canon:

    VITESSE = 750
    TAILLE_RESERVE = 2
    RAYON_POINTILLES = 2
    ESPACEMENT_POINTILLES = 75
    ECHELLE_RESERVE = 0.5

    def __init__(self, canevas: tkinter.Canvas, position: Vector2, grille: GrilleHexagonale, rayon: int, couleurs: list[int], balles: list[Balle]) -> None:
        self.canevas = canevas
        self.canevas.bind('<Button-1>', self.envoi_balle)
        self.canevas.bind('<Button-3>', self.discard_balle)
        self.position = position # là où on tire la balle, en bas au centre
        self.grille = grille
        self.rayon = rayon
        self.couleurs = couleurs

        self.souris = Vector2(0,0)
        self.canevas.bind("<Motion>", self._mouvement_souris)

        self.balles_mobiles = balles
        self.balle: Balle = None

        self.centre_balle = Vector2(self.rayon, self.rayon)
        self.centre_balle_reserve = self.centre_balle * self.ECHELLE_RESERVE
        
        self.reserve: list[tuple[int, str]] = []
        self.position_reserve = self.position + self.centre_balle
        self.delta_reserve = Vector2(0, self.rayon*1.5)

        self.pointilles: list[int] = [] # crée les pointillés a l'avance pour éviter de les recréer en permanace et augmenter les performances
        self.pointilles_visibles = 0
        self.offset_pointilles = 0
        for _ in range(50):
            self.pointilles.append(self.canevas.create_oval(-self.RAYON_POINTILLES, -self.RAYON_POINTILLES, self.RAYON_POINTILLES, self.RAYON_POINTILLES, fill="", outline=""))
        self.pointilles.append(self.canevas.create_oval(*(self.centre_balle*-1), *self.centre_balle, fill="", outline="", width=2))

    def reset(self):
        for id, _ in self.reserve: self.canevas.delete(id)

        self.reserve = []
        if(self.balle is not None):
            self.canevas.delete(self.balle.id)
            self.balle = None

    def charge_balle(self):
        """Crée la balle au niveau du canon à balles (en bas de la fenêtre) et choisi sa couleur aléatoirement."""
        if(self.balle is not None): return
        
        if len(self.reserve)-1 < self.TAILLE_RESERVE:
            # ajoute des balles a la réserve, d'un rayon plus petit 
            self.remplir_reserve()

        # charge la balle dans le canon
        id, col = self.reserve.pop(0)
        self.canevas.delete(id)
        self.balle = Balle(self.canevas, self.grille, self.balles_mobiles, copy.copy(self.position), self.rayon, Vector2(0, -self.VITESSE), col)

        # bouge les balles de la reserve
        for i, (r, c) in enumerate(self.reserve):
            self.canevas.moveto(r, *(self.position_reserve+self.delta_reserve*i-self.centre_balle_reserve))
            color = {"fill": "", "outline":""} if i >= self.TAILLE_RESERVE else {"fill": c, "outline": "#000000"}
            self.canevas.itemconfigure(r, **color)

    def remplir_reserve(self):
        "Ajoute autant de balles que de couleurs dans le niveau dans la reserve dans un ordre aléatoire."
        cols = self.couleurs.copy()
        random.shuffle(cols)
        for ic in cols:
            id = self.canevas.create_oval(*(self.centre_balle_reserve*-1),*self.centre_balle_reserve, fill="", outline="")
            self.reserve.append((id, theme.billes[ic]))

    def envoi_balle(self, event) : 
        """Envoie la balle dans la direction de la souris."""
        if(self.balle is None): return

        # cache tous les pointillés et la simulation
        for i in range(0, self.pointilles_visibles):
            self.canevas.itemconfigure(self.pointilles[i], fill="")
        self.canevas.itemconfigure(self.pointilles[-1], outline="")
        self.balles_mobiles.append(self.balle)
        self.balle = None
    
    def discard_balle(self, event) : 
        """Ignore la balle actuelle et charge la suivante."""
        if(self.balle is None): return
        self.canevas.delete(self.balle.id)
        self.balle = None
        self.charge_balle()
    
    
    def update(self, delta: float):
        """Simule la trajectoire de la balle et l'affiche pour guider le joueur."""

        if(self.balle is None): return # on ne fait rien si la balle est lancée
        direction: Vector2 = self.souris - self.position
        angle = math.atan2(direction.y, direction.x)
        vitesse = Vector2(math.cos(angle), math.sin(angle)) * self.VITESSE

        self.balle.vitesse = copy.copy(vitesse) # copié car on veut en garder en sauvegarde pour plus tard dans la fonction
        
        distance = self.offset_pointilles
        self.pointilles_visibles = 0
        dt = 1/250
        while not self.balle.collision() and self.pointilles_visibles < len(self.pointilles)-1: # tant qu'on a pas rencontré de bille et donc que la balle est en mouvement
            self.balle.deplacer(dt)
            distance += self.balle.vitesse.norme * dt
            if(distance >= self.ESPACEMENT_POINTILLES): # affiche et bouge un pointillé à la place de la balle
                self.canevas.moveto(self.pointilles[self.pointilles_visibles], *(self.balle.position-Vector2(self.RAYON_POINTILLES, self.RAYON_POINTILLES)))
                self.canevas.itemconfigure(self.pointilles[self.pointilles_visibles], fill=self.balle.couleur)
                distance -= self.ESPACEMENT_POINTILLES
                self.pointilles_visibles+=1

        # décale les pointillés avec le temps pour donner un effet annimé
        self.offset_pointilles = (self.offset_pointilles-self.balle.vitesse.norme * delta/2)%self.ESPACEMENT_POINTILLES
        self.balle.stabilise_position()
        
        for i in range(self.pointilles_visibles, len(self.pointilles)-1): # cache les pointillés inutilisés
            self.canevas.itemconfigure(self.pointilles[i], fill="")
        
        # affiche la balle simulée dans sa position finale
        self.canevas.moveto(self.pointilles[-1], * (self.grille.coordonees_to_position(self.grille.position_to_coordonees(self.balle.position))-self.centre_balle))
        self.canevas.itemconfigure(self.pointilles[-1], outline=self.balle.couleur) # pointillés de la couleur de la balle qu'on lance
        
        # reinitialise la balle simulée
        self.balle.position = copy.copy(self.position)
        self.balle.vitesse = vitesse
        self.canevas.moveto(self.balle.id, *self.balle.coin_NW)


    def _mouvement_souris(self, event: tkinter.Event):
        """Actualise la position de la souris."""
        self.souris = Vector2(event.x, event.y)
