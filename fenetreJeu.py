import balle

class FenetresJeu:
    def __init__(self, niveau: str) -> None:
        """initialise la fenêtre de jeu avec le niveau choisi."""

    def _init_niveau(self) -> None:
        """lecture et chargement du niveau."""

    def _creer_widgets(self) -> None:
        """Ajoute l'interface du jeu."""


    def update(self) -> None:
        """
        Appelée plusieurs fois par seconde.
        Appellere toutes les fonctions liées au mouvement de la balle (timer) et du jeu.
        """
    
    def _update_souris(self) -> None:
        """Récupère la position de la souris."""

    def _update_trajectoire(self) -> None:
        """Simule la trajectoire de la balle et l'affiche pour guider le joueur."""

    def _update_balle(self) -> None:
        """Controlle le déplacement de la balle."""


    def deplacer_balle(self, balle: balle.Balle, dt: float) -> None:
        """Deplace une balle sur dt secondes et prends en compte les collisions."""

    def collision_bille(self, balle: balle.Balle) -> int|None:
        """Renvoie l'id de la bille touchée ou None si la balle ne touche pas de bille."""

    # ? changer la fonction pour qu'elle retourne tous les voisins de la même couleure et faire le test du nombre dans une autre fonction ou lors de la collision de la balle
    def recherche_voisins(self, balle: balle.Balle, nombre: int = 3) -> bool:
        """
        Renvoie `True` s'il y a plus de `nombre` billes adjacentes de la même couleur a `balle`.
        Stocke les coordonnées de la balle qui reste alors sur le caneva si ce n'est pas la cas.
        """

    def eclate_billes_adjacentes(self,  balle: balle.Balle) : 
        """Eclates toutes les billes adjacentes de la même couleur que la balle."""

    def _eclate_bille(self, bille: int):
        """Eclate une bille."""

    def test_fin_de_partie (self) -> bool: 
        """Arrête le jeu (sortir de la fonction update) si il n'y a plus de billes et affiche le score dans une messagebox."""