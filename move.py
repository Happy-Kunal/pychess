from dataclasses import dataclass

@dataclass(frozen=True)
class Move:
    x1: int
    y1: int
    x2: int
    y2: int
    