"""
Перечисления для шахматной игры
"""

from enum import Enum


class PieceColor(Enum):
    WHITE = "Белые"
    BLACK = "Черные"

    def __init__(self, display_name):
        self._display_name = display_name

    def get_display_name(self):
        return self._display_name

    def opposite(self):
        return PieceColor.BLACK if self == PieceColor.WHITE else PieceColor.WHITE


class PieceType(Enum):
    PAWN = ("Пешка", "♟", "♙", 1)
    KNIGHT = ("Конь", "♞", "♘", 3)
    BISHOP = ("Слон", "♝", "♗", 3)
    ROOK = ("Ладья", "♜", "♖", 5)
    QUEEN = ("Ферзь", "♛", "♕", 9)
    KING = ("Король", "♚", "♔", 0)

    def __init__(self, display_name, black_symbol, white_symbol, value):
        self._display_name = display_name
        self._black_symbol = black_symbol
        self._white_symbol = white_symbol
        self._value = value

    def get_display_name(self):
        return self._display_name

    def get_symbol(self, color):
        return self._white_symbol if color == PieceColor.WHITE else self._black_symbol

    def get_value(self):
        return self._value


class GameStatus(Enum):
    NOT_STARTED = "Не начата"
    IN_PROGRESS = "В процессе"
    CHECK = "Шах"
    CHECKMATE_WHITE = "Мат - победа белых"
    CHECKMATE_BLACK = "Мат - победа черных"
    STALEMATE = "Пат"
    DRAW = "Ничья"
    DRAW_BY_AGREEMENT = "Ничья по согласию"
    DRAW_BY_REPETITION = "Ничья по повторению"
    DRAW_BY_50_MOVES = "Ничья по 50 ходам"

    def __init__(self, display_name):
        self._display_name = display_name

    def get_display_name(self):
        return self._display_name


class MoveType(Enum):
    NORMAL = "Обычный ход"
    CAPTURE = "Взятие"
    CASTLING_KINGSIDE = "Рокировка королевская"
    CASTLING_QUEENSIDE = "Рокировка ферзевая"
    EN_PASSANT = "Взятие на проходе"
    PROMOTION = "Превращение пешки"

    def __init__(self, display_name):
        self._display_name = display_name

    def get_display_name(self):
        return self._display_name


class PlayerType(Enum):
    HUMAN = "Человек"
    AI_EASY = "ИИ (легкий)"
    AI_MEDIUM = "ИИ (средний)"
    AI_HARD = "ИИ (сложный)"

    def __init__(self, display_name):
        self._display_name = display_name

    def get_display_name(self):
        return self._display_name