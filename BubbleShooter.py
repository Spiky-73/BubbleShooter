"""
Executez ce fichier pour jouer au jeu
"""

import tkinter as tk

class BubbleShooter():
    
    def __init__(self):        
        self.racine = tk.Tk()
        self.racine.title("Fenêtre pour interactions Texte et Graphique...")
        self.racine.config(width=400, height=700)
        self.racine.resizable(height = False, width = False)

        self.canevas = tk.Canvas(self.racine, width=self.racine["width"], height=self.racine["height"])
        self.canevas.pack()
    

if __name__ == "__main__":
    app = BubbleShooter()
    app.racine.mainloop()
