from abc import ABC, abstractmethod

# Интерфейс для операций
class Operation(ABC):
    @abstractmethod
    def execute(self, num1, num2):
        pass

# Класс для сложения
class Addition(Operation):
    def execute(self, num1, num2):
        return num1 + num2

# Класс для вычитания
class Subtraction(Operation):
    def execute(self, num1, num2):
        return num1 - num2

# Класс для умножения
class Multiplication(Operation):
    def execute(self, num1, num2):
        return num1 * num2

# Класс для деления
class Division(Operation):
    def execute(self, num1, num2):
        if num2 == 0:
            raise ArithmeticError("Делить на ноль нельзя")
        return num1 / num2

# Класс для остатка от деления
class Modulo(Operation):
    def execute(self, num1, num2):
        if num2 == 0:
            raise ArithmeticError("Делить на ноль нельзя")
        return num1 % num2

# Основной класс калькулятора
class Calculator:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2
        self.operation = None

    def set_operation(self, operation):
        self.operation = operation

    def calculate(self):
        if self.operation is None:
            raise ValueError("Операция не установлена")
        return self.operation.execute(self.num1, self.num2)

# Класс для работы с пользовательским вводом
class CalculatorUI:
    def __init__(self):
        pass

    def run(self):
        print("=== Калькулятор ===")

        try:
            num1 = float(input("Введите первое число: "))
            num2 = float(input("Введите второе число: "))
            operator = input("Введите действие (+, -, *, /, %): ")

            calculator = Calculator(num1, num2)

            operation = self._get_operation(operator)
            calculator.set_operation(operation)
            result = calculator.calculate()
            print(f"Результат: {result}")

        except ValueError as e:
            if "Операция не установлена" in str(e):
                print("Операция не установлена")
            elif "Неверный оператор" in str(e):
                print("Неверный оператор")
            else:
                print("Неверный ввод. Пожалуйста, введите корректные числа.")
        except ArithmeticError as e:
            print(e)
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    def _get_operation(self, operator):
        operations = {
            '+': Addition(),
            '-': Subtraction(),
            '*': Multiplication(),
            '/': Division(),
            '%': Modulo()
        }

        if operator not in operations:
            raise ValueError("Неверный оператор")

        return operations[operator]

# Главная функция
def main():
    ui = CalculatorUI()
    ui.run()

if __name__ == "__main__":
    main()
