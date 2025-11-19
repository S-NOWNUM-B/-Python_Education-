"""
Интерфейсы для шахматной игры
"""

from abc import ABC, abstractmethod


class Movable(ABC):
    """Интерфейс для фигур, которые могут двигаться"""

    @abstractmethod
    def get_possible_moves(self, board, position):
        """Получить возможные ходы"""
        pass

    @abstractmethod
    def is_valid_move(self, board, from_pos, to_pos):
        """Проверка корректности хода"""
        pass


class Capturable(ABC):
    """Интерфейс для фигур, которые могут быть взяты"""

    @abstractmethod
    def can_be_captured(self):
        """Может ли фигура быть взята"""
        pass