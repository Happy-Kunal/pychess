from abc import ABC, abstractmethod
from typing import override

from chess_enums import ChessPieceColor, GameMode
from chesspiece import ChessPiece
from intefaces import IChessPiece
from move_strategy import PawnMoveStrategy, KinghtMoveStrategy, BishopMoveStrategy, RookMoveStrategy, KingMoveStrategy

class AbstractChessPieceFactory(ABC):
    def __init__(self, game_mode: GameMode) -> None:
        self.game_mode = game_mode
    

    @abstractmethod
    def create_pawn(self, color: ChessPieceColor, row: int, col: int) -> IChessPiece:...

    @abstractmethod
    def create_knight(self, color: ChessPieceColor, row: int, col: int) -> IChessPiece:...

    @abstractmethod
    def create_bishop(self, color: ChessPieceColor, row: int, col: int) -> IChessPiece:...

    @abstractmethod
    def create_rook(self, color: ChessPieceColor, row: int, col: int) -> IChessPiece:...

    @abstractmethod
    def create_queen(self, color: ChessPieceColor, row: int, col: int) -> IChessPiece:...

    @abstractmethod
    def create_king(self, color: ChessPieceColor, row: int, col: int) -> IChessPiece:...


class SimpleChessPieceFactory(AbstractChessPieceFactory):
    def __init__(self, game_mode: GameMode) -> None:
        super().__init__(game_mode)
        self.pawn_strategy = PawnMoveStrategy(game_mode=self.game_mode)
        self.knight_strategy = KinghtMoveStrategy()
        self.bishop_strategy = BishopMoveStrategy()
        self.rook_strategy = RookMoveStrategy()
        self.king_strategy = KingMoveStrategy()

    @override
    def create_pawn(self, color: ChessPieceColor, row: int, col: int) -> IChessPiece:
        return ChessPiece(
            color=color,
            row=row,
            col=col,
            points=1,
            is_king_piece=False,
            move_strategies=[self.pawn_strategy]
        )
    
    @override
    def create_knight(self, color: ChessPieceColor, row: int, col: int) -> IChessPiece:
        return ChessPiece(
            color=color,
            row=row,
            col=col,
            points=3,
            is_king_piece=False,
            move_strategies=[self.knight_strategy]
        )
    
    @override
    def create_bishop(self, color: ChessPieceColor, row: int, col: int) -> IChessPiece:
        return ChessPiece(
            color=color,
            row=row,
            col=col,
            points=3,
            is_king_piece=False,
            move_strategies=[self.bishop_strategy]
        )
    
    @override
    def create_rook(self, color: ChessPieceColor, row: int, col: int) -> IChessPiece:
        return ChessPiece(
            color=color,
            row=row,
            col=col,
            points=5,
            is_king_piece=False,
            move_strategies=[self.rook_strategy]
        )
    
    @override
    def create_queen(self, color: ChessPieceColor, row: int, col: int) -> IChessPiece:
        return ChessPiece(
            color=color,
            row=row,
            col=col,
            points=9,
            is_king_piece=False,
            move_strategies=[self.rook_strategy, self.bishop_strategy]
        )
    
    @override
    def create_king(self, color: ChessPieceColor, row: int, col: int) -> IChessPiece:
        return ChessPiece(
            color=color,
            row=row,
            col=col,
            points=100,
            is_king_piece=True,
            move_strategies=[self.king_strategy]
        )

def normal_chess_board_pieces_factory(chess_piece_factory: AbstractChessPieceFactory) -> list[IChessPiece]:
    pieces: list[IChessPiece] = list()

    pieces.extend([chess_piece_factory.create_pawn(ChessPieceColor.WHITE, 1, j) for j in range(8)])
    pieces.extend([chess_piece_factory.create_pawn(ChessPieceColor.BLACK, 6, j) for j in range(8)])
    
    rook_knight_bishop_creaters = (
        chess_piece_factory.create_rook,
        chess_piece_factory.create_knight,
        chess_piece_factory.create_bishop
    )
    for color in ChessPieceColor:
        row = 0 if color is ChessPieceColor.WHITE else 7
        for (leftcol, create_piece) in enumerate(rook_knight_bishop_creaters):
            pieces.append(create_piece(color, row, leftcol))
            pieces.append(create_piece(color, row, 7 - leftcol))

        pieces.append(chess_piece_factory.create_king(color, row, 4))
        pieces.append(chess_piece_factory.create_queen(color, row, 3))
    
    return pieces
