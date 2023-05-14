
class Etat:
    """
    Classe destinée à être dérivée.
    Représente un état du jeu.
    Utilisez `from core.fenetre import fenetre` pour avoir accès à la grille, au canon ou au variables globales.
    Ajoutez `fenetre.ajout_etat(<Etat>())` d'un état et importez ce fichier dans le fichier principal pour pouvoir l'utiliser. 
    """

    def init(self, *args) -> None:
        """Initialise l'état suite à un changement d'état sur la fenêtre avec les arguments données lors du changement."""

        pass

    
    def clear(self) -> None:
        """Efface toute l'interface ajoutée par l'état."""
        
        pass

    
    def update(self, delta: float) -> None:
        """Actualise l'état. Est appellée en continu."""

        pass


    def on_eclatement_bille(self, nb_eclates: int) -> None:
        """Appellée lors de l'éclatement d'un groupe de billes."""

        pass