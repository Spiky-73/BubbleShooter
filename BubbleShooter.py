"""
Executez ce fichier pour jouer au jeu
"""
import tkinter as tk
from tkinter import messagebox
from fenetreJeu import FenetresJeu
class FenetresMenu:
    
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Bubble Shooter")
        self.root.config(width=300, height=700)
        self.root.resizable(height = False, width = False)
        
        self.f_graph=None
        self.f_graph_width=500
        self.f_graph_height=700
        
        self.fichier='init_jeu.csv'
        self.init_jeu_dico={}
        self._creer_widgets()

    def _creer_widgets(self) -> None:
        """Ajoute l'interface du menu."""
        
        self.select = tk.Label(self.root, text = "\nBUBBLE SHOOTER:", font='Helvetica 18 bold')
        self.select.pack(side=tk.TOP, fill='x')
        
        self.regles=tk.Button(self.root, text='Règles du jeu')
        self.regles.pack(side=tk.TOP, fill='x')
        self.regles.bind('<Button-1>', self.affiche_regles_jeu)
        
        self.select = tk.Label(self.root, text = "\nChoisissez le niveau :", font='Helvetica 11 bold')
        self.select.pack(side=tk.TOP, fill='x')
        
        self.fen_jeu_f=tk.Button(self.root, text='Facile')
        self.fen_jeu_f.pack(side=tk.BOTTOM, anchor=tk.E)
        self.fen_jeu_f.bind('<Button-1>', self.lancer_jeu_f)
        
        
        self.fen_jeu_m=tk.Button(self.root, text='Moyen')
        self.fen_jeu_m.pack(side=tk.BOTTOM, anchor=tk.E)
        self.fen_jeu_m.bind('<Button-1>', self.lancer_jeu_m)
        
        self.fen_jeu_d=tk.Button(self.root, text='Difficile')
        self.fen_jeu_d.pack(side=tk.BOTTOM, anchor=tk.E)
        self.fen_jeu_d.bind('<Button-1>', self.lancer_jeu_d)
        
        
    def lancer_jeu_f(self, event) -> None:
        """Cree la fenêtre de jeu et ferme la fenêtre principale."""
        fen = FenetresJeu(self.root, "facile")
        fen.racine.mainloop()
        
        
    def lancer_jeu_m(self, event) -> None:
        """Cree la fenêtre de jeu et ferme la fenêtre principale."""
        fen = FenetresJeu(self.root,"moyen")
        fen.racine.mainloop()
    def lancer_jeu_d(self, event) -> None:
        """Cree la fenêtre de jeu et ferme la fenêtre principale."""
        fen = FenetresJeu(self.root,"difficile")
        fen.racine.mainloop()
        
    def affiche_regles_jeu(self, event) -> None:
        """Ouvre une message box contenant les règles du jeu."""
        
        messagebox.showinfo("Règles du jeu ", "...")  
        
        
if __name__ == "__main__":
    app = FenetresMenu()
    app.root.mainloop()
