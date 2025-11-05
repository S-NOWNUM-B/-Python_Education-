from enum import Enum


# Перечисление для единиц измерения температуры
class TemperatureUnit(Enum):
    CELSIUS = "celsius"
    FAHRENHEIT = "fahrenheit"
    KELVIN = "kelvin"


# Класс для хранения температуры
class Temperature:
    def __init__(self, value, unit):
        self._value = value
        self._unit = unit

    # Геттеры
    def get_value(self):
        return self._value

    def get_unit(self):
        return self._unit

    # Метод для отображения температуры
    def display(self):
        unit_symbols = {
            TemperatureUnit.CELSIUS: "°C",
            TemperatureUnit.FAHRENHEIT: "°F",
            TemperatureUnit.KELVIN: "K"
        }
        unit_symbol = unit_symbols[self._unit]
        return f"{self._value:.2f}{unit_symbol}"


# Класс конвертера температуры
class TemperatureConverter:

    # Конвертация из Цельсия в Фаренгейт
    def celsius_to_fahrenheit(self, celsius):
        return celsius * 9.0 / 5.0 + 32

    # Конвертация из Цельсия в Кельвин
    def celsius_to_kelvin(self, celsius):
        return celsius + 273.15

    # Конвертация из Фаренгейта в Цельсий
    def fahrenheit_to_celsius(self, fahrenheit):
        return (fahrenheit - 32) * 5.0 / 9.0

    # Конвертация из Фаренгейта в Кельвин
    def fahrenheit_to_kelvin(self, fahrenheit):
        return (fahrenheit - 32) * 5.0 / 9.0 + 273.15

    # Конвертация из Кельвина в Цельсий
    def kelvin_to_celsius(self, kelvin):
        return kelvin - 273.15

    # Конвертация из Кельвина в Фаренгейт
    def kelvin_to_fahrenheit(self, kelvin):
        return (kelvin - 273.15) * 9.0 / 5.0 + 32

    # Универсальный метод конвертации
    def convert(self, temperature, target_unit):
        value = temperature.get_value()
        source_unit = temperature.get_unit()

        # Если единицы совпадают, возвращаем исходную температуру
        if source_unit == target_unit:
            return temperature

        result = 0

        # Конвертация в зависимости от исходной и целевой единицы
        if source_unit == TemperatureUnit.CELSIUS:
            if target_unit == TemperatureUnit.FAHRENHEIT:
                result = self.celsius_to_fahrenheit(value)
            elif target_unit == TemperatureUnit.KELVIN:
                result = self.celsius_to_kelvin(value)
        elif source_unit == TemperatureUnit.FAHRENHEIT:
            if target_unit == TemperatureUnit.CELSIUS:
                result = self.fahrenheit_to_celsius(value)
            elif target_unit == TemperatureUnit.KELVIN:
                result = self.fahrenheit_to_kelvin(value)
        elif source_unit == TemperatureUnit.KELVIN:
            if target_unit == TemperatureUnit.CELSIUS:
                result = self.kelvin_to_celsius(value)
            elif target_unit == TemperatureUnit.FAHRENHEIT:
                result = self.kelvin_to_fahrenheit(value)

        return Temperature(result, target_unit)


# Класс для работы с пользовательским интерфейсом
class ConverterUI:
    def __init__(self):
        self.converter = TemperatureConverter()

    def run(self):
        print("=== Конвертер температуры ===\n")

        while True:
            try:
                # Ввод исходной температуры
                source_temp = self._get_temperature_input()

                # Выбор целевой единицы
                target_unit = self._get_target_unit(source_temp.get_unit())

                # Конвертация
                result = self.converter.convert(source_temp, target_unit)

                # Вывод результата
                print(f"\nРезультат: {source_temp.display()} = {result.display()}")

                # Продолжить или выйти
                if not self._ask_continue():
                    break

                print()

            except ValueError as e:
                print(f"Ошибка: {e}. Пожалуйста, попробуйте снова.\n")
            except KeyboardInterrupt:
                print("\n\nПрограмма прервана.")
                break
            except Exception as e:
                print("Ошибка: Некорректный ввод. Пожалуйста, попробуйте снова.\n")

        print("Спасибо за использование конвертера температуры!")

    # Метод для ввода температуры
    def _get_temperature_input(self):
        print("Выберите исходную единицу измерения:")
        print("1. Цельсий (°C)")
        print("2. Фаренгейт (°F)")
        print("3. Кельвин (K)")
        choice = int(input("Введите выбор (1-3): "))

        unit = self._get_unit_from_choice(choice)

        value = float(input("Введите значение температуры: "))

        # Валидация для Кельвина (не может быть меньше 0)
        if unit == TemperatureUnit.KELVIN and value < 0:
            raise ValueError("Кельвин не может быть отрицательным")

        # Валидация для абсолютного нуля в Цельсиях
        if unit == TemperatureUnit.CELSIUS and value < -273.15:
            raise ValueError("Температура не может быть ниже абсолютного нуля (-273.15°C)")

        # Валидация для абсолютного нуля в Фаренгейтах
        if unit == TemperatureUnit.FAHRENHEIT and value < -459.67:
            raise ValueError("Температура не может быть ниже абсолютного нуля (-459.67°F)")

        return Temperature(value, unit)

    # Метод для выбора целевой единицы
    def _get_target_unit(self, source_unit):
        print("\nВыберите целевую единицу измерения:")

        available_units = [unit for unit in TemperatureUnit if unit != source_unit]

        for i, unit in enumerate(available_units, 1):
            unit_names = {
                TemperatureUnit.CELSIUS: "Цельсий (°C)",
                TemperatureUnit.FAHRENHEIT: "Фаренгейт (°F)",
                TemperatureUnit.KELVIN: "Кельвин (K)"
            }
            print(f"{i}. {unit_names[unit]}")

        choice = int(input("Введите выбор: "))

        if 1 <= choice <= len(available_units):
            return available_units[choice - 1]
        else:
            raise ValueError("Некорректный выбор")

    # Преобразование номера выбора в единицу измерения
    def _get_unit_from_choice(self, choice):
        units = {
            1: TemperatureUnit.CELSIUS,
            2: TemperatureUnit.FAHRENHEIT,
            3: TemperatureUnit.KELVIN
        }

        if choice not in units:
            raise ValueError("Некорректный выбор")

        return units[choice]

    # Спросить пользователя, хочет ли он продолжить
    def _ask_continue(self):
        answer = input("\nКонвертировать еще одну температуру? (д/н): ").lower()
        return answer in ['д', 'да', 'y', 'yes']


# Главная функция
def main():
    ui = ConverterUI()
    ui.run()


if __name__ == "__main__":
    main()