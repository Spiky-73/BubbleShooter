import copy
import math
import random
import tkinter
from utilitaire import Vector2

from .balle import Balle
from .grilleHexagonale import GrilleHexagonale
from .gestionnaireDeTheme import theme

class Canon:

    # paramètres
    VITESSE = 40 # billes/s
    TAILLE_RESERVE = 2
    RAYON_POINTILLES = 2
    ESPACEMENT_POINTILLES = 3 # billes
    ECHELLE_RESERVE = 0.5
    REJET_PAR_LANCE = 2

    def __init__(self, canevas: tkinter.Canvas, position: Vector2, grille: GrilleHexagonale, rayon: int, couleurs: list[int], balles: list[Balle]) -> None:
        """Constructeur qui initialise le canon."""

        self.canevas = canevas
        self.canevas.bind('<Button-1>', self.envoi_balle)
        self.canevas.bind('<Button-3>', self.discard_balle)
        self.position = position # position du canon : là où on tire la balle, en bas au centre
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

        self.pointilles: list[int] = [] # crée les pointillés à l'avance pour éviter de les recréer en permanence et augmenter les performances
        self.pointilles_visibles = 0
        self.offset_pointilles = 0
        self.balle_lances = 0
        self.rejet_restant = self.REJET_PAR_LANCE
        for _ in range(50):
            self.pointilles.append(self.canevas.create_oval(-self.RAYON_POINTILLES, -self.RAYON_POINTILLES, self.RAYON_POINTILLES, self.RAYON_POINTILLES, fill="", outline=""))
        self.pointilles.append(self.canevas.create_oval(*(self.centre_balle*-1), *self.centre_balle, fill="", outline="", width=2))


    def reset(self):
        """Réinitialise le canon à l'état de départ (nombre de possibilités de changement...)."""
        self.rejet_restant = self.REJET_PAR_LANCE
        self.balle_lances = 0
        for id, _ in self.reserve: self.canevas.delete(id)

        self.reserve = []
        if(self.balle is not None):
            self.canevas.delete(self.balle.id)
            self.balle = None


    def charge_balle(self):
        """Crée la balle au niveau du canon à balles (en bas de la fenêtre) et choisi sa couleur aléatoirement."""
        if(self.balle is not None): return
        
        # Ajoute des balles à la réserve, d'un rayon plus petit 
        while len(self.reserve)-1 < self.TAILLE_RESERVE:
            self.remplir_reserve()

        # Charge la balle dans le canon
        id, col = self.reserve.pop(0)
        self.canevas.delete(id)
        self.balle = Balle(self.canevas, self.grille, self.balles_mobiles, copy.copy(self.position), self.rayon, Vector2(0, 0), col) # de la couleur d'une des billes du niveau chargé

        # bouge les balles de la réserve
        for i, (r, c) in enumerate(self.reserve):
            self.canevas.moveto(r, *(self.position_reserve+self.delta_reserve*i-self.centre_balle_reserve))
            color = {"fill": "", "outline":""} if i >= self.TAILLE_RESERVE else {"fill": c, "outline": "#000000"} # contours des billes sont noirs (=#000000)
            self.canevas.itemconfigure(r, **color)


    def remplir_reserve(self):
        """Ajoute autant de balles que de couleurs dans le niveau dans la réserve dans un ordre aléatoire."""

        cols = self.couleurs.copy() # on récupère les couleurs disponibles dans le niveau chargé
        random.shuffle(cols) # mélange aléatoirement
        for ic in cols:
            id = self.canevas.create_oval(*(self.centre_balle_reserve*-1),*self.centre_balle_reserve, fill="", outline="")
            self.reserve.append((id, theme.billes[ic]))


    def envoi_balle(self, event) : 
        """Envoie la balle dans la direction de la souris."""

        if(self.balle is None): return

        # Cache tous les pointillés et la simulation quand on lance
        for i in range(0, self.pointilles_visibles):
            self.canevas.itemconfigure(self.pointilles[i], fill="")
        self.canevas.itemconfigure(self.pointilles[-1], outline="")
        self.balles_mobiles.append(self.balle)
        self.balle = None

        self.rejet_restant = self.REJET_PAR_LANCE
        self.balle_lances +=1
    

    def discard_balle(self, event) : 
        """Ignore la balle actuelle et charge la suivante, si on veut changer de balle avec un clic droit."""

        if(self.balle is None): return
        if self.rejet_restant <= 0: return
        if not self.grille.gelee: self.rejet_restant -= 1 # à chaque changement on enlève 1 au nombre de changements restants (2 par lancer)
        self.canevas.delete(self.balle.id)
        self.balle = None
        self.charge_balle()
    
    
    def update(self, delta: float):
        """Simule la trajectoire de la balle et l'affiche pour guider le joueur."""

        if(self.balle is None): return # on ne fait rien si la balle est lancée et en cours de mouvement
        
        # calcule le vecteur vitesse orienté vers la souris
        direction: Vector2 = self.souris - self.position # on récupère la direction de la souris
        angle = math.atan2(direction.y, direction.x)
        vitesse = Vector2(math.cos(angle), math.sin(angle)) * self.VITESSE * self.rayon*2

        # modifie la vitesse de la balle à lancer
        self.balle.vitesse = copy.copy(vitesse) # copié car on veut la garder en sauvegarde pour plus tard dans la fonction
        
        # intilialise les variables des pointillés
        # self.offset_pointilles permet de décaler les pointillés avec le temps
        distance = self.offset_pointilles
        self.pointilles_visibles = 0

        dt = 1/120 # pour s'actualiser toutes les 1/250 ème secondes

        # simule la boucle suivie par la balle lorsque elle est lancée
        while not self.balle.collision() and self.pointilles_visibles < len(self.pointilles)-1: # tant qu'on a pas rencontré de bille et donc que la balle est en mouvement
            
            # déplace la balle
            self.balle.deplacer(dt)
            
            # actualise la distance parcourue
            distance += self.balle.vitesse.norme * dt / (self.rayon*2)

            # affiche un pointillé à intervalle régulier a l'emplacement de la balle
            if(distance >= self.ESPACEMENT_POINTILLES):

                # affiche le pointillé et le configure
                self.canevas.moveto(self.pointilles[self.pointilles_visibles], *(self.balle.position-Vector2(self.RAYON_POINTILLES, self.RAYON_POINTILLES)))
                self.canevas.itemconfigure(self.pointilles[self.pointilles_visibles], fill=self.balle.couleur)

                # actualisation des variables
                distance -= self.ESPACEMENT_POINTILLES
                self.pointilles_visibles+=1 # rajoute des pointillés sur la ligne

        # décale les pointillés avec le temps pour donner un effet animé
        self.offset_pointilles = (self.offset_pointilles-self.balle.vitesse.norme/(self.rayon*2) * delta/2)%self.ESPACEMENT_POINTILLES
        self.balle.stabilise_position()
        
        # cache tous les pointillés inutilisés pour ne pas avoir à les recréer en permanence
        for i in range(self.pointilles_visibles, len(self.pointilles)-1): self.canevas.itemconfigure(self.pointilles[i], fill="")
        
        # affiche la balle simulée dans sa position finale
        self.canevas.moveto(self.pointilles[-1], * (self.grille.coordonees_to_position(self.grille.position_to_coordonees(self.balle.position))-self.centre_balle))
        self.canevas.itemconfigure(self.pointilles[-1], outline=self.balle.couleur) # pointillés de la couleur de la balle qu'on lance
        
        # réinitialise la balle simulée
        self.balle.position = copy.copy(self.position)
        self.balle.vitesse = vitesse
        self.canevas.moveto(self.balle.id, *self.balle.coin_NW)


    def _mouvement_souris(self, event: tkinter.Event):
        """Actualise la position de la souris."""

        self.souris = Vector2(event.x, event.y)
