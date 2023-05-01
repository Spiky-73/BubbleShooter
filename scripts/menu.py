from tkinter import messagebox
from core.script import Script
from core.fenetre import fenetre
from core.gestionnaireDeTheme import theme
from .jeu import Jeu
from utilitaire import Vector2, Vector2Int
import core.gestionnaireDeNiveaux as lvl


class Menu(Script):
    
    def init(self) -> None:

        lvl.charge_niveau("#menu", fenetre.grille, fenetre.canon)
        fenetre.grille.bind_tag("play", self.play)
        fenetre.grille.bind_tag("regles", self.regles)
        fenetre.grille.bind_tag("niveau", self.niveau_suiv)
        fenetre.grille.bind_tag("theme", self.theme_suiv)
        self.ids: list[int] = []
        self.niveau = "facile"
        self.theme = theme.nom

        fenetre.grille.tag_bille(Vector2Int(13,7), "play")
        fenetre.grille.tag_bille(Vector2Int(3,15), "regles")
        fenetre.grille.tag_bille(Vector2Int(20,15), "niveau")
        fenetre.grille.tag_bille(Vector2Int(22,39), "theme")
        self.ids.append(fenetre.canevas.create_text(*fenetre.grille.coordonees_to_position(Vector2Int(12,7)) - Vector2(fenetre.RAYON, 1), text="JOUER", fill=theme.text[0], font="Helvetica 25 bold"))
        self.ids.append(fenetre.canevas.create_text(*fenetre.grille.coordonees_to_position(Vector2Int(3,15)), text="REGLES", fill=theme.text[1], font="Helvetica 15 bold"))
        self.ids.append(fenetre.canevas.create_text(*(fenetre.grille.coordonees_to_position(Vector2Int(20,15))-Vector2(0, fenetre.RAYON)), text="NIVEAU", fill=theme.text[0], font="Helvetica 12 bold"))
        self.ids.append(fenetre.canevas.create_text(*(fenetre.grille.coordonees_to_position(Vector2Int(20,15))+Vector2(0, fenetre.RAYON)), text=self.niveau.upper(), fill=theme.text[0], font="Helvetica 12 bold"))
        self.ids.append(fenetre.canevas.create_text(*fenetre.grille.coordonees_to_position(Vector2Int(22,39)), text="THEME", fill=theme.text[1], font="Helvetica 10 bold"))
        self.ids.append(fenetre.canevas.create_text(*(fenetre.grille.coordonees_to_position(Vector2Int(22,40))+Vector2(fenetre.RAYON, 0)), text=theme.nom.upper(), fill=theme.text[1], font="Helvetica 10 bold"))
        fenetre.grille.gelee = True

    

    def clear(self) -> None:
        for id in self.ids:
            fenetre.canevas.delete(id)


    def update(self, delta: float) -> None:
        return super().update(delta)

    def play(self, bille):
        fenetre.set_scipt(Jeu(), self.niveau)
    
    def niveau_suiv(self, bille):
        niveaux = list(lvl.iter_niveaux())
        self.niveau = niveaux[(niveaux.index(self.niveau)+1)%len(niveaux)]
        fenetre.canevas.itemconfigure(self.ids[3], text = self.niveau.upper())
    
    def theme_suiv(self, bille):
        themes = list(theme.iter_themes())
        self.theme = themes[(themes.index(self.theme)+1)%len(themes)]
        fenetre.canevas.itemconfigure(self.ids[5], text = self.theme.upper())
        theme.charge_theme(self.theme)
        fenetre.set_scipt(Menu())

    def regles(self, bille):
        """Ouvre une message box contenant les règles du jeu."""

        messagebox.showinfo("Règles du jeu ", 
                            "Objectif : \nExplose toutes les billes pour vider ton plateau ! \n "
                            
                            "\nPour y parvenir, il faut lancer la balle sur les billes du plateau de la même couleur. \nSi la balle touche un groupe de deux billes de la même couleur ou plus, alors ce groupe éclate. \nSi la bille qu'elle touche n'est pas de la même couleur, alors la balle que tu as lancé s'y accroche."
                            
                            "\n \nCommandes :\n"
                            "À l’aide de ta souris, glisse sur l'endroit où tu veux envoyer la balle. Un tracé de ton lancer apparaitra et t’aidera beaucoup pour viser correctement et toucher ta cible. Lorsque tu es certain de ton plan de tir, il suffit de cliquer (clic gauche de ta souris).\n"

                            "Tu peux te servir des parois pour faire rebondir ta balle et parvenir aux endroits les plus inaccessibles.\n"

                            "\nÀ chaque bille éclatée, tu gagnes des points. Si tu manques ton coup, ta bulle se collera aux autres et te rajoutera un handicap pour atteindre ton but.\n"

                            "Pour augmenter ton score, essaye d'exploser des grands groupes de billes. Plus le groupe de billes qui explose est grand, plus tes points gagnés sont multipliés ! Ta rapidité est aussi prise en compte pour calculer ton score alors tente d'éliminer toutes les billes le plus rapidement possible !"

                            "\n\nSi une des billes touche le bas du plateau, tu perds la partie. En revanche, si tu les élimines toutes, tu gagnes la partie.\nA toi de jouer ! :)\n")  

