from chess_enums import ChessPieceColor

class ChessPieceNotFoundException(Exception):
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        super().__init__(f"no chess piece at ({self.x}, {self.y})")

class KingPieceNotFoundException(Exception):
    def __init__(self, color: ChessPieceColor) -> None:
        super().__init__(f"no king found for {color.value} pieces")

