"""
Exécutez ce fichier pour jouer au jeu.
"""
from core.fenetre import fenetre
from etats.menu import Menu

# import pathlib
# import tkinter as tk
# from tkinter import StringVar, messagebox, OptionMenu
# from gestionnaireDeTheme import theme
# import gestionnaireDeNiveaux

# from fenetreJeu import FenetresJeu

# class FenetresMenu:
    
#     def __init__(self): 
#         """ Constructeur pour intialiser la fenêtre principale de menu du jeu. """

#         self.racine = tk.Tk()
#         self.racine.title("Bubble Shooter")
#         self.racine.resizable(height = False, width = False)
        
#         self._creer_widgets()


#     def _creer_widgets(self):
#         """Ajoute l'interface du menu en créant les widgets."""
        
#         self.lb_nom = tk.Label(self.racine, text = "\nBUBBLE SHOOTER", font='Helvetica 18 bold')
#         self.lb_nom.pack(side=tk.TOP, fill='x')
        
#         self.btn_regles=tk.Button(self.racine, text='Règles du jeu')
#         self.btn_regles.pack(side=tk.TOP, fill='x') # pour que le bouton prenne toute la longueur
#         self.btn_regles.bind('<Button-1>', self.affiche_regles_jeu)

#         self.lb_themes = tk.Label(self.racine, text = "Thème")
#         self.lb_themes.pack(side=tk.LEFT, anchor=tk.N) # le place a gauche pour laisser la place au choix à droite
#         themes = list(theme.iter_themes())
#         self.var_theme = StringVar(self.racine)
#         self.var_theme.set(themes[0]) # default value
#         self.om_theme = OptionMenu(self.racine, self.var_theme, *themes)
#         self.om_theme.pack(side=tk.TOP, anchor=tk.N)

#         self.lb_niveau = tk.Label(self.racine, text = "\nChoisissez le niveau :", font='Helvetica 11 bold')
#         self.lb_niveau.pack(side=tk.TOP, fill='x')
#         self.btns_niveaux: list[tk.Button] = []
#         for niveau in gestionnaireDeNiveaux.iter_niveaux(): # lecture des fichiers csv contenant la disposition prédéfinie des billes (niveaux)
#             btn = tk.Button(self.racine, text=niveau)
#             btn.pack(side=tk.BOTTOM, anchor=tk.N)
#             btn.bind('<Button-1>', self._lancer_jeu)
#             self.btns_niveaux.append(btn)


#     def _lancer_jeu(self, event: tk.Event):
#         self.lancer_jeu(event.widget["text"]) # la fonction est appelée par l'event
    
    
#     def lancer_jeu(self, niveau: str):
#         """Crée la fenêtre de jeu et ferme la fenêtre principale."""
#         theme.charge_theme(self.var_theme.get())
#         self.racine.destroy()
#         jeu = FenetresJeu(niveau)
#         jeu.racine.mainloop()


#     def affiche_regles_jeu(self, event):
#         """Ouvre une message box contenant les règles du jeu."""

#         messagebox.showinfo("Règles du jeu ", 
#                             "Objectif : \nExplose toutes les billes pour vider ton plateau ! \n "
                            
#                             "\nPour y parvenir, il faut lancer la balle sur les billes du plateau de la même couleur. \nSi la balle touche un groupe de deux billes de la même couleur ou plus, alors ce groupe éclate. \nSi la bille qu'elle touche n'est pas de la même couleur, alors la balle que tu as lancé s'y accroche."
                            
#                             "\n \nCommandes :\n"
#                             "À l’aide de ta souris, glisse sur l'endroit où tu veux envoyer la balle. Un tracé de ton lancer apparaitra et t’aidera beaucoup pour viser correctement et toucher ta cible. Lorsque tu es certain de ton plan de tir, il suffit de cliquer (clic gauche de ta souris).\n"

#                             "Tu peux te servir des parois pour faire rebondir ta balle et parvenir aux endroits les plus inaccessibles.\n"

#                             "\nÀ chaque bille éclatée, tu gagnes des points. Si tu manques ton coup, ta bulle se collera aux autres et te rajoutera un handicap pour atteindre ton but.\n"

#                             "Pour augmenter ton score, essaye d'exploser des grands groupes de billes. Plus le groupe de billes qui explose est grand, plus tes points gagnés sont multipliés ! Ta rapidité est aussi prise en compte pour calculer ton score alors tente d'éliminer toutes les billes le plus rapidement possible !"

#                             "\n\nSi une des billes touche le bas du plateau, tu perds la partie. En revanche, si tu les élimines toutes, tu gagnes la partie.\nA toi de jouer ! :)\n")  

        
if __name__ == "__main__":
    fenetre.start(Menu())
    # app.racine.mainloop()
