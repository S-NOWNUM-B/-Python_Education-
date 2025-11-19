from enum import Enum


# Класс игрока
class Player:
    def __init__(self, name, symbol):
        self._name = name
        self._symbol = symbol
        self._wins = 0

    # Геттеры
    def get_name(self):
        return self._name

    def get_symbol(self):
        return self._symbol

    def get_wins(self):
        return self._wins

    # Метод увеличения счетчика побед
    def increment_wins(self):
        self._wins += 1

    # Метод отображения информации о игроке
    def display_info(self):
        print(f"{self._name} ({self._symbol}) - Wins: {self._wins}")


# Класс игрового поля
class Board:
    def __init__(self):
        self._SIZE = 3
        self._grid = []
        self._moves_count = 0
        self._initialize_board()

    # Метод инициализации доски
    def _initialize_board(self):
        self._grid = [[' ' for _ in range(self._SIZE)] for _ in range(self._SIZE)]

    # Метод сброса доски
    def reset(self):
        self._initialize_board()
        self._moves_count = 0

    # Метод отображения доски
    def display(self):
        print("\n     1   2   3")
        print("   +---+---+---+")

        for row in range(self._SIZE):
            print(f" {row + 1} ", end="")
            for col in range(self._SIZE):
                print(f"| {self._grid[row][col]} ", end="")
            print("|")
            print("   +---+---+---+")
        print()

    # Метод отображения доски с инструкцией
    def display_with_guide(self):
        print("\n=== Game Board ===")
        self.display()
        print("Enter row (1-3) and column (1-3) to make a move")

    # Метод проверки, свободна ли клетка
    def is_cell_empty(self, row, col):
        if row < 0 or row >= self._SIZE or col < 0 or col >= self._SIZE:
            return False
        return self._grid[row][col] == ' '

    # Метод совершения хода
    def make_move(self, row, col, symbol):
        if not self.is_cell_empty(row, col):
            return False

        self._grid[row][col] = symbol
        self._moves_count += 1
        return True

    # Метод проверки заполненности доски
    def is_full(self):
        return self._moves_count >= self._SIZE * self._SIZE

    # Метод проверки победы по горизонтали
    def _check_rows(self, symbol):
        for row in range(self._SIZE):
            if all(self._grid[row][col] == symbol for col in range(self._SIZE)):
                return True
        return False

    # Метод проверки победы по вертикали
    def _check_columns(self, symbol):
        for col in range(self._SIZE):
            if all(self._grid[row][col] == symbol for row in range(self._SIZE)):
                return True
        return False

    # Метод проверки победы по диагоналям
    def _check_diagonals(self, symbol):
        # Главная диагональ (слева-направо)
        if all(self._grid[i][i] == symbol for i in range(self._SIZE)):
            return True

        # Побочная диагональ (справа-налево)
        if all(self._grid[i][self._SIZE - 1 - i] == symbol for i in range(self._SIZE)):
            return True

        return False

    # Метод проверки победителя
    def check_winner(self, symbol):
        return self._check_rows(symbol) or self._check_columns(symbol) or self._check_diagonals(symbol)

    # Метод получения количества сделанных ходов
    def get_moves_count(self):
        return self._moves_count

    # Метод получения размера доски
    def get_size(self):
        return self._SIZE


# Перечисление состояния игры
class GameState(Enum):
    IN_PROGRESS = 1
    PLAYER1_WON = 2
    PLAYER2_WON = 3
    DRAW = 4


