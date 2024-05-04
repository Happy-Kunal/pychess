from copy import deepcopy

from chess_enums import ChessPieceColor, GameMode
from exceptions import ChessPieceNotFoundException, KingPieceNotFoundException
from historical_move import HistoricalMove, Move
from intefaces import IChessPiece, IBoard

class Board:
    def __init__(self, pieces: list[IChessPiece], max_history: int = 10000):
        self.game_board = [[None] * 8 for _ in range(8)]
        self.white_king = None
        self.black_king = None
        self.white_pieces: set[IChessPiece] = set()
        self.black_pieces: set[IChessPiece] = set()
        self.game_history: list[HistoricalMove] = list()
        self.max_history = max_history


        for piece in pieces:
            self.game_board[piece.get_row()][piece.get_col()] = piece
            if piece.get_color() is ChessPieceColor.BLACK:
                self.black_pieces.add(piece)
                if (piece.is_king()): self.black_king = piece
            else:
                self.white_pieces.add(piece)
                if (piece.is_king()): self.white_king = piece
        
        if (not self.white_king): raise KingPieceNotFoundException(color=ChessPieceColor.WHITE)
        if (not self.black_king): raise KingPieceNotFoundException(color=ChessPieceColor.BLACK)
    
    def make_move(self, x1: int, y1: int, x2: int, y2: int):
        piece = self.get_piece_at(x1, y1)

        if piece is None:
            raise ChessPieceNotFoundException(x1, y1)
        elif killed_piece := self.get_piece_at(x2, y2):
            if (killed_piece.get_color() is ChessPieceColor.WHITE):
                self.white_pieces.remove(killed_piece)
            else:
                self.black_pieces.remove(killed_piece)

        if len(self.game_history) >= self.max_history:
            self.game_history.pop(0)
        
        self.game_history.append(
            HistoricalMove(
                positions=Move(
                    x1=x1,
                    y1=y1,
                    x2=x2,
                    y2=y2
                ),
                moved_piece=piece,
                killed_piece=killed_piece
            )
        )

        self.game_board[x2][y2] = self.game_board[x1][y1]
        self.game_board[x1][y1] = None

        piece.set_position(x2, y2)

    def unmake_move(self):
        if (self.game_history):
            last_move = self.game_history.pop()
            self.game_board[last_move.positions.x1][last_move.positions.y1] = last_move.moved_piece
            self.game_board[last_move.positions.x2][last_move.positions.y2] = last_move.killed_piece
            last_move.moved_piece.set_position(last_move.positions.x1, last_move.positions.y1)

            if (last_move.killed_piece is not None):
                if (last_move.killed_piece.get_color() is ChessPieceColor.WHITE):
                    self.white_pieces.add(last_move.killed_piece)
                else:
                    self.black_pieces.add(last_move.killed_piece)


    def get_piece_at(self, x: int, y: int) -> IChessPiece | None:
        if (0 <= x < 8 and 0 <= y < 8):
            return self.game_board[x][y]
        return None
    
    def is_valid_position(self, x: int, y: int) -> bool:
        return 0 <= x < 8 and 0 <= y < 8
    
    def is_position_empty(self, x: int, y: int) -> bool:
        return self.is_valid_position(x, y) and self.get_piece_at(x, y) is None
    
    def get_king(self, color: ChessPieceColor) -> IChessPiece:
        return self.white_king if color is ChessPieceColor.WHITE else self.black_king
    
    def get_pieces(self, color: ChessPieceColor) -> set[IChessPiece]:
        if (color is ChessPieceColor.WHITE):
            return self.white_pieces
        else:
            return self.black_pieces


