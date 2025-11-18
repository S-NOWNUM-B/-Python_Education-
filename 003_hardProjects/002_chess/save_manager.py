"""
Менеджер сохранения и загрузки игр
"""

import json
import os
from datetime import datetime
from exceptions import SaveGameException


class SaveManager:
    """Менеджер сохранения партий"""

    SAVE_DIR = "saved_games"

    def __init__(self):
        if not os.path.exists(self.SAVE_DIR):
            os.makedirs(self.SAVE_DIR)

    def save_game(self, game, filename=None):
        """Сохранить игру"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"chess_game_{timestamp}.json"

        filepath = os.path.join(self.SAVE_DIR, filename)

        try:
            game_data = self._serialize_game(game)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(game_data, f, ensure_ascii=False, indent=2)

            print(f"\n✓ Игра сохранена: {filename}")
            return filepath

        except Exception as e:
            raise SaveGameException(f"Ошибка сохранения игры: {str(e)}")

    def load_game(self, filename):
        """Загрузить игру"""
        filepath = os.path.join(self.SAVE_DIR, filename)

        if not os.path.exists(filepath):
            raise SaveGameException(f"Файл не найден: {filename}")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                game_data = json.load(f)

            game = self._deserialize_game(game_data)
            print(f"\n✓ Игра загружена: {filename}")
            return game

        except Exception as e:
            raise SaveGameException(f"Ошибка загрузки игры: {str(e)}")

    def list_saved_games(self):
        """Список сохраненных игр"""
        files = [f for f in os.listdir(self.SAVE_DIR) if f.endswith('.json')]
        return sorted(files, reverse=True)

    def _serialize_game(self, game):
        """Сериализация игры в JSON"""
        moves_data = []
        for move in game.get_move_history():
            moves_data.append({
                'notation': move.to_algebraic(),
                'timestamp': move.get_timestamp().isoformat()
            })

        return {
            'white_player': {
                'name': game._white_player.get_name(),
                'rating': game._white_player.get_rating()
            },
            'black_player': {
                'name': game._black_player.get_name(),
                'rating': game._black_player.get_rating()
            },
            'moves': moves_data,
            'status': game.get_status().name,
            'move_count': game._move_count,
            'saved_at': datetime.now().isoformat()
        }

    def _deserialize_game(self, game_data):
        """Десериализация игры из JSON"""
        # Упрощенная реализация
        # В полной версии нужно восстановить позицию на доске
        return None