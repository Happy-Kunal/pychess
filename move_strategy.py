from typing import override, Type
from abc import ABC, abstractmethod
import operator
import itertools

from move import Move
from intefaces import IBoard, IBoardAnalyzer
from chess_enums import ChessPieceColor, GameMode

class ChessPieceMoveStrategy(ABC):
    @abstractmethod
    def get_moves(self, row: int, col: int, board: IBoard, board_analyzer: IBoardAnalyzer) -> set[Move]:...


class PawnMoveStrategy(ChessPieceMoveStrategy):
    def __init__(self, game_mode: GameMode) -> None:
        self.game_mode = game_mode

    @override
    def get_moves(self, row: int, col: int, board: IBoard, board_analyzer: IBoardAnalyzer) -> set[Move]:
        curr_piece = board.get_piece_at(row, col)

        moves = set()
        if self.game_mode is GameMode.WHITE_DOWN and curr_piece.color is ChessPieceColor.WHITE or self.game_mode is GameMode.BLACK_DOWN and curr_piece.color is ChessPieceColor.BLACK:
            direction = 1
        else:
            direction = -1
        
        x = row + direction
        y = col

        if (
            board.is_valid_position(x, y)
            and board.get_piece_at(x, y) is None
        ):
            moves.add(Move(row, col, x, y))
            if (
                min(row, 7 - row) == 1
                and board.is_valid_position(x + direction, y)
                and board.get_piece_at(x + direction, y) is None
            ):
                moves.add(Move(row, col, x + direction, y))

        curr_piece = board.get_piece_at(row, col)
        for y_diagonal in (y - 1, y + 1):
            if (
                board.is_valid_position(x, y_diagonal)
                and (other_piece := board.get_piece_at(x, y_diagonal)) is not None
                and board_analyzer.are_opponents(curr_piece, other_piece)
            ):
                moves.add(Move(row, col, x, y_diagonal))

        return moves

class KinghtMoveStrategy(ChessPieceMoveStrategy):
    @override
    def get_moves(self, row: int, col: int, board: IBoard, board_analyzer: IBoardAnalyzer) -> set[Move]:
        curr_piece = board.get_piece_at(row, col)
        moves = set()
        add = operator.add
        sub = operator.sub
        op_list = [(add, sub), (sub, add), (add, add), (sub, sub)]
        delta = [(1, 2), (2, 1)]
        for comb in itertools.product(op_list, delta):
            x = comb[0][0](row, comb[1][0])
            y = comb[0][1](col, comb[1][1])
            if (
                board.is_position_empty(x, y)
                or (
                    (other_piece := board.get_piece_at(x, y))
                    and board_analyzer.are_opponents(curr_piece, other_piece)
                )
            ):
                moves.add(Move(row, col, x, y))
        
        return moves

class BishopMoveStrategy(ChessPieceMoveStrategy):
    @override
    def get_moves(self, row: int, col: int, board: IBoard, board_analyzer: IBoardAnalyzer) -> set[Move]:
        curr_piece = board.get_piece_at(row, col)
        moves = set()
        add = operator.add
        sub = operator.sub
        operators = [(add, add), (add, sub), (sub, add), (sub, sub)]
        for ops in operators:
            i = 0
            while True:
                i += 1
                x = ops[0](row, i)
                y = ops[1](col, i)
                if not board.is_valid_position(x, y):
                    break
                elif (other_piece := board.get_piece_at(x, y)):
                    if board_analyzer.are_opponents(curr_piece, other_piece):
                        moves.add(Move(row, col, x, y))
                    break
                else:
                    moves.add(Move(row, col, x, y))

        return moves

class RookMoveStrategy(ChessPieceMoveStrategy):
    @override
    def get_moves(self, row: int, col: int, board: IBoard, board_analyzer: IBoardAnalyzer) -> set[Move]:
        curr_piece = board.get_piece_at(row, col)
        moves = set()

        for op in [operator.add, operator.sub]:
            i = 0
            while True:
                i += 1
                x = op(row, i)
                if not board.is_valid_position(x, col):
                    break
                elif (other_piece := board.get_piece_at(x, col)):
                    if (board_analyzer.are_opponents(curr_piece, other_piece)):
                        moves.add(Move(row, col, x, col))
                    break
                else:
                    moves.add(Move(row, col, x, col))

        
        for op in [operator.add, operator.sub]:
            i = 0
            while True:
                i += 1
                y = op(col, i)
                if not board.is_valid_position(row, y):
                    break
                elif (other_piece := board.get_piece_at(row, y)):
                    if (board_analyzer.are_opponents(curr_piece, other_piece)):
                        moves.add(Move(row, col, row, y))
                    break
                else:
                    moves.add(Move(row, col, row, y))
        
        return moves

class KingMoveStrategy(ChessPieceMoveStrategy):
    @override
    def get_moves(self, row: int, col: int, board: IBoard, board_analyzer: IBoardAnalyzer) -> set[Move]:
        curr_piece = board.get_piece_at(row, col)
        moves = set()

        for delta_row in range(-1, 2):
            for delta_col in range(-1, 2):
                    x = row + delta_row
                    y = col + delta_col

                    if (
                        (delta_row or delta_col)
                        and board.is_valid_position(x, y)
                        and (
                                (other_piece := board.get_piece_at(x, y)) is None
                                or board_analyzer.are_opponents(curr_piece, other_piece)
                            )
                    ):
                        moves.add(Move(row, col, x, y))
        
        return moves

