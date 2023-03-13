"""
Executez ce fichier pour jouer au jeu
"""

import tkinter as tk

class BubbleShooter():
    
    def __init__(self):        
        self.racine = tk.Tk()
        self.racine.title("Fenêtre pour interactions Texte et Graphique...")
        self.racine.config(width=450, height=700)
        self.racine.resizable(height = False, width = False)

        self.canevas = tk.Canvas(self.racine, width=self.racine["width"], height=self.racine["height"])
        self.canevas.pack()
    
    def creer_widgets(self,root):
        self.fen_graphique = None
    
    def trajectoire_balle(self,event):
        
        """ Trajectoire = droite entre la position de la souris au moment où on clique et la position du 
        canon à billes en bas de l'écran. """
        
        mouseX = event.x # on récupère la position de la souris
        mouseY = event.y
        x = self.fen_graphique.canevas.canvasx(mouseX)
        y = self.fen_graphique.canevas.canvasy(mouseY)
        print(f"")
        

if __name__ == "__main__":
    app = BubbleShooter()
    app.racine.mainloop()
