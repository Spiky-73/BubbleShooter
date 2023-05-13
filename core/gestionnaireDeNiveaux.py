import csv
import pathlib

from typing import Iterator
from core.canon import Canon

from .grilleHexagonale import GrilleHexagonale
from utilitaire import Vector2Int
from .gestionnaireDeTheme import theme


DOSSIER = "niveaux"
DOSSIER_ETATS = "etats"


def charge_niveau(nom: str, grille: GrilleHexagonale, canon: Canon) -> None:
    """
    Charge un niveau sur une grille et paramètre les balles du canon.
    Cherche le dossier dans "etat" si le niveau commence par '#'.
    """

    # Récupère le chemin du fichier
    path = f"{DOSSIER_ETATS if nom.startswith('#') else DOSSIER}/{nom[1:]}.csv"
    
    grille.reset()
    canon.reset()
    
    # Lecture du fichier
    couleurs = set()
    with open(path, encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile,  delimiter=",")
        for j, ligne in enumerate(reader):

            # Inverse la parite des lignes si necessaire
            if j == 0 and len(ligne) != grille.dimensions.x: grille.glissement()

            # Remplissage de la grille
            for i, c in enumerate(ligne):
                if c != " ":
                    c = int(c)
                    couleurs.add(c) # enregistre la couleur de la bille
                    grille.place(Vector2Int(i,j), theme.billes[c])

    # Paramètre le canon
    canon.couleurs = list(couleurs)


def iter_niveaux() -> Iterator[str]:
    """Renvoie le nom de tous les thèmes disponibles."""
    path = pathlib.Path(DOSSIER)
    for theme in path.glob('*.csv'):
        yield theme.name.removesuffix(".csv")