class BoardAnalyzer:
    @classmethod
    def are_friends(cls, piece1: IChessPiece, piece2: IChessPiece) -> bool:
        return piece1.get_color() == piece2.get_color()
    
    @classmethod
    def are_opponents(cls, piece1: IChessPiece, piece2: IChessPiece) -> bool:
        return not cls.are_friends(piece1, piece2)
    
    @classmethod
    def is_there_any_threat_to_king(cls, color: ChessPieceColor, board: IBoard) -> bool:
        king = board.get_king(color=color)
        enemies = board.get_pieces(ChessPieceColor.BLACK) if color is ChessPieceColor.WHITE else board.get_pieces(ChessPieceColor.WHITE)

        x, y = king.get_row(), king.get_col()
        
        for enemy in enemies:
            moves = enemy.get_moves(board=board, board_analyzer=cls)
            for move in moves:
                if move.x2 == x and move.y2 == y:
                    return True
        
        return False
    
    @classmethod
    def filter_moves(cls, color: ChessPieceColor, moves: set[Move], board: IBoard) -> set[Move]:
        output_moves = moves.copy()
        for move in moves:
            board.make_move(x1=move.x1, y1=move.y1, x2=move.x2, y2=move.y2)
            if (cls.is_there_any_threat_to_king(color=color, board=board)):
                output_moves.remove(move)
            board.unmake_move()
        
        return output_moves

    
    @classmethod
    def get_all_valid_moves(cls, color: ChessPieceColor, board: IBoard) -> set[Move]:
        valid_moves = set()
        for piece in (board.get_pieces(color=color)):
            valid_moves = valid_moves.union(
                cls.filter_moves(
                    color=color,
                    board=board,
                    moves=piece.get_moves(
                        board=board, board_analyzer=cls
                    )
                )
            )

        return valid_moves

    
    @classmethod
    def has_moves(cls, color: ChessPieceColor, board: IBoard):
        comrade_pieces = board.get_pieces(color=color)

        for piece in comrade_pieces:
            if (len(cls.filter_moves(color=piece.get_color(), moves=piece.get_moves(board=board, board_analyzer=cls), board=board))):
                return True
        
        return False
    
    @classmethod
    def insufficient_material(cls, board: IBoard) -> bool:
        # TODO: figure out how to write a scaleable and
        # dependency injection based implementation for
        # this method
        return False
    
    @classmethod
    def is_winner(cls, color: ChessPieceColor, board: IBoard) -> bool:
        opponent_color = ChessPieceColor.BLACK if color is ChessPieceColor.WHITE else ChessPieceColor.WHITE
        return (
            cls.is_there_any_threat_to_king(color=opponent_color, board=board)
            and not cls.has_moves(color=opponent_color, board=board)
        )
    
    @classmethod
    def is_draw(cls, board: IBoard) -> bool:
        return (
            not cls.is_winner(color=ChessPieceColor.WHITE, board=board)
            and not cls.is_winner(color=ChessPieceColor.BLACK, board=board)
            and cls.insufficient_material(board=board)
        )
    
    @classmethod
    def is_terminal(cls, board: IBoard) -> bool:
        return (
            cls.is_winner(color=ChessPieceColor.WHITE, board=board)
            or cls.is_winner(color=ChessPieceColor.BLACK, board=board)
            or cls.is_draw(board=board)
        )
    
    @classmethod
    def evaluate_delta_points_for_given_board(cls, board: IBoard) -> int:
        delta_points = 0
        for piece in board.get_pieces(ChessPieceColor.WHITE):
            delta_points += piece.get_points()
        
        for piece in board.get_pieces(ChessPieceColor.BLACK):
            delta_points -= piece.get_points()

        return delta_points
    
    @classmethod
    def evaluate_board(cls, game_mode: GameMode, board: IBoard) -> int:
        if (game_mode is GameMode.BLACK_DOWN): return -cls.evaluate_board(GameMode.WHITE_DOWN, board=board)
        
        kings_score_sum = board.get_king(ChessPieceColor.WHITE).get_points() + board.get_king(ChessPieceColor.BLACK).get_points()

        if cls.is_winner(ChessPieceColor.WHITE, board=board): return kings_score_sum
        elif cls.is_winner(ChessPieceColor.BLACK, board=board): return -kings_score_sum
        elif cls.is_draw(board=board): return 0
        else: return cls.evaluate_delta_points_for_given_board(board=board)
