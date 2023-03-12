"""
Executez ce fichier pour jouer au jeu
"""

import tkinter

class BubbleShooter():
    
    def __init__(self):        
        self.racine = tkinter.Tk()
        self.racine.title("Fenêtre pour interactions Texte et Graphique")
        self.racine.resizable(height = False, width = False)

    
if __name__ == "__main__":
    app = BubbleShooter()
    app.racine.mainloop()
