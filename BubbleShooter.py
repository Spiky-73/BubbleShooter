"""
Executez ce fichier pour jouer au jeu
"""

import tkinter as tk
import csv 

class BubbleShooter():
    
    def __init__(self):        
        self.racine = tk.Tk()
        self.racine.title("Fenêtre pour interactions Texte et Graphique...")
        self.racine.config(width=300, height=300)
        self.racine.resizable(height = False, width = False)
        
        self.fen_jeu=tk.Button(self.racine, text='Lancement du jeu')
        self.fen_jeu.pack()
        self.fen_jeu.bind('<Button-1>', self.ouvrir_fen_jeu)
    
        self.fichier='init_jeu.csv'
        self.init_jeu_dico={}
        
        self.fen_jeu=None
        

    def ouvrir_fen_jeu(self,event):
        if self.fen_jeu!=None:
            self.fen_jeu.destroy()
        self.fen_jeu=tk.Toplevel(self.racine)
        self.fen_jeu.width=700
        self.fen_jeu.height=700
        self.fen_jeu.resizable(height = False, width = False)
        
        self.canevas = tk.Canvas(self.fen_jeu, width=500, height=700, bg='lightblue')
        self.canevas.pack()
        
        self.init_jeu()
        
        
    def init_jeu(self):
        rayon=20
        self.lire_init_jeu()
        for x, y, color in self.init_jeu_dico.values():
            self.canevas.create_oval(x,y, x+rayon, y+rayon, fill=color)
            
            
    def lire_init_jeu(self):
        with open(self.fichier, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            dicotemp = {}
            reader_=list(reader)
            for ligne in reader_:
                print(ligne)
                ident, x, y, color = ligne[0], ligne[1], ligne[2], ligne[3]
                if ident not in dicotemp: # si la clef n'existe pas encore
                    dicotemp[ident] = [float(x),float(y), str(color)] # on cree la liste des infos associées
        self.init_jeu_dico = dicotemp
      #  print(self.init_jeu_dico)
        
if __name__ == "__main__":
    app = BubbleShooter()
    app.racine.mainloop()
