from copy import deepcopy
import csv
import json
import math
import pathlib
import tkinter

from typing import Iterator

from grilleHexagonale import GrilleHexagonale
from utilitaire import Vector2Int
from gestionnaireDeTheme import theme


_dossier = "niveaux"

def charge_niveau(nom: str, canevas: tkinter.Canvas, rayon: int) -> tuple[GrilleHexagonale, list[int]]:
    """Charge un niveau"""   
    path = f"{_dossier}/{nom}.csv"
    hauteur = (2*rayon)*math.cos(math.pi/6)
    grille = GrilleHexagonale(canevas, int(canevas["width"]) // (2*rayon), int(int(canevas["height"])/hauteur), rayon)
    
    couleurs = []
    with open(path, encoding='utf-8') as csvfile: # lecture du fichier csv contenant le niveau choisi
        reader = csv.reader(csvfile,  delimiter=",")
        for j, ligne in enumerate(reader):
            if j == 0 and len(ligne) != grille.dimentions.x:
                grille.glissement()
            for i, c in enumerate(ligne): 
                if c != " ":
                    c = int(c)
                    if(not c in couleurs):
                        couleurs.append(c)
                    grille.place(Vector2Int(i,j), theme.billes[c])
    
    return grille, couleurs


def iter_niveaux() -> Iterator[str]:
    """Renvoie le nom de tous les themes disponibles"""
    path = pathlib.Path(_dossier)
    for theme in path.glob('*.csv'):
        yield theme.name.removesuffix(".csv")