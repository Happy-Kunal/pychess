from enum import Enum, auto


class ChessPieceColor(str, Enum):
    BLACK = 'black'
    WHITE = 'white'

class BoardBackgroundTile(str, Enum):
    LIGHT = 'light'
    DARK = 'dark'
    HIGHLIGHTED = 'highlight'

class GameMode:
    WHITE_DOWN = auto()
    BLACK_DOWN = auto()
    