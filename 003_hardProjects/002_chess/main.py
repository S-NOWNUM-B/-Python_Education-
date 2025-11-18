"""
Главный файл шахматной игры
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game import ChessGame
from player import Player
from ai import ChessAI
from save_manager import SaveManager
from enums import PieceColor, PlayerType, GameStatus, PieceType
from exceptions import ChessException
from utils import parse_move_input


class ChessUI:
    """Пользовательский интерфейс"""

    def __init__(self):
        self._game = None
        self._save_manager = SaveManager()
        self._ai = None

    def run(self):
        """Запуск игры"""
        print("╔════════════════════════════════════════╗")
        print("║         ШАХМАТНАЯ ИГРА                 ║")
        print("╚════════════════════════════════════════╝\n")

        while True:
            try:
                if not self._game:
                    self._main_menu()
                else:
                    self._game_loop()

            except KeyboardInterrupt:
                print("\n\nВыход из игры...")
                break
            except ChessException as e:
                print(f"\n✗ Ошибка: {str(e)}")
            except Exception as e:
                print(f"\n✗ Непредвиденная ошибка: {str(e)}")

    def _main_menu(self):
        """Главное меню"""
        print("\n=== Главное меню ===")
        print("1. Новая игра (Игрок vs Игрок)")
        print("2. Новая игра (Игрок vs ИИ)")
        print("3. Загрузить игру")
        print("4. Выход")

        choice = input("\nВыбор: ").strip()

        if choice == '1':
            self._new_game_pvp()
        elif choice == '2':
            self._new_game_ai()
        elif choice == '3':
            self._load_game()
        elif choice == '4':
            sys.exit(0)

    def _new_game_pvp(self):
        """Новая игра игрок против игрока"""
        print("\n=== Новая игра ===")
        white_name = input("Имя игрока (белые): ") or "Игрок 1"
        black_name = input("Имя игрока (черные): ") or "Игрок 2"

        white_player = Player(white_name, PieceColor.WHITE)
        black_player = Player(black_name, PieceColor.BLACK)

        self._game = ChessGame(white_player, black_player)
        print("\n✓ Игра начата!")

    def _new_game_ai(self):
        """Новая игра против ИИ"""
        print("\n=== Новая игра против ИИ ===")
        player_name = input("Ваше имя: ") or "Игрок"

        print("\nВыберите сложность:")
        print("1. Легкий")
        print("2. Средний")
        print("3. Сложный")

        difficulty_choice = input("Выбор: ").strip()
        difficulty_map = {
            '1': PlayerType.AI_EASY,
            '2': PlayerType.AI_MEDIUM,
            '3': PlayerType.AI_HARD
        }
        difficulty = difficulty_map.get(difficulty_choice, PlayerType.AI_MEDIUM)

        print("\nВыберите цвет:")
        print("1. Белые")
        print("2. Черные")

        color_choice = input("Выбор: ").strip()

        if color_choice == '1':
            player = Player(player_name, PieceColor.WHITE)
            ai_player = Player("Компьютер", PieceColor.BLACK, difficulty)
        else:
            player = Player(player_name, PieceColor.BLACK)
            ai_player = Player("Компьютер", PieceColor.WHITE, difficulty)

        white_player = player if player.get_color() == PieceColor.WHITE else ai_player
        black_player = ai_player if ai_player.get_color() == PieceColor.BLACK else player

        self._game = ChessGame(white_player, black_player)
        self._ai = ChessAI(difficulty)
        print("\n✓ Игра начата!")

    def _load_game(self):
        """Загрузить игру"""
        saved_games = self._save_manager.list_saved_games()

        if not saved_games:
            print("\n✗ Нет сохраненных игр")
            return

        print("\n=== Сохраненные игры ===")
        for i, game_file in enumerate(saved_games, 1):
            print(f"{i}. {game_file}")

        choice = input("\nВыберите игру (или 0 для отмены): ").strip()

        if choice == '0':
            return

        try:
            index = int(choice) - 1
            if 0 <= index < len(saved_games):
                self._game = self._save_manager.load_game(saved_games[index])
        except (ValueError, IndexError):
            print("✗ Некорректный выбор")

    def _game_loop(self):
        """Основной игровой цикл"""
        self._game.get_board().display()
        self._game.display_status()

        # Проверка окончания игры
        if self._game.get_status() not in [GameStatus.IN_PROGRESS, GameStatus.CHECK]:
            self._game_over()
            return

        current_player = self._game.get_current_player()

        # Ход ИИ
        if current_player.get_player_type() != PlayerType.HUMAN and self._ai:
            print(f"\n{current_player.get_name()} думает...")
            move = self._ai.get_best_move(self._game, current_player.get_color())

            if move:
                from_pos, to_pos = move
                try:
                    made_move = self._game.make_move(from_pos, to_pos)
                    print(f"Ход: {made_move.to_algebraic()}")
                except ChessException as e:
                    print(f"ИИ ошибка: {str(e)}")
            return

        # Ход игрока
        print(f"\nХод: {current_player.get_name()} ({current_player.get_color().get_display_name()})")
        print("Введите ход (например: e2e4) или команду (help, save, resign, draw, back)")

        user_input = input("> ").strip().lower()

        if user_input == 'help':
            self._show_help()
        elif user_input == 'save':
            self._save_game()
        elif user_input == 'resign':
            self._game.resign(current_player.get_color())
        elif user_input == 'draw':
            confirm = input("Предложить ничью? (y/n): ")
            if confirm.lower() == 'y':
                self._game.offer_draw()
        elif user_input == 'back':
            self._game = None
        else:
            from_pos, to_pos = parse_move_input(user_input)

            if not from_pos or not to_pos:
                print("✗ Некорректный формат хода")
                return

            try:
                # Проверка превращения пешки
                piece = self._game.get_board().get_piece(*from_pos)
                promotion = None

                if piece and piece.get_type() == PieceType.PAWN:
                    if (piece.get_color() == PieceColor.WHITE and to_pos[0] == 0) or \
                            (piece.get_color() == PieceColor.BLACK and to_pos[0] == 7):
                        promotion = self._ask_promotion()

                made_move = self._game.make_move(from_pos, to_pos, promotion)
                print(f"\n✓ Ход: {made_move.to_algebraic()}")

            except ChessException as e:
                print(f"✗ {str(e)}")

    def _ask_promotion(self):
        """Спросить в какую фигуру превратить пешку"""
        print("\nВо что превратить пешку?")
        print("1. Ферзь (Q)")
        print("2. Ладья (R)")
        print("3. Слон (B)")
        print("4. Конь (N)")

        choice = input("Выбор (по умолчанию Ферзь): ").strip()

        promotion_map = {
            '1': PieceType.QUEEN,
            '2': PieceType.ROOK,
            '3': PieceType.BISHOP,
            '4': PieceType.KNIGHT,
            'q': PieceType.QUEEN,
            'r': PieceType.ROOK,
            'b': PieceType.BISHOP,
            'n': PieceType.KNIGHT
        }

        return promotion_map.get(choice.lower(), PieceType.QUEEN)

    def _save_game(self):
        """Сохранить игру"""
        filename = input("Имя файла (или Enter для автоматического): ").strip()
        if filename and not filename.endswith('.json'):
            filename += '.json'

        self._save_manager.save_game(self._game, filename)

    def _game_over(self):
        """Игра окончена"""
        print("\n" + "=" * 50)
        print("ИГРА ОКОНЧЕНА".center(50))
        print("=" * 50)

        status = self._game.get_status()
        print(f"\nРезультат: {status.get_display_name()}")

        if status == GameStatus.CHECKMATE_WHITE:
            print(f"Победа: {self._game._white_player.get_name()}")
        elif status == GameStatus.CHECKMATE_BLACK:
            print(f"Победа: {self._game._black_player.get_name()}")

        print(f"\nВсего ходов: {self._game._move_count}")

        save = input("\nСохранить игру? (y/n): ")
        if save.lower() == 'y':
            self._save_game()

        self._game = None

    def _show_help(self):
        """Показать справку"""
        print("\n=== Справка ===")
        print("Формат хода: e2e4 или e2-e4")
        print("Рокировка: e1g1 (королевская), e1c1 (ферзевая)")
        print("\nКоманды:")
        print("  help - показать справку")
        print("  save - сохранить игру")
        print("  resign - сдаться")
        print("  draw - предложить ничью")
        print("  back - вернуться в меню")
        print("---")


def main():
    ui = ChessUI()
    ui.run()


if __name__ == "__main__":
    main()