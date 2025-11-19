"""
Класс шахматного хода
"""

from datetime import datetime
from enums import MoveType, PieceType


class Move:
    """Шахматный ход"""

    def __init__(self, from_pos, to_pos, piece, captured_piece=None, move_type=MoveType.NORMAL):
        self._from_pos = from_pos
        self._to_pos = to_pos
        self._piece = piece
        self._captured_piece = captured_piece
        self._move_type = move_type
        self._timestamp = datetime.now()
        self._promotion_piece = None
        self._is_check = False
        self._is_checkmate = False

    def get_from_pos(self):
        return self._from_pos

    def get_to_pos(self):
        return self._to_pos

    def get_piece(self):
        return self._piece

    def get_captured_piece(self):
        return self._captured_piece

    def get_move_type(self):
        return self._move_type

    def get_timestamp(self):
        return self._timestamp

    def set_promotion_piece(self, piece_type):
        self._promotion_piece = piece_type

    def get_promotion_piece(self):
        return self._promotion_piece

    def set_check(self, is_check):
        self._is_check = is_check

    def set_checkmate(self, is_checkmate):
        self._is_checkmate = is_checkmate

    def is_check(self):
        return self._is_check

    def is_checkmate(self):
        return self._is_checkmate

    def to_algebraic(self):
        """Преобразовать ход в алгебраическую нотацию"""
        from_col = chr(ord('a') + self._from_pos[1])
        from_row = str(8 - self._from_pos[0])
        to_col = chr(ord('a') + self._to_pos[1])
        to_row = str(8 - self._to_pos[0])

        piece_symbol = ""
        if self._piece.get_type() != PieceType.PAWN:
            symbols = {
                PieceType.KNIGHT: "N",
                PieceType.BISHOP: "B",
                PieceType.ROOK: "R",
                PieceType.QUEEN: "Q",
                PieceType.KING: "K"
            }
            piece_symbol = symbols.get(self._piece.get_type(), "")

        # Рокировка
        if self._move_type == MoveType.CASTLING_KINGSIDE:
            return "O-O"
        elif self._move_type == MoveType.CASTLING_QUEENSIDE:
            return "O-O-O"

        # Обычный ход
        capture_symbol = "x" if self._captured_piece else ""
        promotion_symbol = ""
        if self._promotion_piece:
            promotion_symbols = {
                PieceType.QUEEN: "Q",
                PieceType.ROOK: "R",
                PieceType.BISHOP: "B",
                PieceType.KNIGHT: "N"
            }
            promotion_symbol = "=" + promotion_symbols.get(self._promotion_piece, "")

        check_symbol = "+" if self._is_check else ""
        checkmate_symbol = "#" if self._is_checkmate else ""

        return f"{piece_symbol}{from_col}{from_row}{capture_symbol}{to_col}{to_row}{promotion_symbol}{check_symbol}{checkmate_symbol}"

    def __str__(self):
        return self.to_algebraic()