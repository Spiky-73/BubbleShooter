
"""
Executez ce fichier pour jouer au jeu
"""

import tkinter as tk

class BubbleShooter():
    
    def __init__(self):        
        self.racine = tk.Tk()
        self.racine.title("Fenêtre principale du jeu")
        self.racine.config(width=300, height=300)
        self.racine.resizable(height = False, width = False)
        
        self.fen_jeu=tk.Button(self.racine, text='Lancement du jeu')
        self.fen_jeu.pack()
        self.fen_jeu.bind('<Button-1>', self.ouvrir_fen_jeu)
        
        self.dx = -1 # pour le déplacement de la bille
        self.dy = 1
    
    def creer_widgets(self,root):
        self.fen_graphique = None
    
    def trajectoire_balle(self,event):
        
        """ Trajectoire = droite entre la position de la souris au moment où on clique et la position du 
        canon à billes en bas de l'écran. """
        
       
            
    def ouvrir_fen_jeu(self,event):
        
        """ Création de la fenêtre de jeu. """
        if self.fen_jeu!=None:
            self.fen_jeu.destroy()
        self.fen_jeu=tk.Toplevel(self.racine)
        self.fen_jeu.width=700
        self.fen_jeu.height=700
        self.fen_jeu.resizable(height = False, width = False)
        
        self.canevas = tk.Canvas(self.fen_jeu, width=500, height=700, bg='lightblue')
        self.canevas.pack()
        

if __name__ == "__main__":
    app = BubbleShooter()
    app.racine.mainloop()

"""
Executez ce fichier pour jouer au jeu
"""
import tkinter

class FenetresMenu:
    def __init__(self) -> None:
        self.root = tkinter.Tk()
        self.root.title("Bubble Shoter")
        self.root.config(width=300, height=300)
        self.root.resizable(height = False, width = False)
        self.fichier='init_jeu.csv'
        self.init_jeu_dico={}
        self._creer_widgets()

    def _creer_widgets(self) -> None:
        """Ajoute l'interface du menu."""
        self.fen_jeu=tkinter.Button(self.root, text='Lancement du jeu')
        self.fen_jeu.place(x=50, y=0)
        self.fen_jeu.bind('<Button-1>', self.lancer_jeu)
        pass

    def lancer_jeu(self, event: tkinter.Event) -> None:
        """Cree la fenêtre de jeu et ferme la fenêtre principale."""

    def affiche_regles_jeu(self, event: tkinter.Event) -> None:
        """Ouvre une message box contenant les règles du jeu."""

if __name__ == "__main__":
    app = FenetresMenu()
    app.mainloop()

