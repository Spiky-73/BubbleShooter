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

        # initialisation des variables
        self.chrono = 0
        self.score = 0
        self.niveau = niveau

        # chargement du niveau
        if niveau == 'aleatoire': self.cree_niveau_aleatoire(4)
        else: lvl.charge_niveau(niveau, fenetre.grille, fenetre.canon)

        self._creer_widgets()


    def clear(self) -> None:
        """Enlève les paramètres de partie en cours qui s'affichent en bas de l'écran de jeu."""

        self.lb_balle_lances.destroy()
        self.lb_chrono.destroy()
        self.lb_score.destroy()


    def _creer_widgets(self):
        """Ajoute l'interface du jeu et ses données et statistiques"""

        self.lb_chrono = tk.Label(fenetre.racine, text = "", font=theme.police(fenetre.RAYON*1.2))
        self.lb_chrono.pack(side = tk.RIGHT)

        self.lb_balle_lances = tk.Label(fenetre.racine, text = "", font=theme.police(fenetre.RAYON*1.2))
        self.lb_balle_lances.pack(side = tk.LEFT)

        self.lb_score = tk.Label(fenetre.racine, text = "", font=theme.police(fenetre.RAYON*1.2))
        self.lb_score.pack(side=tk.TOP)


    def cree_niveau_aleatoire(self, nb_color):
        """Génère une grille de jeu aléatoirement en respectant un nombre de couleurs de billes."""

        fenetre.canon.couleurs = [i for i in range(nb_color)]
        for y in range(0, 20):
            for x in range(fenetre.grille.dimensions.x-(y-fenetre.grille.grande_ligne)%2):
                fenetre.grille.place(Vector2Int(x, y), theme.billes[random.choice(fenetre.canon.couleurs)])


    def update(self, delta: float) -> None:
        """Actualise le temps total de jeu et le score."""

        self.chrono += delta
        self.lb_chrono.configure(text=f"Temps : {self.chrono:.2f}s")
        self.lb_balle_lances.configure(text=f"Nb de balles :{fenetre.canon.balle_lances}")
        self.lb_score.configure(text=f"Score : {self.score} pts")

        self.test_fin_de_partie()

# 10 + 10 + 10 + 15 + 20 + 25 + 30
# 10 * n + 5 + 10 + 15 + ... + (n-3)*5
# 10 * n + 5*(1+2+3+...+(n-3))
# 10 * n + 5*(n-3)(n-2)/2


    def on_eclatement_bille(self, nb_eclates: int) -> None:
        """Augmente le score. Un grand combo est plus rentable que un petit combo."""
        
        # ajoute les scores des 3 premères billes
        # chaque bille bonus ajoute de plus en plus de score
        self.score += 10*nb_eclates + 5*(nb_eclates-3)*(nb_eclates-2)/2


    def test_fin_de_partie(self): 
        """Arrête le jeu s'il n'y a plus de billes ou que le canon est bloqué."""

        # partie gagnée
        if fenetre.grille.nb_billes == 0:

            # bonus de score en fonction du temps
            if   self.chrono <= 60 :  mult = 1.5
            elif self.chrono <= 120 : mult = 1.2
            elif self.chrono <= 180 : mult = 1.1
            else :                    mult = 1
            self.score = int(self.score*mult)

            # fin du jeu
            fenetre.set_etat("FinDePartie", True, self.score, self.chrono, self.niveau)

        else:
            # partie perdue
            for i in fenetre.grille._grille[fenetre.POSITION_CANNON.y]:
                if i != -1:
                    # fin du jeu
                    fenetre.set_etat("FinDePartie", False, self.score, self.chrono,self.niveau)
                    break

                    
fenetre.ajout_etat(Jeu())