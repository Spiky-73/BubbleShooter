import csv
import pathlib

from typing import Iterator
from core.canon import Canon

from .grilleHexagonale import GrilleHexagonale
from utilitaire import Vector2Int
from .gestionnaireDeTheme import theme


_dossier = "niveaux" # pas utile de faire une classe


def charge_niveau(nom: str, grille: GrilleHexagonale, canon: Canon) -> None:
    """Charge un niveau."""

    path = f"etats/{nom[1:]}.csv" if(nom.startswith("#")) else f"{_dossier}/{nom}.csv" # charge le niveau à partir de son nom
    grille.reset()
    canon.reset()
    
    couleurs = []
    with open(path, encoding='utf-8') as csvfile: # lecture du fichier csv contenant le niveau choisi
        reader = csv.reader(csvfile,  delimiter=",")
        for j, ligne in enumerate(reader):
            if j == 0 and len(ligne) != grille.dimensions.x:
                grille.glissement()
            for i, c in enumerate(ligne): 
                if c != " ":
                    c = int(c)
                    if(not c in couleurs):
                        couleurs.append(c)
                    grille.place(Vector2Int(i,j), theme.billes[c])
    canon.couleurs = couleurs


def iter_niveaux() -> Iterator[str]:
    """Renvoie le nom de tous les thèmes disponibles."""

    path = pathlib.Path(_dossier)
    for theme in path.glob('*.csv'):
        yield theme.name.removesuffix(".csv")