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

        # Enregistrement des tags
        fenetre.grille.bind_tag("replay", self.replay)
        fenetre.grille.bind_tag("menu", self.menu)

        # Chargement du niveau et ajout des tags
        lvl.charge_niveau("#finDePartie", fenetre.grille, fenetre.canon)
        fenetre.grille.tag_bille(Vector2Int(3,22), "replay")
        fenetre.grille.tag_bille(Vector2Int(19,22), "menu")

        # Ajout du texte
        message = "Bravo !! Tu as gagné ;)" if gagner else "Tu as perdu..."
        message += f"\nTu as fini le jeu en {chrono:.2f} s\nTon score est de : {score}"
        self.ids = [
            fenetre.canevas.create_text(*fenetre.grille.coordonees_to_position(Vector2Int(5,21)) - Vector2(fenetre.RAYON, 0), text="REJOUER", fill=theme.text[1], font=theme.police(fenetre.RAYON*2)),
            fenetre.canevas.create_text(*fenetre.grille.coordonees_to_position(Vector2Int(19,21)) - Vector2(fenetre.RAYON, 0), text="MENU", fill=theme.text[0], font=theme.police(fenetre.RAYON*2)),
            fenetre.canevas.create_text(250,250, text=message, fill=theme.text[0], font=theme.police(fenetre.RAYON*1.5))
            ]
        
        fenetre.grille.gelee = True


    def clear(self) -> None:
        """Supprime les textes."""
        for id in self.ids:
            fenetre.canevas.delete(id)
        
    def replay(self, bille):
        """Relance une partie avec le même niveau."""
        fenetre.set_etat("Jeu", self.niveau)

    def menu(self, bille):
        """Passe au menu principal"""
        fenetre.set_etat("Menu")

fenetre.ajout_etat(FinDePartie())