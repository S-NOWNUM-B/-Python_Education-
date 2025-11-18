# Класс для хранения статистики текста
class TextStatistics:
    def __init__(self, word_count, char_count, sentence_count, paragraph_count):
        self._word_count = word_count
        self._char_count = char_count
        self._sentence_count = sentence_count
        self._paragraph_count = paragraph_count

    # Геттеры
    def get_word_count(self):
        return self._word_count

    def get_char_count(self):
        return self._char_count

    def get_sentence_count(self):
        return self._sentence_count

    def get_paragraph_count(self):
        return self._paragraph_count

    # Метод для отображения статистики
    def display(self):
        print("\n=== Статистика текста ===")
        print(f"Слов: {self._word_count}")
        print(f"Символов (с пробелами): {self._char_count}")

        chars_without_spaces = self._count_chars_without_spaces()
        print(f"Символов (без пробелов): {chars_without_spaces}")
        print(f"Предложений: {self._sentence_count}")
        print(f"Параграфов: {self._paragraph_count}")

        if self._word_count > 0:
            avg_word_length = chars_without_spaces / self._word_count
            print(f"Средняя длина слова: {avg_word_length:.2f} символов")

    # Вспомогательный метод для подсчета символов без пробелов
    def _count_chars_without_spaces(self):
        # Упрощенная оценка: символы минус примерное количество пробелов
        return self._char_count - (self._word_count - 1) if self._word_count > 0 else self._char_count


# Класс анализатора текста
class TextAnalyzer:

    # Метод подсчета слов
    def count_words(self, text):
        if not text or not text.strip():
            return 0

        # Разделение по пробельным символам
        words = text.strip().split()
        return len(words)

    # Метод подсчета символов
    def count_chars(self, text):
        if text is None:
            return 0
        return len(text)

    # Метод подсчета предложений
    def count_sentences(self, text):
        if not text or not text.strip():
            return 0

        # Подсчет предложений по знакам: . ! ?
        count = 0
        last_was_punctuation = False

        for char in text:
            # Проверка на конец предложения
            if char in '.!?':
                if not last_was_punctuation:
                    count += 1
                    last_was_punctuation = True
            elif not char.isspace():
                last_was_punctuation = False

        return count

    # Метод подсчета параграфов
    def count_paragraphs(self, text):
        if not text or not text.strip():
            return 0

        # Параграфы разделяются пустыми строками (двойной перевод строки)
        import re
        paragraphs = re.split(r'\n\s*\n', text.strip())
        return len([p for p in paragraphs if p.strip()])

    # Универсальный метод анализа текста
    def analyze(self, text):
        words = self.count_words(text)
        chars = self.count_chars(text)
        sentences = self.count_sentences(text)
        paragraphs = self.count_paragraphs(text)

        return TextStatistics(words, chars, sentences, paragraphs)


# Класс для чтения текста из файла
class FileTextReader:

    # Метод чтения файла
    def read_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        except Exception as e:
            raise Exception(f"Ошибка при чтении файла: {e}")


# Класс для работы с пользовательским интерфейсом
class AnalyzerUI:
    def __init__(self):
        self.analyzer = TextAnalyzer()
        self.file_reader = FileTextReader()

    def run(self):
        print("=== Анализатор текста ===\n")

        while True:
            try:
                # Выбор источника текста
                text = self._get_text_input()

                if text is None:
                    break

                # Анализ текста
                stats = self.analyzer.analyze(text)

                # Вывод результата
                stats.display()

                # Продолжить или выйти
                if not self._ask_continue():
                    break

                print()

            except Exception as e:
                print(f"Ошибка: {e}\n")

        print("Спасибо за использование анализатора текста!")

    # Метод для выбора способа ввода текста
    def _get_text_input(self):
        print("Выберите способ ввода:")
        print("1. Ввести текст вручную")
        print("2. Прочитать из файла")
        print("3. Выход")

        try:
            choice = int(input("Введите выбор (1-3): "))

            if choice == 1:
                return self._get_manual_input()
            elif choice == 2:
                return self._get_file_input()
            elif choice == 3:
                return None
            else:
                raise ValueError("Некорректный выбор")
        except ValueError as e:
            raise ValueError("Некорректный ввод")

    # Метод для ввода текста вручную
    def _get_manual_input(self):
        print("\nВведите ваш текст (введите 'END' на новой строке для завершения):")
        lines = []

        while True:
            line = input()
            if line == "END":
                break
            lines.append(line)

        return "\n".join(lines)

    # Метод для чтения текста из файла
    def _get_file_input(self):
        file_path = input("\nВведите путь к файлу: ")

        text = self.file_reader.read_file(file_path)
        print("Файл успешно загружен!")

        return text

    # Спросить пользователя, хочет ли он продолжить
    def _ask_continue(self):
        answer = input("\nАнализировать другой текст? (д/н): ").lower()
        return answer in ['д', 'да', 'y', 'yes']


# Главная функция
def main():
    ui = AnalyzerUI()
    ui.run()


if __name__ == "__main__":
    main()
