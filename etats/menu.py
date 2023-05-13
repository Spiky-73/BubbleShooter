from tkinter import messagebox
from core.etat import Etat
from core.fenetre import fenetre
from core.gestionnaireDeTheme import theme
from utilitaire import Vector2, Vector2Int
import core.gestionnaireDeNiveaux as lvl

class Menu(Etat):
    
    def init(self) -> None:
        """Constructeur"""

        self.niveau = "facile"
        self.theme = theme.nom


        # Chargement du niveau et ajout des tags
        lvl.charge_niveau("#menu", fenetre.grille, fenetre.canon)
        fenetre.grille.tag_bille(Vector2Int(13,7), "play")
        fenetre.grille.tag_bille(Vector2Int(3,15), "regles")
        fenetre.grille.tag_bille(Vector2Int(20,15), "niveau")
        fenetre.grille.tag_bille(Vector2Int(22,39), "theme")
        fenetre.grille.tag_bille(Vector2Int(1,39), "quitter")
        
        # Enregistrement des tags
        fenetre.grille.bind_tag("play", self.play)
        fenetre.grille.bind_tag("regles", self.regles)
        fenetre.grille.bind_tag("niveau", self.niveau_suiv)
        fenetre.grille.bind_tag("theme", self.theme_suiv)
        fenetre.grille.bind_tag("quitter", self.quitter)

        # Ajout des textes
        # On utilise des position des billes pour que l'interface reste a l'échelle quel que soit la taille de la fenètre
        self.ids = [
            fenetre.canevas.create_text(*fenetre.grille.coordonees_to_position(Vector2Int(12,7)) - Vector2(fenetre.RAYON, 1), text="JOUER", fill=theme.text[0], font=theme.police(fenetre.RAYON*2.2)),
            fenetre.canevas.create_text(*fenetre.grille.coordonees_to_position(Vector2Int(3,15)), text="REGLES", fill=theme.text[1], font=theme.police(fenetre.RAYON*1.5)),
            fenetre.canevas.create_text(*(fenetre.grille.coordonees_to_position(Vector2Int(20,15))-Vector2(0, fenetre.RAYON)), text="NIVEAU", fill=theme.text[0], font=theme.police(fenetre.RAYON*1.2)),
            fenetre.canevas.create_text(*(fenetre.grille.coordonees_to_position(Vector2Int(20,15))+Vector2(0, fenetre.RAYON)), text=self.niveau.upper(), fill=theme.text[0], font=theme.police(fenetre.RAYON*1.2)),
            fenetre.canevas.create_text(*fenetre.grille.coordonees_to_position(Vector2Int(22,39)), text="THEME", fill=theme.text[1], font=theme.police(fenetre.RAYON)),
            fenetre.canevas.create_text(*(fenetre.grille.coordonees_to_position(Vector2Int(22,40))+Vector2(fenetre.RAYON, 0)), text=theme.nom.upper(), fill=theme.text[1], font=theme.police(fenetre.RAYON)),
            fenetre.canevas.create_text(*(fenetre.grille.coordonees_to_position(Vector2Int(1,39))+Vector2(0, fenetre.RAYON)), text="QUITTER", fill=theme.text[1], font=theme.police(fenetre.RAYON)),
        ]

        # Gèle la grille pour que les boutons se régénère
        fenetre.grille.gelee = True


    def clear(self) -> None:
        """Supprime les textes."""
        for id in self.ids:
            fenetre.canevas.delete(id)
    

    def play(self, bille):
        """Lance le jeu avec le niveau sélectioné."""
        fenetre.set_etat("Jeu", self.niveau)

    
    def quitter(self, bille):
        """Quitte le jeu."""
        fenetre.stop()

    
    def niveau_suiv(self, bille):
        """Selectionne le niveau suivant dans la liste des niveaux."""

        # Récupère la liste des niveaux
        niveaux = list(lvl.iter_niveaux())

        # Passe au niveau suivant (facile --> moyen --> aléatoire) et actualise l'interface
        self.niveau = niveaux[(niveaux.index(self.niveau)+1)%len(niveaux)]
        fenetre.canevas.itemconfigure(self.ids[3], text = self.niveau.upper())

    
    def theme_suiv(self, bille):
        """Selectionne le thème suivant dans la liste des thèmes."""

        # Récupère la liste des thèmes
        themes = list(theme.iter_themes())

        # Passe au thème suivant et actualise l'interface
        self.theme = themes[(themes.index(self.theme)+1)%len(themes)]
        fenetre.canevas.itemconfigure(self.ids[5], text = self.theme.upper())

        # Charge le thème suivant et recharge le menu pour le le thème prenne effet
        theme.charge_theme(self.theme)
        fenetre.set_etat("Menu")


    def regles(self, bille):
        """Ouvre une message box contenant les règles du jeu."""

        messagebox.showinfo("Règles du jeu ", 
                            "Objectif : \nExplose toutes les billes pour vider ton plateau ! \n "
                            
                            "\nPour y parvenir, il faut lancer la balle sur les billes du plateau de la même couleur. \nSi la balle touche un groupe de deux billes de la même couleur ou plus, alors ce groupe éclate. \nSi la bille qu'elle touche n'est pas de la même couleur, alors la balle que tu as lancé s'y accroche."
                            
                            "\n \nCommandes :\n"
                            "À l’aide de ta souris, glisse sur l'endroit où tu veux envoyer la balle. Un tracé de ton lancer apparaitra et t’aidera beaucoup pour viser correctement et toucher ta cible. Lorsque tu es certain de ton plan de tir, il suffit de cliquer (clic gauche de ta souris).\n"

                            "Tu peux te servir des parois pour faire rebondir ta balle et parvenir aux endroits les plus inaccessibles.\n"

                            "\nÀ chaque bille éclatée, tu gagnes des points. Si tu manques ton coup, ta bulle se collera aux autres et te rajoutera un handicap pour atteindre ton but.\n"

                            "\nTu as la possibilité de changer la balle que tu vas tirer avec ton canon. Les balles suivantes sont affichées dans l'ordre à côté du canon. Tu peux choisir de lancer la balle suivante plutôt que celle initialement dans ton canon. Pour cela, fais un clic droit avec ta souris. Attention, tu ne peux faire que 2 clics droits par tir au maximum !\n"

                            "Pour augmenter ton score, essaye d'exploser des grands groupes de billes. Plus le groupe de billes qui explose est grand, plus tes points gagnés sont multipliés ! Ta rapidité est aussi prise en compte pour calculer ton score alors tente d'éliminer toutes les billes le plus rapidement possible !"

                            "\n\nSi une des billes touche le bas du plateau, tu perds la partie. En revanche, si tu les élimines toutes, tu gagnes la partie.\nA toi de jouer ! :)\n")  


fenetre.ajout_etat(Menu())