# Класс игры
class Game:
    def __init__(self, player1, player2):
        self._board = Board()
        self._player1 = player1
        self._player2 = player2
        self._current_player = player1
        self._state = GameState.IN_PROGRESS
        self._games_played = 0
        self._draws = 0

    # Метод начала новой игры
    def start_new_game(self):
        self._board.reset()
        self._current_player = self._player1
        self._state = GameState.IN_PROGRESS
        self._games_played += 1

    # Метод совершения хода
    def make_move(self, row, col):
        # Конвертируем из 1-based в 0-based индексацию
        row -= 1
        col -= 1

        # Проверяем валидность хода
        if row < 0 or row >= self._board.get_size() or col < 0 or col >= self._board.get_size():
            print("Error: Position outside board boundaries!")
            return False

        if not self._board.is_cell_empty(row, col):
            print("Error: Cell already occupied!")
            return False

        # Совершаем ход
        self._board.make_move(row, col, self._current_player.get_symbol())
        return True

    # Метод проверки состояния игры
    def check_game_state(self):
        # Проверка на победу текущего игрока
        if self._board.check_winner(self._current_player.get_symbol()):
            if self._current_player == self._player1:
                self._state = GameState.PLAYER1_WON
                self._player1.increment_wins()
            else:
                self._state = GameState.PLAYER2_WON
                self._player2.increment_wins()
            return

        # Проверка на ничью
        if self._board.is_full():
            self._state = GameState.DRAW
            self._draws += 1
            return

        self._state = GameState.IN_PROGRESS

    # Метод смены игрока
    def switch_player(self):
        self._current_player = self._player2 if self._current_player == self._player1 else self._player1

    # Метод получения текущего игрока
    def get_current_player(self):
        return self._current_player

    # Метод получения доски
    def get_board(self):
        return self._board

    # Метод получения состояния игры
    def get_state(self):
        return self._state

    # Метод проверки, закончена ли игра
    def is_game_over(self):
        return self._state != GameState.IN_PROGRESS

    # Метод отображения результата игры
    def display_result(self):
        self._board.display()

        if self._state == GameState.PLAYER1_WON:
            print(f"🎉 {self._player1.get_name()} ({self._player1.get_symbol()}) WINS!")
        elif self._state == GameState.PLAYER2_WON:
            print(f"🎉 {self._player2.get_name()} ({self._player2.get_symbol()}) WINS!")
        elif self._state == GameState.DRAW:
            print("🤝 It's a DRAW!")

    # Метод отображения статистики
    def display_statistics(self):
        print("\n=== Game Statistics ===")
        print(f"Total games played: {self._games_played}")
        self._player1.display_info()
        self._player2.display_info()
        print(f"Draws: {self._draws}")

        if self._games_played > 0:
            print(f"\n{self._player1.get_name()} win rate: {self._player1.get_wins() / self._games_played * 100:.1f}%")
            print(f"{self._player2.get_name()} win rate: {self._player2.get_wins() / self._games_played * 100:.1f}%")


# Класс для работы с пользовательским интерфейсом
class TicTacToeUI:
    def __init__(self):
        self._game = None

    def run(self):
        print("=== Tic-Tac-Toe Game ===\n")

        # Создание игроков
        player1 = self._create_player(1, 'X')
        player2 = self._create_player(2, 'O')

        self._game = Game(player1, player2)

        # Главное меню
        while True:
            self._display_main_menu()

            try:
                choice = int(input())

                if choice == 1:
                    self._play_game()
                elif choice == 2:
                    self._game.display_statistics()
                elif choice == 3:
                    print("\nThanks for playing!")
                    return
                else:
                    print("Invalid choice. Please try again.")
            except Exception:
                print("\nError: Invalid input. Please try again.")

    # Метод создания игрока
    def _create_player(self, player_number, symbol):
        name = input(f"Enter name for Player {player_number} ({symbol}): ")
        return Player(name, symbol)

    # Метод отображения главного меню
    def _display_main_menu(self):
        print("\n=== Main Menu ===")
        print("1. Play Game")
        print("2. View Statistics")
        print("3. Exit")
        print("Enter choice (1-3): ", end='')

    # Метод игрового процесса
    def _play_game(self):
        self._game.start_new_game()

        print("\n=== New Game Started ===")
        self._game.get_board().display_with_guide()

        # Игровой цикл
        while not self._game.is_game_over():
            current = self._game.get_current_player()

            print(f"\n{current.get_name()}'s turn ({current.get_symbol()})")

            try:
                row = int(input("Enter row (1-3): "))
                col = int(input("Enter column (1-3): "))

                # Попытка совершить ход
                if self._game.make_move(row, col):
                    self._game.get_board().display()
                    self._game.check_game_state()

                    if not self._game.is_game_over():
                        self._game.switch_player()
                else:
                    print("Try again!")

            except Exception:
                print("\nError: Invalid input. Please enter numbers 1-3.")

        # Отображение результата
        self._game.display_result()

        # Спросить, хотят ли игроки сыграть снова
        answer = input("\nPlay again? (y/n): ").lower()

        if answer in ['y', 'yes']:
            self._play_game()

# Главная функция
def main():
    ui = TicTacToeUI()
    ui.run()

if __name__ == "__main__":
    main()