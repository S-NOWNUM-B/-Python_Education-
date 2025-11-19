"""
Шахматная доска
"""

from piece import Pawn, Knight, Bishop, Rook, Queen, King
from enums import PieceColor, PieceType
from exceptions import InvalidPositionException


class Board:
    """Шахматная доска 8x8"""

    def __init__(self):
        self._board = [[None for _ in range(8)] for _ in range(8)]
        self._captured_pieces = {PieceColor.WHITE: [], PieceColor.BLACK: []}
        self.en_passant_target = None
        self._initialize_board()

    def _initialize_board(self):
        """Начальная расстановка фигур"""
        # Пешки
        for col in range(8):
            self._board[1][col] = Pawn(PieceColor.BLACK)
            self._board[6][col] = Pawn(PieceColor.WHITE)

        # Остальные фигуры
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        for col, piece_class in enumerate(piece_order):
            self._board[0][col] = piece_class(PieceColor.BLACK)
            self._board[7][col] = piece_class(PieceColor.WHITE)

    def get_piece(self, row, col):
        """Получить фигуру на позиции"""
        if not self._is_valid_position(row, col):
            raise InvalidPositionException(f"Некорректная позиция: ({row}, {col})")
        return self._board[row][col]

    def set_piece(self, row, col, piece):
        """Установить фигуру на позицию"""
        if not self._is_valid_position(row, col):
            raise InvalidPositionException(f"Некорректная позиция: ({row}, {col})")
        self._board[row][col] = piece

    def remove_piece(self, row, col):
        """Убрать фигуру с позиции"""
        piece = self.get_piece(row, col)
        self._board[row][col] = None
        return piece

    def is_empty(self, row, col):
        """Проверка, пуста ли клетка"""
        return self.get_piece(row, col) is None

    def _is_valid_position(self, row, col):
        """Проверка корректности позиции"""
        return 0 <= row < 8 and 0 <= col < 8

    def find_king(self, color):
        """Найти короля указанного цвета"""
        for row in range(8):
            for col in range(8):
                piece = self._board[row][col]
                if piece and piece.get_type() == PieceType.KING and piece.get_color() == color:
                    return (row, col)
        return None

    def is_square_attacked(self, position, by_color):
        """Проверка, атакована ли клетка фигурами указанного цвета"""
        for row in range(8):
            for col in range(8):
                piece = self._board[row][col]
                if piece and piece.get_color() == by_color:
                    if piece.get_type() == PieceType.KING:
                        # Для короля проверяем только соседние клетки
                        king_moves = [
                            (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                            (row, col - 1), (row, col + 1),
                            (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)
                        ]
                        if position in king_moves:
                            return True
                    else:
                        possible_moves = piece.get_possible_moves(self, (row, col))
                        if position in possible_moves:
                            return True
        return False

    def is_in_check(self, color):
        """Проверка, находится ли король под шахом"""
        king_pos = self.find_king(color)
        if not king_pos:
            return False
        return self.is_square_attacked(king_pos, color.opposite())

    def get_all_possible_moves(self, color):
        """Получить все возможные ходы для цвета"""
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self._board[row][col]
                if piece and piece.get_color() == color:
                    piece_moves = piece.get_possible_moves(self, (row, col))
                    for move in piece_moves:
                        moves.append(((row, col), move))
        return moves

    def capture_piece(self, piece):
        """Добавить фигуру в список захваченных"""
        self._captured_pieces[piece.get_color()].append(piece)

    def get_captured_pieces(self, color):
        """Получить захваченные фигуры"""
        return self._captured_pieces[color]

    def display(self):
        """Отобразить доску"""
        print("\n    a  b  c  d  e  f  g  h")
        print("  ┌─────────────────────────┐")

        for row in range(8):
            print(f"{8 - row} │", end="")
            for col in range(8):
                piece = self._board[row][col]
                if piece:
                    print(f" {piece.get_symbol()} ", end="")
                else:
                    # Шахматная раскраска
                    if (row + col) % 2 == 0:
                        print(" · ", end="")
                    else:
                        print("   ", end="")
            print(f"│ {8 - row}")

        print("  └─────────────────────────┘")
        print("    a  b  c  d  e  f  g  h\n")

    def clone(self):
        """Создать копию доски"""
        new_board = Board()
        new_board._board = [[self._board[row][col] for col in range(8)] for row in range(8)]
        new_board.en_passant_target = self.en_passant_target
        return new_board