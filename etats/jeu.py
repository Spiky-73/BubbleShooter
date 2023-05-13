import tkinter as tk
import random
from core.etat import Etat
from core.fenetre import fenetre
import core.gestionnaireDeNiveaux as lvl
from core.gestionnaireDeTheme import theme
from utilitaire import Vector2Int

class Jeu(Etat):

    def init(self, niveau: str) -> None:
        """Charge un niveau."""

        if niveau == 'aleatoire':
            self.niveau_aleatoire(4)
        else:
            lvl.charge_niveau(niveau, fenetre.grille, fenetre.canon)
        self._creer_widgets()

        self.chrono = 0
        self.score = 0
        self.niveau = niveau


    def clear(self) -> None:
        """Enlève les paramètres de partie en cours qui s'affichent en bas de l'écran de jeu, les remet à zéro."""

        self.lb_balle_lances.destroy()
        self.lb_chrono.destroy()
        self.lb_score.destroy()


    def _creer_widgets(self):
        """Ajoute l'interface du jeu et ses données/statistiques : score, temps écoulé, nombre de billes éclatées..."""

        self.lb_chrono = tk.Label(fenetre.racine, text = "", font=theme.police(fenetre.RAYON*1.2)) # affichage des statistiques
        self.lb_chrono.pack(side=tk.RIGHT)

        self.lb_balle_lances = tk.Label(fenetre.racine, text = "", font=theme.police(fenetre.RAYON*1.2))
        self.lb_balle_lances.pack(side=tk.LEFT)

        self.lb_score = tk.Label(fenetre.racine, text = "", font=theme.police(fenetre.RAYON*1.2))
        self.lb_score.pack(side=tk.TOP)


    def niveau_aleatoire(self, nb_color):
        """Génère une grille de jeu aléatoirement en respectant un nombre de couleurs de billes."""

        fenetre.canon.couleurs = [i for i in range(nb_color)]
        for y in range(0, 20):
            for x in range(fenetre.grille.dimensions.x-(y-fenetre.grille.grande_ligne)%2):
                fenetre.grille.place(Vector2Int(x, y), theme.billes[random.choice(fenetre.canon.couleurs)])


    def update(self, delta: float) -> None:
        """Actualise le temps total de jeu et le score. Calcule le score du joueur."""

        self.chrono += delta
        self.lb_chrono.configure(text=f"Temps: {self.chrono:.2f}s")
        self.lb_balle_lances.configure(text=f"Nb de balles:{fenetre.canon.balle_lances}")
        self.lb_score.configure(text=f"Score: {self.score} pts")

        self.test_fin_de_partie()

    
    def on_eclatement_bille(self, nb_eclates: int) -> None:
        """Pour le calcul du score, bonus de points si un grand groupe de billes est éclaté."""

        combo = 10
        nb_eclates -= 3 
        self.score += 3*combo # score = score + nombre de billes éclatées x combo

        for _ in range(nb_eclates):
            combo += 5
            self.score += combo


    def test_fin_de_partie(self): 
        """Arrête le jeu (sortir de la fonction update) s'il n'y a plus de billes et affiche le score dans une messagebox."""

        if fenetre.grille.compte_billes == 0:
           
            mult = 1
            if self.chrono < 40:     mult = 1.5 # bonus 
            elif self.chrono <= 120 : mult = 1.2
            elif self.chrono <= 180 : mult = 1.1 # léger bonus de rapidité si on met entre 2 et 3 minutes pour finir le jeu
            else : mult = 1 # si le joueur met plus de 3 minutes pour terminer le niveau (chrono affiché en fin de partie), pas de bonus de rapidité
            self.score = int(self.score*mult)
            fenetre.set_etat("FinDePartie", True, self.score, self.chrono, self.niveau)

        else:
            for i in fenetre.grille._grille[fenetre.POSITION_CANNON.y]:
                if i != -1:
                    fenetre.set_etat("FinDePartie", False, self.score, self.chrono,self.niveau)
                    break

                    
fenetre.ajout_etat(Jeu())