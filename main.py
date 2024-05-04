import sys
from graphics import Graphics
from board import Board, BoardAnalyzer
from chess_game_data import ChessGameData

from chess_enums import GameMode
from factory import normal_chess_board_pieces_factory
from chesspiece_with_gui_factory import ChessPieceWithGUIFactory


if __name__ == '__main__':
    keep_playing = True
    
    try:
        depth = int(sys.argv[1])
    except Exception:
        print("invalid value for depth taking default depth = 2")
        depth = 2

    game_mode = GameMode.WHITE_DOWN
    chess_piece_factory = ChessPieceWithGUIFactory(game_mode=game_mode)

    pieces = normal_chess_board_pieces_factory(chess_piece_factory=chess_piece_factory)
    board = Board(pieces=pieces)
    board_analyzer = BoardAnalyzer()
    game_data = ChessGameData(
        game_mode=game_mode,
        board=board,
        board_analyzer=board_analyzer,
        depth=depth,
        play_with_ai=True
    )

    gui = Graphics(game_data=game_data)

    while keep_playing:
        gui.draw_background()
        keep_playing = gui.start()
        
