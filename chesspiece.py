from typing import Type

from pygame import SurfaceType

from chess_enums import ChessPieceColor
from move_strategy import ChessPieceMoveStrategy
from historical_move import Move
from intefaces import IBoard, IBoardAnalyzer

class ChessPiece:
    def __init__(
        self,
        color: ChessPieceColor,
        row: int,
        col: int,
        points: int,
        is_king_piece: bool,
        move_strategies: list[Type[ChessPieceMoveStrategy]],
        image: SurfaceType | None = None # for gui support @decided not to go with decorator pattern,
    ):
        self.row = row
        self.col = col
        self.color = color
        self.points = points
        self.is_king_piece = is_king_piece
        self.move_strategies = move_strategies.copy()
        self.image = image
    
    def get_row(self) -> int:
        return self.row
    
    def get_col(self) -> int:
        return self.col
    
    def get_color(self) -> ChessPieceColor:
        return self.color
    
    def get_points(self) -> int:
        return self.points
    
    def is_king(self):
        return self.is_king_piece
    
    def set_position(self, row: int, col: int):
        self.row = row
        self.col = col

    
    def get_moves(self, board: IBoard, board_analyzer: IBoardAnalyzer) -> set[Move]:
        moves: set[Move] = set()
        for strategy in self.move_strategies:
            moves = moves.union(strategy.get_moves(row=self.row, col=self.col, board=board, board_analyzer=board_analyzer))
        
        return moves
    
    def get_image(self) -> SurfaceType | None:
        return self.image

