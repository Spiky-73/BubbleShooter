import dataclasses
import tkinter
import utilitaire

RAYON = 10

@dataclasses.dataclass
class Balle:
    position: utilitaire.Vector2
    vitesse: utilitaire.Vector2
    couleur: str
    id: int
    