from dataclasses import dataclass, field

from chess_enums import GameMode
from intefaces import IBoard, IBoardAnalyzer

@dataclass(frozen=True)
class ChessGameData:
    game_mode: GameMode
    board: IBoard
    board_analyzer: IBoardAnalyzer
    depth: int = field(default=2)
    play_with_ai: bool = field(default=False)

    def __post_init__(self):
        if (self.depth < 1):
            raise ValueError(
                f"depth of minimax tree can't be less than 1 (give: {self.depth})"
            )
