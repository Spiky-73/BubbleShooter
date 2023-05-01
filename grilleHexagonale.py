import math
import random
import tkinter
from typing import Literal
from utilitaire import Vector2, Vector2Int

class GrilleHexagonale:

    VOISINS = [
        [
                    Vector2Int(-1,-1), Vector2Int(0,-1),
            Vector2Int(-1,0),  Vector2Int(0,0),  Vector2Int(1,0),
                    Vector2Int(-1,1),  Vector2Int(0,1)
        ], [
                    Vector2Int(0,-1), Vector2Int(1,-1), 
            Vector2Int(-1,0),  Vector2Int(0,0),  Vector2Int(1,0),
                    Vector2Int(0,1),  Vector2Int(1,1)
        ]
    ]

    def __init__(self, canevas: tkinter.Canvas, width: int, height: int, rayon, grande_ligne: Literal[0,1] = 0):

        self.canevas = canevas
        self.dimentions = Vector2Int(width, height)
        self.rayon = rayon
        self.hauteur = (2*self.rayon)*math.cos(math.pi/6)
        self.centre = Vector2(self.rayon, self.rayon)

        self.grande_ligne = grande_ligne


        self._grille: list[list[int]] = []
        for y in range(height):
            self._grille.append([-1 for _ in range(width-(y-self.grande_ligne)%2)])


        self.img_eclats = tkinter.PhotoImage(file="images/eclats.png").subsample(6)


    def __getitem__(self, coords: Vector2Int) -> int:
        """Renvoie l'id de la bille dans la case correspondante"""
        return self._grille[coords.y][coords.x]

    def place(self, bille: Vector2Int, color: str):
        """Ajoute une bille sur le caneva."""

        y = max(0, min(bille.y, len(self._grille)-1))
        x = max(0, min(bille.x, len(self._grille[y])))
        position = self.coordonees_to_position(bille) # appel de coordonees_to_position pour la conversion
        self._grille[y][x] = self.canevas.create_oval(*(position-self.centre), *(position+self.centre), fill=color, tags="Bille")
    
    def enleve(self, bille: Vector2Int):
        """Surprime une bille sur le caneva."""
        self.canevas.delete(self._grille[bille.y][bille.x])
        self._grille[bille.y][bille.x] = -1

    def eclate(self, bille: Vector2Int):
        """Eclate une bille."""

        self.enleve(bille)
        pos = self.coordonees_to_position(bille)

        anim = self.canevas.create_image(pos.x,pos.y, image = self.img_eclats, anchor=tkinter.CENTER)
        
        # supression de l'image
        self.canevas.after(random.randint(100, 500), self._eclate_bille_fin, anim)


    def glissement(self):
        self.grande_ligne = (self.grande_ligne+1)%2
        self._grille.insert(0, [-1 for _ in range(self.dimentions.x-self.grande_ligne)])
        for bille in self._grille.pop():
            self.canevas.delete(bille)
        self.canevas.move("Bille", 0, -self.hauteur)


    def get_groupe(self, bille: Vector2Int) -> list[Vector2Int]:
        """ Renvoie les coordonnées des billes formant un groupe de couleur."""

        # initialise un BFS
        groupe = [bille]
        attente = [bille]
        color: str = self.canevas.itemcget(self._grille[bille.y][bille.x], "fill")

        while len(attente) != 0: # BFS avec une condition
            pos = attente.pop()
            voisins = self.VOISINS[pos.y%2-self.grande_ligne]
            for delta in voisins:
                n_pos = pos + delta
                if self.coords_valides(n_pos) and not n_pos in groupe:
                    id = self[n_pos]
                    if(id != -1 and self.canevas.itemcget(id, "fill") == color):
                        attente.append(n_pos)
                        groupe.append(n_pos)
            
        return groupe
       
    def test_eclate_groupe(self, bille: Vector2Int):
        """Teste si la bille touchée appartient à un groupe d'au moins 2 billes de même couleur que la balle lancée."""

        groupe = self.get_groupe(bille)
        if(len(groupe) < 3): # si la chaine de billes de même couleur ainsi formée est < 2
            return 
        
        billes_a_tester: set[Vector2Int] = set()
        for b in groupe:
            voisins = self.VOISINS[b.y%2-self.grande_ligne]
            self.eclate(b) # on éclate car le chaîne ainsi formée comporte au minimum 3 billes de la même couleur
            for v in voisins:
                p = b+v
                if(not p in billes_a_tester):
                    billes_a_tester.add(p)
        
        self.eclate_billes_detaches()


    def eclate_billes_detaches(self):
        """Eclates les billes qui ne sont pas rattachées au haut de la grille"""

        # stoquage des données (-1: non exploré, )
        connectees: list[list[bool]] = []
        attente: list[Vector2Int] = []

        for y in range(0, self.dimentions.y):
            connectees.append([False for _ in range(self.dimentions.x-(y-self.grande_ligne)%2)])

        for x in range(self.dimentions.x-self.grande_ligne):
            if(self[Vector2Int(x, 0)] != -1): attente.append(Vector2Int(x, 0))
            connectees[0][x] = True

        # BFS a partir de toutes les billes pouvant servir de connection

        while len(attente) != 0: # BFS avec une condition
            pos = attente.pop()
            voisins = self.VOISINS[pos.y%2-self.grande_ligne]
            for delta in voisins:
                n_pos = pos + delta
                if self.coords_valides(n_pos) and not connectees[n_pos.y][n_pos.x]:
                    connectees[n_pos.y][n_pos.x] = True
                    if(self[n_pos] != -1): attente.append(n_pos)

        # suppresion des billes non connectés
        for y in range(self.dimentions.y):
            cl = (y-self.grande_ligne)%2
            for x in range(self.dimentions.x-cl):
                if(self._grille[y][x] != -1 and not connectees[y][x]): self.eclate(Vector2Int(x,y))



    def coords_valides(self, coords: Vector2Int):
        """Renvoie vrai si les coordonnés sont dans la grille."""
        return 0 <= coords.y and coords.y < self.dimentions.y and 0 <= coords.x and coords.x < self.dimentions.x - (coords.y-self.grande_ligne)%2

    def position_to_coordonees(self, position: Vector2) -> Vector2Int:
        """Convertit la position du centre d'une bille du canevas en coordonnées dans la grille de billes."""

        side = self.hauteur/(1+math.cos(math.pi/3))
        y, rem_y = divmod(position.y-self.rayon+side/2, self.hauteur)

        correction = 0
        if(rem_y > side and y != -1): correction = (rem_y-side) * math.tan(math.pi/3)
        position_x = position.x - correction
        type_ligne = (y-self.grande_ligne)%2

        x, rem_x = divmod(position_x - (self.rayon * type_ligne), self.rayon*2)
        if(correction != 0):
            if(rem_x > (self.rayon-correction)*2):
                y += 1
                x += type_ligne
                type_ligne = 1-type_ligne
        
        return Vector2Int(int(x), int(y))
    
    def coordonees_to_position(self, coords: Vector2Int) -> Vector2:
        """Convertit des coordonnées dans la grille de bille en position sur le canevas"""
        x = self.rayon + coords.x*self.rayon*2 + (self.rayon * ((coords.y-self.grande_ligne)%2))
        y = self.rayon + coords.y * self.hauteur
        return Vector2(x, y)
    

    def _eclate_bille_fin(self, anim_id: int):
        """Fin de l'animation."""
        self.canevas.delete(anim_id)