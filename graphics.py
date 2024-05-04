import itertools

import pygame

from chesspiece import ChessPiece
from computer import get_ai_move
from chess_game_data import ChessGameData
from chess_enums import ChessPieceColor, BoardBackgroundTile, GameMode

assets = dict()
assets[BoardBackgroundTile.DARK] = pygame.transform.scale(pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/square brown dark_png_shadow_128px.png'), (75, 75))
assets[BoardBackgroundTile.LIGHT] = pygame.transform.scale(pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/square brown light_png_shadow_128px.png'), (75, 75))

assets[BoardBackgroundTile.HIGHLIGHTED] = pygame.transform.scale(pygame.image.load('assets/JohnPablok Cburnett Chess set/128px/highlight_128px.png'), (75, 75))

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)


class Graphics:
    def __init__(self, game_data: ChessGameData, size: tuple[int, int] = (600, 650)): 
        pygame.init()
        pygame.display.set_caption('ChessAI')
        icon = pygame.image.load('assets/icon.png')
        pygame.display.set_icon(icon)

        self.screen = pygame.display.set_mode(size=size)
        self.screen.fill((0, 0, 0))
        self.game_data = game_data

    def draw_background(self):
        block_x = 0
        for _ in range(4):
            block_y = 0
            for _ in range(4):
                self.screen.blit(assets[BoardBackgroundTile.LIGHT], (block_x, block_y))
                self.screen.blit(assets[BoardBackgroundTile.DARK], (block_x + 75, block_y))
                self.screen.blit(assets[BoardBackgroundTile.LIGHT], (block_x + 75, block_y + 75))
                self.screen.blit(assets[BoardBackgroundTile.DARK], (block_x, block_y + 75))
                block_y += 150
            block_x += 150
        
        step_x = 0
        surface_width = pygame.display.get_surface().get_size()[0]

        for piece in itertools.chain(self.game_data.board.get_pieces(ChessPieceColor.WHITE), self.game_data.board.black_pieces):
            row, col = piece.get_row(), piece.get_col()
            step_x = col * 75
            step_y = surface_width - 75 * (row + 1)
            self.screen.blit(piece.get_image(), (step_x, step_y))

        pygame.display.update()

    def draw_text(self, text: str):
        surface = pygame.Surface((400, 50))
        surface.fill((0, 0, 0))
        self.screen.blit(surface, (100, 600))
        text_surface = font.render(text, False, (237, 237, 237))
        if 'DRAW' in text:
            x = 260
        else:
            x = 230
        text_surface_restart = font.render('PRESS "SPACE" TO RESTART', False, (237, 237, 237))
        self.screen.blit(text_surface, (x, 600))
        self.screen.blit(text_surface_restart, (150, 620))
        pygame.display.update()

    def start(self):
        possible_piece_moves = []
        running = True
        visible_moves = False
        dimensions = pygame.display.get_surface().get_size()
        game_over = False
        piece = None
        player_color = ChessPieceColor.WHITE if self.game_data.game_mode is GameMode.WHITE_DOWN else ChessPieceColor.BLACK
        if self.game_data.game_mode is GameMode.BLACK_DOWN and self.game_data.play_with_ai:
            move = get_ai_move(self.game_data)
            self.game_data.board.make_move(x1=move.x1, y1=move.y1, x2=move.x2, y2=move.y2)
            self.draw_background()

        moving_piece = None
        while running:
            if game_over:
                self.draw_text(game_over_txt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if game_over and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return True # restart game
                    else:
                        return False # game over
                if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                    x = 7 - pygame.mouse.get_pos()[1] // 75
                    y = pygame.mouse.get_pos()[0] // 75
                    if (piece := self.game_data.board.get_piece_at(x, y)) and (player_color == piece.get_color() or not self.game_data.play_with_ai) and (x, y) not in possible_piece_moves:
                        moving_piece = piece
                        moves = self.game_data.board_analyzer.filter_moves(
                            color=piece.get_color(),
                            moves=piece.get_moves(board=self.game_data.board, board_analyzer=self.game_data.board_analyzer),
                            board=self.game_data.board
                        )
                        move_positions = []
                        possible_piece_moves.clear()
                        
                        for move in moves:
                            move_positions.append((dimensions[0] - (8 - move.y2) * 75, dimensions[1] - move.x2 * 75 - 125))
                            move_x = 7 - move_positions[-1][1] // 75
                            move_y = move_positions[-1][0] // 75
                            possible_piece_moves.append((move_x, move_y))
                        
                        if visible_moves:
                            self.draw_background()
                            visible_moves = False
                        
                        for move in move_positions:
                            visible_moves = True
                            self.screen.blit(assets[BoardBackgroundTile.HIGHLIGHTED], (move[0], move[1]))
                            pygame.display.update()
                    
                    else:
                        clicked_move = (x, y)
                        try:
                            if clicked_move in possible_piece_moves:
                                self.game_data.board.make_move(moving_piece.get_row(), moving_piece.get_col(), x, y)
                                possible_piece_moves.clear()
                                self.draw_background()
                                if self.game_data.play_with_ai:
                                    move = get_ai_move(self.game_data)
                                    if (move is not None):
                                        self.game_data.board.make_move(x1=move.x1, y1=move.y1, x2=move.x2, y2=move.y2)
                                        self.draw_background()
                                        
                            if self.game_data.board_analyzer.is_winner(color=ChessPieceColor.WHITE, board=self.game_data.board):
                                game_over = True
                                game_over_txt = 'WHITE WINS!'
                            elif self.game_data.board_analyzer.is_winner(color=ChessPieceColor.BLACK, board=self.game_data.board):
                                game_over = True
                                game_over_txt = 'BLACK WINS!'
                            elif self.game_data.board_analyzer.is_draw(board=self.game_data.board):
                                game_over = True
                                game_over_txt = 'DRAW!'
                        except UnboundLocalError:
                            print("Error")
        
        return False
