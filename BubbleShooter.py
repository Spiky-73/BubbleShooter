"""
Exécutez ce fichier pour jouer au jeu.
"""

from etats import menu, jeu, finDePartie # est présent ici pour que tous les états s'enregistrent à la fenêtre. Cela évite aux états de s'importer les uns les autres et de causer un import circulaire.

from core.fenetre import fenetre

if __name__ == "__main__":
    fenetre.start("Menu")
