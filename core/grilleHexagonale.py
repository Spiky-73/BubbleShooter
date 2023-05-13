import math
import random
import tkinter
from typing import Callable, Literal
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

    def __init__(self, canevas: tkinter.Canvas, dimensions: Vector2Int, rayon: int, grande_ligne: Literal[0,1] = 0):
        """Initialise la grille."""

        # Empéche les bille placé sur la grille au préalable d'écalter
        # Empéche les billes détachées d'éclater
        self.gelee = False

        # Variables
        self.canevas = canevas
        self.dimensions = dimensions
        self.rayon = rayon
        self.hauteur = (2*self.rayon)*math.cos(math.pi/6)
        self.centre = Vector2(self.rayon, self.rayon)
        self.grande_ligne = grande_ligne
        self.nb_billes = 0
        self.img_eclats = tkinter.PhotoImage(file="images/eclats.png").subsample(6) # pour l'animation

        # Billes boutons
        self._binds: dict[str, Callable[[Vector2Int], None]] = {}

        # Crée la grille
        self._grille: list[list[int]] = []
        for y in range(self.dimensions.y):
            self._grille.append([-1 for _ in range(self.dimensions.y-(y-self.grande_ligne)%2)])



    def bind_tag(self, nom: str, action: Callable[[Vector2Int], None]) -> None:
        """Relie une action à un tag de bille."""
        self._binds[nom] = action


    def tag_bille(self, bille: Vector2Int, tag: str):
        """Ajoute un tag a une bille"""
        self.canevas.addtag_withtag(tag, self[bille])


    def __getitem__(self, coords: Vector2Int) -> int:
        """Renvoie l'id de la bille dans la case correspondante."""
        return self._grille[coords.y][coords.x]


    def place(self, bille: Vector2Int, color: str):
        """Ajoute une bille sur le caneva."""

        # out of bounds
        y = max(0, min(bille.y, len(self._grille)-1))
        x = max(0, min(bille.x, len(self._grille[y])))
        
        # Crée l'image de la bille
        position = self.coordonees_to_position(bille) # appel de coordonees_to_position pour la conversion
        self._grille[y][x] = self.canevas.create_oval(*(position-self.centre), *(position+self.centre), fill=color, tags="Bille")
        
        # Rend les billes placés éclatables si la grille est gelée 
        if(self.gelee): self.canevas.addtag_withtag("temp", self._grille[y][x])
            
        self.nb_billes += 1

    
    def enleve(self, bille: Vector2Int):
        """Supprime une bille sur le caneva."""

        # Efface la bille
        self.canevas.delete(self._grille[bille.y][bille.x])
        self._grille[bille.y][bille.x] = -1
        self.nb_billes -= 1


    def eclate(self, bille: Vector2Int):
        """Eclate une bille."""
        
        # Crée l'animation
        pos = self.coordonees_to_position(bille)
        anim = self.canevas.create_image(pos.x,pos.y, image = self.img_eclats, anchor=tkinter.CENTER)
        
        # Supréssion permanente de la bille
        if(not self.gelee or "temp" in self.canevas.gettags(self[bille])):
            self.enleve(bille)
            self.canevas.after(random.randint(100, 500), self._eclate_bille_fin, anim)
        
        # Supression temporaire de la bille si la bille est gelée
        else:
            # Cachel la bille
            id = self[bille]
            color: str = self.canevas.itemcget(id, "fill")
            self.canevas.itemconfigure(id, fill="", outline="")
           
            # Régénaration de la bille
            self.canevas.after(random.randint(100, 500), self._eclate_bille_gelee_fin, anim, id, color)

        
    def reset(self):
        """Efface toutes les bille de la grille"""

        # Réinitialisation des variables
        self.nb_billes = 0
        self.gelee = False
        self._binds = {}

        # Réinitialisation de la grille
        for y in range(self.dimensions.y):
            cl = (y-self.grande_ligne)%2
            for x in range(self.dimensions.x-cl):
                if(self._grille[y][x] != -1): self.canevas.delete(self._grille[y][x])
                self._grille[y][x] = -1


    def glissement(self):
        """Fait glisser les billes de la grille une ligne vers le bas"""

        # Modifie la grille
        self.grande_ligne = (self.grande_ligne+1)%2
        self._grille.insert(0, [-1 for _ in range(self.dimensions.x-self.grande_ligne)])
        
        # Efface les billes de la ligne du bas
        for bille in self._grille.pop():
            self.canevas.delete(bille)

        # Bouge les billes
        self.canevas.move("Bille", 0, -self.hauteur)


    def get_groupe(self, bille: Vector2Int) -> tuple[list[Vector2Int], dict[str, Vector2Int]]:
        """
        Renvoie les coordonnées des billes formant un groupe de couleur.
        Renvoi aussi les tags éclatés et la position de leur bille.
        """

        # Initialise un BFS avec une condition
        tags: dict[str, Vector2Int] = {}
        groupe: list[Vector2Int] = []
        attente = [bille]
        color: str = self.canevas.itemcget(self[bille], "fill")

        # BFS avec une condition
        while len(attente) != 0:
            pos = attente.pop()
            voisins = self.VOISINS[pos.y%2-self.grande_ligne]
            for delta in voisins:
                n_pos = pos + delta
                if self.coords_valides(n_pos) and not n_pos in groupe:
                    id = self[n_pos]
                    if(id != -1 and self.canevas.itemcget(id, "fill") == color):
                        for tag in self.canevas.gettags(id): tags[tag] = n_pos
                        attente.append(n_pos)
                        groupe.append(n_pos)

        del tags["Bille"] # surpime ce tag car toute les billes l'on
        return groupe, tags
    
       
    def test_eclate_groupe(self, bille: Vector2Int):
        """Teste si la bille touchée appartient à un groupe d'au moins 2 billes de même couleur que la balle lancée."""


        # Récupére le groupe et les tags touchés
        groupe, tags = self.get_groupe(bille)

        # Vérifie si le groupe doit être éclaté
        if(len(groupe) < 3 and len(tags) == 0): return
        
        # Eclates toutes les billes
        if(len(groupe) > 1):
            for b in groupe:
                self.eclate(b) # on éclate car le chaîne ainsi formée comporte au minimum 3 billes de la même couleur
        
        # Eclate les billes détachées
        if(not self.gelee):self.eclate_billes_detaches()

        # Appéles les fonction associées aux tags
        for tag, b in tags.items():
            if(tag in self._binds): self._binds[tag](b)


    def eclate_billes_detaches(self):
        """Eclate les billes qui ne sont pas rattachées au haut de la grille"""

        # Stockage des données
        attente: list[Vector2Int] = []
        connectees: list[list[bool]] = []
        for y in range(0, self.dimensions.y):
            connectees.append([False for _ in range(self.dimensions.x-(y-self.grande_ligne)%2)])

        # Ajout des points de départ
        for x in range(self.dimensions.x-self.grande_ligne):
            if(self[Vector2Int(x, 0)] != -1): attente.append(Vector2Int(x, 0))
            connectees[0][x] = True

        # BFS a partir de toutes les billes pouvant servir de connection
        while len(attente) != 0:
            pos = attente.pop()
            voisins = self.VOISINS[pos.y%2-self.grande_ligne]
            for delta in voisins:
                n_pos = pos + delta
                if self.coords_valides(n_pos) and not connectees[n_pos.y][n_pos.x]:
                    connectees[n_pos.y][n_pos.x] = True
                    if(self[n_pos] != -1): attente.append(n_pos)

        #Suppression des billes non connectées
        eclates = 0
        for y in range(self.dimensions.y):
            cl = (y-self.grande_ligne)%2
            for x in range(self.dimensions.x-cl):
                if(self._grille[y][x] != -1 and not connectees[y][x]):
                    self.eclate(Vector2Int(x,y))
                    eclates += 1


    def coords_valides(self, coords: Vector2Int):
        """Renvoie vrai si les coordonnées sont dans la grille."""
        return 0 <= coords.y and coords.y < self.dimensions.y and 0 <= coords.x and coords.x < self.dimensions.x - (coords.y-self.grande_ligne)%2


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
        """Convertit des coordonnées dans la grille de billes en position sur le canevas"""
        x = self.rayon + coords.x*self.rayon*2 + (self.rayon * ((coords.y-self.grande_ligne)%2))
        y = self.rayon + coords.y * self.hauteur
        return Vector2(x, y)
    

    def _eclate_bille_fin(self, anim_id: int):
        self.canevas.delete(anim_id)
    
    def _eclate_bille_gelee_fin(self, anim_id: int, id_bille: int, color: str):
        self.canevas.delete(anim_id)
        self.canevas.itemconfigure(id_bille, fill=color, outline="black")