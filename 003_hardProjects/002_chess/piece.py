"""
Классы шахматных фигур
"""

from abc import ABC, abstractmethod
from enums import PieceType, PieceColor
from interfaces import Movable, Capturable


class Piece(Movable, Capturable, ABC):
    """Базовый класс шахматной фигуры"""

    def __init__(self, color, piece_type):
        self._color = color
        self._type = piece_type
        self._has_moved = False
        self._move_count = 0

    def get_color(self):
        return self._color

    def get_type(self):
        return self._type

    def has_moved(self):
        return self._has_moved

    def set_moved(self):
        self._has_moved = True
        self._move_count += 1

    def get_move_count(self):
        return self._move_count

    def can_be_captured(self):
        return True

    def get_symbol(self):
        return self._type.get_symbol(self._color)

    def get_value(self):
        return self._type.get_value()

    @abstractmethod
    def get_possible_moves(self, board, position):
        pass

    def is_valid_move(self, board, from_pos, to_pos):
        possible_moves = self.get_possible_moves(board, from_pos)
        return to_pos in possible_moves

    def __str__(self):
        return self.get_symbol()


class Pawn(Piece):
    """Пешка"""

    def __init__(self, color):
        super().__init__(color, PieceType.PAWN)

    def get_possible_moves(self, board, position):
        moves = []
        row, col = position
        direction = 1 if self._color == PieceColor.WHITE else -1

        # Ход вперед на одну клетку
        new_row = row + direction
        if 0 <= new_row < 8 and board.is_empty(new_row, col):
            moves.append((new_row, col))

            # Ход вперед на две клетки (начальная позиция)
            if not self._has_moved:
                new_row2 = row + 2 * direction
                if 0 <= new_row2 < 8 and board.is_empty(new_row2, col):
                    moves.append((new_row2, col))

        # Взятие по диагонали
        for col_offset in [-1, 1]:
            new_col = col + col_offset
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board.get_piece(new_row, new_col)
                if target_piece and target_piece.get_color() != self._color:
                    moves.append((new_row, new_col))

                # Взятие на проходе
                if board.en_passant_target == (new_row, new_col):
                    moves.append((new_row, new_col))

        return moves


class Knight(Piece):
    """Конь"""

    def __init__(self, color):
        super().__init__(color, PieceType.KNIGHT)

    def get_possible_moves(self, board, position):
        moves = []
        row, col = position

        # Все возможные ходы коня
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]

        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board.get_piece(new_row, new_col)
                if not target_piece or target_piece.get_color() != self._color:
                    moves.append((new_row, new_col))

        return moves


class Bishop(Piece):
    """Слон"""

    def __init__(self, color):
        super().__init__(color, PieceType.BISHOP)

    def get_possible_moves(self, board, position):
        return self._get_diagonal_moves(board, position)

    def _get_diagonal_moves(self, board, position):
        moves = []
        row, col = position

        # Четыре диагональных направления
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            for i in range(1, 8):
                new_row = row + dr * i
                new_col = col + dc * i

                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break

                target_piece = board.get_piece(new_row, new_col)

                if not target_piece:
                    moves.append((new_row, new_col))
                elif target_piece.get_color() != self._color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break

        return moves


class Rook(Piece):
    """Ладья"""

    def __init__(self, color):
        super().__init__(color, PieceType.ROOK)

    def get_possible_moves(self, board, position):
        return self._get_straight_moves(board, position)

    def _get_straight_moves(self, board, position):
        moves = []
        row, col = position

        # Четыре прямых направления
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            for i in range(1, 8):
                new_row = row + dr * i
                new_col = col + dc * i

                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break

                target_piece = board.get_piece(new_row, new_col)

                if not target_piece:
                    moves.append((new_row, new_col))
                elif target_piece.get_color() != self._color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break

        return moves


class Queen(Piece):
    """Ферзь"""

    def __init__(self, color):
        super().__init__(color, PieceType.QUEEN)

    def get_possible_moves(self, board, position):
        # Ферзь = ладья + слон
        moves = []
        moves.extend(self._get_straight_moves(board, position))
        moves.extend(self._get_diagonal_moves(board, position))
        return moves

    def _get_straight_moves(self, board, position):
        rook = Rook(self._color)
        return rook._get_straight_moves(board, position)

    def _get_diagonal_moves(self, board, position):
        bishop = Bishop(self._color)
        return bishop._get_diagonal_moves(board, position)


class King(Piece):
    """Король"""

    def __init__(self, color):
        super().__init__(color, PieceType.KING)

    def can_be_captured(self):
        return False  # Короля нельзя взять, только поставить мат

    def get_possible_moves(self, board, position):
        moves = []
        row, col = position

        # Король ходит на одну клетку в любом направлении
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board.get_piece(new_row, new_col)
                if not target_piece or target_piece.get_color() != self._color:
                    moves.append((new_row, new_col))

        # Рокировка
        if not self._has_moved and not board.is_in_check(self._color):
            # Королевская рокировка
            if self._can_castle_kingside(board, position):
                moves.append((row, col + 2))

            # Ферзевая рокировка
            if self._can_castle_queenside(board, position):
                moves.append((row, col - 2))

        return moves

    def _can_castle_kingside(self, board, position):
        row, col = position

        # Проверка что между королем и ладьей пусто
        if not board.is_empty(row, col + 1) or not board.is_empty(row, col + 2):
            return False

        # Проверка что ладья на месте и не ходила
        rook = board.get_piece(row, 7)
        if not rook or rook.get_type() != PieceType.ROOK or rook.has_moved():
            return False

        # Проверка что король не проходит через битое поле
        if board.is_square_attacked((row, col + 1), self._color.opposite()):
            return False

        return True

    def _can_castle_queenside(self, board, position):
        row, col = position

        # Проверка что между королем и ладьей пусто
        if not board.is_empty(row, col - 1) or not board.is_empty(row, col - 2) or not board.is_empty(row, col - 3):
            return False

        # Проверка что ладья на месте и не ходила
        rook = board.get_piece(row, 0)
        if not rook or rook.get_type() != PieceType.ROOK or rook.has_moved():
            return False

        # Проверка что король не проходит через битое поле
        if board.is_square_attacked((row, col - 1), self._color.opposite()):
            return False

        return True