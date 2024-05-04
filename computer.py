import math
from board import Board
import random

from chess_enums import ChessPieceColor, GameMode
from move import Move
from chess_game_data import ChessGameData
from intefaces import IChessPiece

i = 0
def minimax(game_data: ChessGameData, curr_depth: int, computers_turn: bool, alpha: int = math.inf, beta: int = -math.inf) -> tuple[int, Move | None]:
    global i
    players_color = ChessPieceColor.WHITE if game_data.game_mode is GameMode.WHITE_DOWN else ChessPieceColor.BLACK
    computers_color = ChessPieceColor.BLACK if game_data.game_mode is GameMode.WHITE_DOWN else ChessPieceColor.WHITE
    if curr_depth <= 0 or game_data.board_analyzer.is_terminal(board=game_data.board):
        return (game_data.board_analyzer.evaluate_board(game_mode=game_data.game_mode, board=game_data.board), None)
    elif computers_turn:
        min_score = math.inf
        best_move = None
        for move in game_data.board_analyzer.get_all_valid_moves(color=computers_color, board=game_data.board):
            game_data.board.make_move(x1=move.x1, y1=move.y1, x2=move.x2, y2=move.y2)
            (curr_score, next_move) = minimax(game_data, curr_depth - 1, computers_turn=False, alpha=alpha, beta=beta)
            if curr_score < min_score:
                min_score = curr_score
                best_move = move
            elif curr_score == min_score and random.random() > 0.5:
                best_move = move
            
            game_data.board.unmake_move()
            alpha = min(alpha, curr_score)

            if alpha < beta:
                break

        
        i += 1
        if (i % 100 == 0): print(i, alpha, beta)

        return (min_score, best_move)

    else:
        max_score = -math.inf
        best_move = None
        for move in game_data.board_analyzer.get_all_valid_moves(color=players_color, board=game_data.board):
            game_data.board.make_move(x1=move.x1, y1=move.y1, x2=move.x2, y2=move.y2)
            (curr_score, next_move) = minimax(game_data, curr_depth - 1, computers_turn=True, alpha=alpha, beta=beta)
            if curr_score > max_score:
                max_score = curr_score
                best_move = move
            elif curr_score == max_score and random.random() > 0.5:
                best_move = move
            
            game_data.board.unmake_move()
            beta = max(beta, curr_score)

            if alpha < beta:
                break


        if (i % 100 == 0): print(i, alpha, beta)
        i += 1

        return (max_score, best_move)



def get_ai_move(game_data: ChessGameData) -> Move:
    global i
    i = 0
    (_, move) = minimax(game_data=game_data, curr_depth=game_data.depth, computers_turn=True)
    return move

