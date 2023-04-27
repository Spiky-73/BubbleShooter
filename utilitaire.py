import dataclasses
from typing import Iterator

@dataclasses.dataclass
class Vector2:
    x: float
    y: float

    @property
    def norme(self) -> float:
        return (self.x**2 + self.y**2)**0.5

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self + other*-1

    def __mul__(self, mul: float):
        return Vector2(self.x * mul, self.y * mul)

    def __truediv__(self, div: float):
        return self * (1/div)

    def distance(self, other) -> float:
        return (self-other).norme
    
    def __iter__(self) -> Iterator[float]:
        return iter(dataclasses.astuple(self))


@dataclasses.dataclass(unsafe_hash=True)
class Vector2Int:
    x: int
    y: int

    @property
    def norme(self) -> float:
        return (self.x**2 + self.y**2)**0.5

    def __add__(self, other):
        return Vector2Int(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self + other*-1

    def __mul__(self, mul: float):
        return Vector2Int(int(self.x * mul), int(self.y * mul))

    def __truediv__(self, div: float):
        return self * (1/div)

    def distance(self, other) -> float:
        return (self-other).norme
    
    def __iter__(self) -> Iterator[float]:
        return iter(dataclasses.astuple(self))
