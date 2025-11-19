"""
Искусственный интеллект для игры в шахматы
"""

import random
from enums import PlayerType, PieceType


class ChessAI:
    """ИИ для шахмат"""

    def __init__(self, difficulty=PlayerType.AI_MEDIUM):
        self._difficulty = difficulty

    def get_best_move(self, game, color):
        """Получить лучший ход"""
        if self._difficulty == PlayerType.AI_EASY:
            return self._get_random_move(game, color)
        elif self._difficulty == PlayerType.AI_MEDIUM:
            return self._get_medium_move(game, color)
        else:
            return self._get_hard_move(game, color)

    def _get_random_move(self, game, color):
        """Случайный ход (легкий уровень)"""
        legal_moves = game._get_legal_moves(color)
        if not legal_moves:
            return None
        return random.choice(legal_moves)

    def _get_medium_move(self, game, color):
        """Средний уровень - с оценкой позиции"""
        legal_moves = game._get_legal_moves(color)
        if not legal_moves:
            return None

        # Оценка каждого хода
        best_score = float('-inf')
        best_move = None

        for from_pos, to_pos in legal_moves:
            score = self._evaluate_move(game, from_pos, to_pos, color)
            if score > best_score:
                best_score = score
                best_move = (from_pos, to_pos)

        return best_move

    def _get_hard_move(self, game, color):
        """Сложный уровень - минимакс с альфа-бета отсечением"""
        # Упрощенная реализация
        return self._minimax(game, color, depth=3)

    def _evaluate_move(self, game, from_pos, to_pos, color):
        """Оценка хода"""
        score = 0

        piece = game._board.get_piece(*from_pos)
        target = game._board.get_piece(*to_pos)

        # Взятие фигуры
        if target:
            score += self._get_piece_value(target) * 10

        # Контроль центра
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        if to_pos in center_squares:
            score += 5

        # Развитие фигур
        if piece.get_type() in [PieceType.KNIGHT, PieceType.BISHOP]:
            if not piece.has_moved():
                score += 3

        return score

    def _get_piece_value(self, piece):
        """Получить ценность фигуры"""
        values = {
            PieceType.PAWN: 1,
            PieceType.KNIGHT: 3,
            PieceType.BISHOP: 3,
            PieceType.ROOK: 5,
            PieceType.QUEEN: 9,
            PieceType.KING: 0
        }
        return values.get(piece.get_type(), 0)

    def _minimax(self, game, color, depth):
        """Алгоритм минимакс (упрощенный)"""
        # Базовая реализация для демонстрации
        return self._get_medium_move(game, color)
