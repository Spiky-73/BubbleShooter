"""
Exécutez ce fichier pour jouer au jeu
"""

import pathlib
import tkinter as tk
from tkinter import messagebox

from fenetreJeu import FenetresJeu

class FenetresMenu:
    
    def __init__(self):
        """Constructeur pour initialiser la fenêtre du jeu"""
        self.racine = tk.Tk()
        self.racine.title("Bubble Shooter")
        self.racine.resizable(height = False, width = False)
        
        self._creer_widgets()


    def _creer_widgets(self):
        """Ajoute l'interface du menu en créant les widgets."""
        
        self.lb_nom = tk.Label(self.racine, text = "\nBUBBLE SHOOTER:", font='Helvetica 18 bold')
        self.lb_nom.pack(side=tk.TOP, fill='x')
        
        self.btn_regles=tk.Button(self.racine, text='Règles du jeu')
        self.btn_regles.pack(side=tk.TOP, fill='x')
        self.btn_regles.bind('<Button-1>', self.affiche_regles_jeu)
        
        self.lb_niveau = tk.Label(self.racine, text = "\nChoisissez le niveau :", font='Helvetica 11 bold')
        self.lb_niveau.pack(side=tk.TOP, fill='x')

        path = pathlib.Path("Niveaux")
        self.btns_niveaux: list[tk.Button] = []
        for niveau in path.glob('*.csv'):
            _, nom = str(niveau).removesuffix(".csv").split("\\")
            btn = tk.Button(self.racine, text=nom)
            btn.pack(side=tk.BOTTOM, anchor=tk.N)
            btn.bind('<Button-1>', self._lancer_jeu)
            self.btns_niveaux.append(btn)


    def _lancer_jeu(self, event: tk.Event):
        self.lancer_jeu(event.widget["text"])
    
    
    def lancer_jeu(self, niveau: str):
        """Crée la fenêtre de jeu et ferme la fenêtre principale."""
        self.racine.destroy()
        jeu = FenetresJeu(niveau)
        jeu.racine.mainloop()


    def affiche_regles_jeu(self, event):
        """Ouvre une message box contenant les règles du jeu."""
        messagebox.showinfo("Règles du jeu ", 
                            "Objectif : \nExplose toutes les billes pour vider ton plateau ! \n "
                            
                            "\n Pour y parvenir, il faut lancer la balle sur les billes du plateau de la même couleur. Si la balle touche un groupe de deux billes de la même couleur ou plus, alors ce groupe éclate."
                            
                            "\n \nCommandes :\n"
                            "À l’aide de ta souris, glisse sur l'endroit où tu veux envoyer la balle. Un tracé de ton lancement apparaitra et t’aidera beaucoup à viser ta cible. Lorsque tu es certain de ton plan de tir, il suffit de cliquer.\n"

                            "Tu peux te servir des parois pour faire rebondir ta balle et parvenir aux endroits les plus inaccessibles.\n"

                            "À chaque bille éclatée, tu gagnes des points. Si tu manques ton coup, ta bulle se collera aux autres et te rajoutera un handicap pour atteindre ton but.\n "

                            "\nSi une des billes touche le bas du plateau, tu perds la partie. En revanche, si tu les élimines toutes, tu gagnes la partie :)\n")  
        
        
if __name__ == "__main__":
    app = FenetresMenu()
    app.racine.mainloop()
