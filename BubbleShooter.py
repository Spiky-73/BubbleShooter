"""
Exécutez ce fichier pour jouer au jeu.
"""

from core.fenetre import fenetre
from etats.menu import Menu


if __name__ == "__main__":
    fenetre.start(Menu())
