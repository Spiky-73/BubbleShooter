"""
Exécutez ce fichier pour jouer au jeu.
"""
from etats import menu, jeu, finDePartie # est present ici pour que tout les etat s'enregistre a la fenetre. cela evite au etats de s'importer les uns les autres et de causer un import circulaire


from core.fenetre import fenetre

if __name__ == "__main__":
    fenetre.start("Menu")
