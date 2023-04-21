"""
Executez ce fichier pour jouer au jeu
"""

import pathlib
import tkinter as tk
from tkinter import messagebox
from fenetreJeu import FenetresJeu


class FenetresMenu:
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bubble Shooter")
        self.root.config(width=300, height=700)
        self.root.resizable(height = False, width = False)
        
        self._creer_widgets()

    def _creer_widgets(self):
        """Ajoute l'interface du menu."""
        
        self.select = tk.Label(self.root, text = "\nBUBBLE SHOOTER:", font='Helvetica 18 bold')
        self.select.pack(side=tk.TOP, fill='x')
        
        self.regles=tk.Button(self.root, text='Règles du jeu')
        self.regles.pack(side=tk.TOP, fill='x')
        self.regles.bind('<Button-1>', self.affiche_regles_jeu)
        
        self.select = tk.Label(self.root, text = "\nChoisissez le niveau :", font='Helvetica 11 bold')
        self.select.pack(side=tk.TOP, fill='x')

        path = pathlib.Path("niveaux")
        self.b_niveaux: list[tk.Button] = []
        for niveau in path.glob('*.csv'):
            _, nom = str(niveau).removesuffix(".csv").split("\\")
            btn = tk.Button(self.root, text=nom)
            btn.pack(side=tk.BOTTOM, anchor=tk.N)
            btn.bind('<Button-1>', self._lancer_jeu)
            self.b_niveaux.append(btn)

    def _lancer_jeu(self, event: tk.Event):
        self.lancer_jeu(event.widget["text"])
    
    def lancer_jeu(self, niveau: str):
        """Cree la fenêtre de jeu et ferme la fenêtre principale."""
        self.root.destroy()
        jeu = FenetresJeu(niveau)
        jeu.racine.mainloop()


    def affiche_regles_jeu(self, event):
        """Ouvre une message box contenant les règles du jeu."""
        messagebox.showinfo("Règles du jeu ", "...")  
        
        
if __name__ == "__main__":
    app = FenetresMenu()
    app.root.mainloop()
