import dataclasses
import utilitaire

@dataclasses.dataclass
class Balle:
    centre: utilitaire.Vector2
    rayon: int
    vitesse: utilitaire.Vector2
    couleur: str
    id: int

    @property
    def coin_NW(self) -> utilitaire.Vector2:
        """ Définit le coin en haut à gauche de la balle."""

        return self.centre - utilitaire.Vector2(self.rayon, self.rayon)
    

    @property
    def coin_SE(self) -> utilitaire.Vector2:
        """Définit le coin en bas à droite de la balle."""

        return self.centre + utilitaire.Vector2(self.rayon, self.rayon)
    