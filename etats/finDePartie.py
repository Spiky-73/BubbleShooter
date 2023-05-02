from core.etat import Etat
from core.fenetre import fenetre
import core.gestionnaireDeNiveaux as lvl
from core.gestionnaireDeTheme import theme
from utilitaire import Vector2Int, Vector2

class FinDePartie(Etat):

    def init(self, score: int, chrono: float) -> None:
        """Fenêtre de fin de partie"""
        self.ids = [
            fenetre.canevas.create_text(250,250, text=f"Bravo ;) Tu as gagné ! \nTu as réussi à finir le jeu en {chrono} s\nTon score est de : {score}", fill=theme.text[0], font="Comic Sans MS 15 ")
        ]
        
    def clear(self) -> None:
        for id in self.ids:
            fenetre.canevas.delete(id)
