import random

#Класс игры
class Game():
    def __init__(self):
        self._secret_number = 0
        self._attempts = 0
        self._is_game_won = False
        self.generate_number()

    #Метод генерации случайного числа
    def generate_number(self):
        self._secret_number = random.randint(1, 100)

    #Метод проверки попытки
    def check_guess(self, user_guess):
        self._attempts += 1

        if user_guess < 1 or user_guess > 100:
            return "Число должно быть от 1 до 100"

        if user_guess < self._secret_number:
            return "Слишком мало! Попробуйте число по больше"
        elif user_guess > self._secret_number:
            return "Слишком много! Попробуйте число по меньше"
        else:
            self._is_game_won = True
            return "Поздравляем! Вы угадали число!"

    #Геттер для количества попыток
    def get_attempts(self):
        return self._attempts

    #Геттер для проверки победы
    def is_won(self):
        return self._is_game_won

    #Метод сброса игры
    def reset(self):
        self._attempts = 0
        self._is_game_won = False
        self.generate_number()

# Класс для работы с пользовательским интерфейсом
class GameUI:
    def __init__(self):
        self.game = Game()

    #Основной цикл игры
    def run(self):
        print("=== Игра 'Угадай число' ===")

        print("Я загадал число от 1 до 100")
        print("Попробуй его отгадать!\n")

        while not self.game.is_won():
            try:
                user_guess = int(input("Введите число: "))
                result = self.game.check_guess(user_guess)
                print(result)
            except ValueError:
                print("Пожалуйста, введите корректное число")
            except KeyboardInterrupt:
                print("\n\n Игра прервана. До свидания!")
                return

        print(f"Количество попыток: {self.game.is_won()}")

        self._play_again()

    #Метод повтора игры
    def _play_again(self):
        answer = input("\nХотите сыграть ещё раз? (д/н): ").lower()

        if answer in ('да', 'yes', 'д', 'y'):
            self.game.reset()
            print("\n=== Новая игра ===")
            self.run()
        else:
            print("Спасибо за игру!")

#Главная функция
def main():
    ui = GameUI()
    ui.run()

if __name__ == '__main__':
    main()