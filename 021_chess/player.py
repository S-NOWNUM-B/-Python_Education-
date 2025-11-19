"""
Класс игрока
"""

from enums import PieceColor, PlayerType


class Player:
    """Шахматный игрок"""

    def __init__(self, name, color, player_type=PlayerType.HUMAN):
        self._name = name
        self._color = color
        self._player_type = player_type
        self._rating = 1200
        self._wins = 0
        self._losses = 0
        self._draws = 0

    def get_name(self):
        return self._name

    def get_color(self):
        return self._color

    def get_player_type(self):
        return self._player_type

    def get_rating(self):
        return self._rating

    def update_rating(self, delta):
        self._rating += delta

    def add_win(self):
        self._wins += 1

    def add_loss(self):
        self._losses += 1

    def add_draw(self):
        self._draws += 1

    def get_statistics(self):
        total_games = self._wins + self._losses + self._draws
        if total_games == 0:
            win_rate = 0
        else:
            win_rate = (self._wins / total_games) * 100

        return {
            'wins': self._wins,
            'losses': self._losses,
            'draws': self._draws,
            'total_games': total_games,
            'win_rate': win_rate
        }

    def display_info(self):
        """Отобразить информацию об игроке"""
        stats = self.get_statistics()

        print(f"\n=== Игрок: {self._name} ===")
        print(f"Цвет: {self._color.get_display_name()}")
        print(f"Тип: {self._player_type.get_display_name()}")
        print(f"Рейтинг: {self._rating}")
        print(f"\nСтатистика:")
        print(f"  Побед: {stats['wins']}")
        print(f"  Поражений: {stats['losses']}")
        print(f"  Ничьих: {stats['draws']}")
        print(f"  Всего игр: {stats['total_games']}")
        print(f"  Процент побед: {stats['win_rate']:.1f}%")
        print("---")