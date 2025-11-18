"""
Исключения для шахматной игры
"""

class ChessException(Exception):
    """Базовое исключение для шахмат"""
    pass

class InvalidMoveException(ChessException):
    """Некорректный ход"""
    pass

class InvalidPositionException(ChessException):
    """Некорректная позиция на доске"""
    pass

class GameOverException(ChessException):
    """Игра завершена"""
    pass

class KingInCheckException(ChessException):
    """Король под шахом"""
    pass

class InvalidNotationException(ChessException):
    """Некорректная шахматная нотация"""
    pass

class SaveGameException(ChessException):
    """Ошибка сохранения игры"""
    pass
