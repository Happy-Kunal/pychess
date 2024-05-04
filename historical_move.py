from typing import Type

from dataclasses import dataclass, field
from intefaces import IChessPiece

from move import Move


@dataclass(frozen=True)
class HistoricalMove:
    positions: Move
    moved_piece: Type[IChessPiece]
    killed_piece: Type[IChessPiece] | None = field(default=None)
