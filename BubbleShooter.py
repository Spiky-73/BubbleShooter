"""
Executez ce fichier pour jouer au jeu
"""

import tkinter

class BubbleShooter():
    
    def __init__(self):        
        self.racine = tkinter.Tk()
        self.racine.title("Fenêtre pour interactions Texte et Graphique")
        self.racine.config(width=300, height=700)
        self.racine.resizable(height = False, width = False)

        self.canevas = tkinter.Canvas(self.racine, width=self.racine["width"], height=self.racine["height"])
        self.canevas.pack()

    
if __name__ == "__main__":
    app = BubbleShooter()
    app.racine.mainloop()
