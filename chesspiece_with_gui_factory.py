from typing import override

from factory import AbstractChessPieceFactory
from chesspiece import ChessPiece
from move_strategy import PawnMoveStrategy, KinghtMoveStrategy, BishopMoveStrategy, RookMoveStrategy, KingMoveStrategy
from chess_enums import ChessPieceColor, GameMode
from intefaces import IChessPiece

import pygame


assets = dict()

assets[(ChessPieceColor.WHITE, "pawn")] = pygame.transform.scale(pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/w_pawn_png_shadow_128px.png'), (75, 75))
assets[(ChessPieceColor.WHITE, "rook")] = pygame.transform.scale(pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/w_rook_png_shadow_128px.png'), (75, 75))
assets[(ChessPieceColor.WHITE, "bishop")] = pygame.transform.scale(pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/w_bishop_png_shadow_128px.png'), (75, 75))
assets[(ChessPieceColor.WHITE, "knight")] = pygame.transform.scale(pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/w_knight_png_shadow_128px.png'), (75, 75))
assets[(ChessPieceColor.WHITE, "king")] = pygame.transform.scale(pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/w_king_png_shadow_128px.png'), (75, 75))
assets[(ChessPieceColor.WHITE, "queen")] = pygame.transform.scale(pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/w_queen_png_shadow_128px.png'), (75, 75))

assets[(ChessPieceColor.BLACK, "pawn")] = pygame.transform.scale(pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/b_pawn_png_shadow_128px.png'), (75, 75))
assets[(ChessPieceColor.BLACK, "rook")] = pygame.transform.scale(pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/b_rook_png_shadow_128px.png'), (75, 75))
assets[(ChessPieceColor.BLACK, "bishop")] = pygame.transform.scale(pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/b_bishop_png_shadow_128px.png'), (75, 75))
assets[(ChessPieceColor.BLACK, "knight")] = pygame.transform.scale(pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/b_knight_png_shadow_128px.png'), (75, 75))
assets[(ChessPieceColor.BLACK, "king")] = pygame.transform.scale(pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/b_king_png_shadow_128px.png'), (75, 75))
assets[(ChessPieceColor.BLACK, "queen")] = pygame.transform.scale(pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/b_queen_png_shadow_128px.png'), (75, 75))


class ChessPieceWithGUIFactory(AbstractChessPieceFactory):
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
            move_strategies=[self.pawn_strategy],
            image=assets[(color, "pawn")]
        )
    
    @override
    def create_knight(self, color: ChessPieceColor, row: int, col: int) -> IChessPiece:
        return ChessPiece(
            color=color,
            row=row,
            col=col,
            points=3,
            is_king_piece=False,
            move_strategies=[self.knight_strategy],
            image=assets[(color, "knight")]
        )
    
    @override
    def create_bishop(self, color: ChessPieceColor, row: int, col: int) -> IChessPiece:
        return ChessPiece(
            color=color,
            row=row,
            col=col,
            points=3,
            is_king_piece=False,
            move_strategies=[self.bishop_strategy],
            image=assets[(color, "bishop")]
        )
    
    @override
    def create_rook(self, color: ChessPieceColor, row: int, col: int) -> IChessPiece:
        return ChessPiece(
            color=color,
            row=row,
            col=col,
            points=5,
            is_king_piece=False,
            move_strategies=[self.rook_strategy],
            image=assets[(color, "rook")]
        )
    
    @override
    def create_queen(self, color: ChessPieceColor, row: int, col: int) -> IChessPiece:
        return ChessPiece(
            color=color,
            row=row,
            col=col,
            points=9,
            is_king_piece=False,
            move_strategies=[self.rook_strategy, self.bishop_strategy],
            image=assets[(color, "queen")]
        )
    
    @override
    def create_king(self, color: ChessPieceColor, row: int, col: int) -> IChessPiece:
        return ChessPiece(
            color=color,
            row=row,
            col=col,
            points=100,
            is_king_piece=True,
            move_strategies=[self.king_strategy],
            image=assets[(color, "king")]
        )


