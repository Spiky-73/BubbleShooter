import csv
from core.etat import Etat
from core.fenetre import fenetre
import core.gestionnaireDeNiveaux as lvl
from core.gestionnaireDeTheme import theme
from utilitaire import Vector2Int

class Jeu(Etat):

    def init(self, niveau: str) -> None:
        """Charge un niveau"""   
        path = f"niveaux/{niveau}.csv"
    
        # if self.niveau == 'aleatoire':
        #     self.niveau_aleatoire()

        lvl.charge_niveau(niveau, fenetre.grille, fenetre.canon)
        

    # def _creer_widgets(self):
        # """Ajoute l'interface du jeu et ses données/statistiques : score, temps écoulé, nombre de billes éclatées..."""

        # self.timer = tk.Label(self.racine, text = "\nTemps écoulé ", font = 'Helvetica 11 bold') # affichage des statistiques
        # self.timer.pack(side=tk.RIGHT, fill='x')

        # self.nbr_billes_eclatees = tk.Label(self.racine, text = "\nNombre de billes éclatées ", font = 'Helvetica 11 bold')
        # self.nbr_billes_eclatees.pack(side=tk.RIGHT, fill='x')

        # self.score = tk.Label(self.racine, text = "\nScore ", font = 'Helvetica 11 bold')
        # self.score.pack(side=tk.RIGHT, fill='x')



    # def niveau_aleatoire(self, nb_color):
    #     """Génère une grille de jeu aléatoirement en respectant un nombre de couleurs de billes."""

    #     liste_ligne=[]
    #     import csv
    #     with open(self.fichier, encoding='utf-8') as fichiercsv: # lecture du fichier csv
    #         writer=csv.writer(fichiercsv)
    #         for i in range (19):
    #             for j in range(25):
    #                 nb=random.randint(0, len(self.index_couleurs))
    #                 liste_ligne.append(nb)
    #             writer.writerow(liste_ligne)

    def update(self, delta: float) -> None:
        pass

#    def _update_score(self):
#        """Actualise le temps total de jeu et le score. Calcule le score du joueur."""
#
#        # à appeler à chaque lancer
#        score = 0
#        if eclate == True : # rajouter un booleen dans la fonction test_eclate_groupe : on incrémente le score à partir du moment où le lancer éclate des billes
#            groupe = self.get_groupe(bille) + self.eclate_billes_detaches() # le nombre de billes éclatées = celles du groupe éclaté + celles qui étaient en dessous et qui tombent aussi car non connectées
#            if groupe == 3 : # nombre minimal pour éclater
#                score += 3
#            elif groupe > 3 and < 10 :
#                score += groupe * 1.2 # bonus : plus on éclate un grand groupe, plus on obtient de points : 1 point par bille éclatée + un coefficient bonus car grande chaîne formée
#            elif groupe >= 10 and < 15 :
#                score += groupe * 1.4
#            elif groupe >= 15 and < 20 :
#                score += groupe * 1.6
#            else :
#                score = score + groupe*2
#        
#        if fin_de_partie == True : # booléen dans test_fin_de_partie
#            if chrono > 180 : # à modifier quand on aura fait la fonction du chrono, si le joueur met plus de 3 minutes pour terminer le niveau (chrono affiché en fin de partie)
#                score = score # pas de bonus de rapidité
#            elif chrono > 120 and chrono <= 180 : # s'il met entre 2 et 3 minutes
#                score = score * 1.1 # léger bonus de rapidité
#            elif chrono >= 40 and chrono <= 120 :
#                score = score * 1.2
#            else : 
#                score = score * 1.5
#            
#        score = score * 10 # pour éviter d'avoir des tout petits scores
#        return score
#
#        # est-ce qu'on affiche le score à chaque lancer en bas ?
    
# def test_fin_de_partie(self) -> bool: 
#     """Arrête le jeu (sortir de la fonction update) s'il n'y a plus de billes et affiche le score dans une messagebox."""
#     pass
