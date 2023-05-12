from core.etat import Etat
from core.fenetre import fenetre
import core.gestionnaireDeNiveaux as lvl
from core.gestionnaireDeTheme import theme
from utilitaire import Vector2Int, Vector2
import core.gestionnaireDeNiveaux as lvl


class FinDePartie(Etat):

    def init(self, gagner, score: int, chrono: float, niveau: str) -> None:
        """Initialise la fenêtre de fin de partie"""
        self.niveau= niveau
        if gagner==True:
            message=f"          Bravo !! Tu as gagné ;)\nTu as réussi à finir le jeu en {chrono} s\nTon score est de : {score}"
        elif gagner == False:
            message =f"Tu as perdu... \nTu as fini le jeu en {chrono} s\nTon score est de : {score}"
        
        lvl.charge_niveau("#finDePartie", fenetre.grille, fenetre.canon)
        fenetre.grille.bind_tag("replay", self.replay)
        fenetre.grille.tag_bille(Vector2Int(3,22), "replay")
        fenetre.grille.bind_tag("menu", self.menu)
        fenetre.grille.tag_bille(Vector2Int(19,22), "menu")
        self.ids = [
            fenetre.canevas.create_text(*fenetre.grille.coordonees_to_position(Vector2Int(5,21)) - Vector2(fenetre.RAYON, 1), text="REJOUER", fill=theme.text[1], font="Helvetica 23 bold"),
            fenetre.canevas.create_text(*fenetre.grille.coordonees_to_position(Vector2Int(19,21)) - Vector2(fenetre.RAYON, 1), text="MENU", fill=theme.text[0], font="Helvetica 23 bold"),
            fenetre.canevas.create_text(250,250, text=message, fill=theme.text[0], font="ComicSansMS 15 ")
            ]
        fenetre.grille.gelee = True


    def clear(self) -> None:
        """Supprime la fenêtre de jeu une fois la partie terminée."""
        
        for id in self.ids:
            fenetre.canevas.delete(id)
        
    def replay(self, bille):
        fenetre.set_etat("Jeu", self.niveau)

    def menu(self, bille):
        fenetre.set_etat("Menu")

fenetre.ajout_etat(FinDePartie())