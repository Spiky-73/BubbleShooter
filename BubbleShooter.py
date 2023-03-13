"""
Executez ce fichier pour jouer au jeu !
"""

import tkinter as tk

class BubbleShooter():
    
    def __init__(self):        
        self.racine = tk.Tk()
        self.racine.title("Fenêtre pour interactions Texte et Graphique...")
        self.racine.config(width=300, height=300)
        self.racine.resizable(height = False, width = False)
        
        self.fen_jeu=tk.Button(self.racine, text='Lancement du jeu')
        self.fen_jeu.pack()
        self.fen_jeu.bind('<Button-1>', self.ouvrir_fen_jeu)
    
    def ouvrir_fen_jeu(self,event):
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
