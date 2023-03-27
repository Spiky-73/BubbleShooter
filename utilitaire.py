from typing import NamedTuple

class Vector2(NamedTuple):
    x: float
    y: float

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)