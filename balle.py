import dataclasses
import utilitaire

RAYON = 30

@dataclasses.dataclass
class Balle:
    position: utilitaire.Vector2
    vitesse: utilitaire.Vector2
    couleur: str
    