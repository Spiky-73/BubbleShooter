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
        
        mouseX = event.x # on récupère la position de la souris
        mouseY = event.y
        x = self.fen_graphique.canevas.canvasx(mouseX)
        y = self.fen_graphique.canevas.canvasy(mouseY)

        if self.x < 0 : # si la bille sort de la fenêtre
            self.x = 0
            self.dx = -self.dx # elle rebondit contre le mur
        if self.y < 0 : # on fait pour toutes les directions
            self.y = 0
            self.dy = -self.dy
            
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
