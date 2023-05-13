
class Etat:
    """
    Classe destinée a être dérivée.
    Représente un état du jeu.
    Utilisez `from core.fenetre import fenetre` pour avoir accès a la grille, au canon ou au variables globales
    Ajoutez `fenetre.ajout_etat(<Etat>())` a d'un état et importez ce fichier dans le fichier principal pour pouvoir l'utiliser. 
    """

    def init(self, *args) -> None:
        """Initialise l'état suite à un changement d'etat sur la feneètre avec les arguments données lors du changement"""
        pass
    
    def clear(self) -> None:
        """Efface tout l'interface ajouté par l'état"""
        pass

    
    def update(self, delta: float) -> None:
        """Actualise l'etat. Est appelle en continue"""
        pass

    def on_eclatement_bille(self, nb_eclates: int) -> None:
        """Appellé lors de l'éclatement d'un groupe de bille"""
        pass