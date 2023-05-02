import tkinter as tk
import random
from core.etat import Etat
from core.fenetre import fenetre
import core.gestionnaireDeNiveaux as lvl
from core.gestionnaireDeTheme import theme
from utilitaire import Vector2Int
from .finDePartie import FinDePartie


class Jeu(Etat):

    def init(self, niveau: str) -> None:
        """Charge un niveau"""   
        if niveau == 'aleatoire':
            self.niveau_aleatoire(4)
        else:
            lvl.charge_niveau(niveau, fenetre.grille, fenetre.canon)
        self._creer_widgets()

        self.chrono = 0
        self.score = 0

    def _creer_widgets(self):
        """Ajoute l'interface du jeu et ses données/statistiques : score, temps écoulé, nombre de billes éclatées..."""

        self.lb_chrono = tk.Label(fenetre.racine, text = "Temps écoulé ", font = 'Helvetica 11 bold') # affichage des statistiques
        self.lb_chrono.pack(side=tk.RIGHT)

        self.lb_balle_lances = tk.Label(fenetre.racine, text = "Nb de balles: ", font = 'Helvetica 11 bold')
        self.lb_balle_lances.pack(side=tk.LEFT)

        self.lb_score = tk.Label(fenetre.racine, text = "\nScore ", font = 'Helvetica 11 bold')
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
        self.lb_chrono.configure(text=f"Temps écoulé {self.chrono:.2f}s")
        self.lb_balle_lances.configure(text=f"Nb de balles:{fenetre.canon.balle_lances}")
        self.lb_score.configure(text=f"Score: {self.score} pts")

        self.test_fin_de_partie()
        # # à appeler à chaque lancer
        # score = 0
        # if eclate == True : # rajouter un booleen dans la fonction test_eclate_groupe : on incrémente le score à partir du moment où le lancer éclate des billes
        #     groupe = self.get_groupe(bille) + self.eclate_billes_detaches() # le nombre de billes éclatées = celles du groupe éclaté + celles qui étaient en dessous et qui tombent aussi car non connectées
        #     if groupe == 3 : # nombre minimal pour éclater
        #         score += 3
        #     elif groupe > 3 and < 10 :
        #         score += groupe * 1.2 # bonus : plus on éclate un grand groupe, plus on obtient de points : 1 point par bille éclatée + un coefficient bonus car grande chaîne formée
        #     elif groupe >= 10 and < 15 :
        #         score += groupe * 1.4
        #     elif groupe >= 15 and < 20 :
        #         score += groupe * 1.6
        #     else :
        #         score = score + groupe*2
        
        # score = score * 10 # pour éviter d'avoir des tout petits scores
        # return score

       # est-ce qu'on affiche le score à chaque lancer en bas ?
    
    def test_fin_de_partie(self): 
        """Arrête le jeu (sortir de la fonction update) s'il n'y a plus de billes et affiche le score dans une messagebox."""
        if fenetre.grille.compte_billes == 0:
            mult = 1
            if self.chrono < 40:     mult = 1.5 # bonus 
            elif self.chrono <= 120 : mult = 1.2
            elif self.chrono <= 180 : mult = 1.1 # léger bonus de rapidité si on met entre 2 et 3 minutes pour finir le jeu
            else : mult = 1 # si le joueur met plus de 3 minutes pour terminer le niveau (chrono affiché en fin de partie), pas de bonus de rapidité
            self.score *= mult
            fenetre.set_scipt(FinDePartie(), self.score, self.chrono)
