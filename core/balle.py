import tkinter
from .grilleHexagonale import GrilleHexagonale
from utilitaire import Vector2, Vector2Int

class Balle:

    def __init__(self, canevas: tkinter.Canvas, grille: GrilleHexagonale, balles: list, position: Vector2, rayon: int, vitesse: Vector2, couleur: str):
        """Constructeur : initialise la balle avec ses paramètres."""

        self.canevas = canevas
        self.taille_canevas = Vector2Int(int(self.canevas["width"]), int(self.canevas["height"]))
        self.grille = grille
        self.position = position
        self.rayon = rayon
        self.couleur = couleur
        self.vitesse = vitesse
        self.id = self.canevas.create_oval(*self.coin_NW, *self.coin_SE, fill=self.couleur)
        self.balles = balles


    @property
    def coin_NW(self) -> Vector2:
        """ Définit le coin en haut à gauche de la balle."""

        return self.position - Vector2(self.rayon, self.rayon)
    
    
    @property
    def coin_SE(self) -> Vector2:
        """Définit le coin en bas à droite de la balle."""

        return self.position + Vector2(self.rayon, self.rayon)
    

    def update(self, delta: float):
        """Actualise la balle et sa position sur le canevas (si elle bouge, rebondit). Déplacement de la balle."""

        self.deplacer(delta)

        if(self.collision()):
            self.stabilise_position()
            self.placer() # place la balle s'il y a collision


    def placer(self) -> None:
        """Place la balle dans la cellule la plus proche."""

        self.canevas.delete(self.id)
        coords = self.grille.position_to_coordonees(self.position)
        self.grille.place(coords, self.couleur)
        self.grille.test_eclate_groupe(coords)

        self.balles.remove(self) # supprime la balle
    
    
    def deplacer(self, dt: float) -> None:
        """
        Déplace une balle sur dt secondes et prend en compte les collisions.
        """
        self.position += self.vitesse * dt

        if self.coin_NW.x < 0 : # si la balle sort de la fenetre
            self.position.x = self.rayon - self.coin_NW.x # North West
            self.vitesse.x *= -1 # elle rebondit contre le mur

        elif self.coin_SE.x > self.taille_canevas.x : # position de la balle et position du bord
            self.position.x = self.taille_canevas.x-self.rayon - (self.coin_SE.x-self.taille_canevas.x) 
            self.vitesse.x *= -1 # change la direction de la balle
    
        if self.coin_SE.y > self.taille_canevas.y : # bille - bord
            self.position.y =  self.taille_canevas.y-self.rayon - (self.coin_SE.y-self.taille_canevas.y)
            self.vitesse.y *= -1

        self.canevas.moveto(self.id, *self.coin_NW) # ce qui déplace l'item sur le canevas

    
    def collision(self) -> bool:
        """Renvoie vrai si la balle touche le haut du canevas ou une bille de la grille"""
        
        # collision avec le haut du canevas
        if(self.coin_NW.y <= 0):
            return True
        
        # recupère la case de la balle et ses voisins
        coord = self.grille.position_to_coordonees(self.position)
        voisins = self.grille.VOISINS[(coord.y-self.grille.grande_ligne)%2]

        for delta in voisins: # regarde si il y a une collision
            n_pos = delta + coord
            if self.grille.coords_valides(n_pos):
                id = self.grille[n_pos]
                if(id != -1 and self.position.distance(self.grille.coordonees_to_position(n_pos)) <= self.rayon + self.grille.rayon): # teste s'il y a contact
                    return True
        return False
    
    
    def stabilise_position(self):
        """Corrige la position de la balle jusqu'à ce qu'il n'y ait plus de collisions et que la balle puisse se poser dans une case vide"""

        self.vitesse *=-1
        while True: # tant que on se poserait sur une case occupée
            coords = self.grille.position_to_coordonees(self.position)
            if(self.grille.coords_valides(coords) and self.grille[coords] == -1):
                break
            self.deplacer(1/1000)
        self.vitesse *=-1