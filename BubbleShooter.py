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
