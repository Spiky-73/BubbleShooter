import dataclasses
import utilitaire

@dataclasses.dataclass
class Balle:
    position: utilitaire.Vector2
    vitesse: utilitaire.Vector2
    couleur: str
    