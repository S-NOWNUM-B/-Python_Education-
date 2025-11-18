"""
Главный файл приложения
"""

from bank import Bank
from user import User
from account import SavingsAccount, CheckingAccount, CreditAccount
from exceptions import (
    BankingException,
    AuthenticationException,
    InvalidPasswordException
)
from utils import validate_email, validate_password_strength, parse_date


class BankingSystemUI:
    def __init__(self):
        self._bank = Bank("Freedom-банк")
        self._current_user = None
        self._initialize_sample_data()

    def _initialize_sample_data(self):
        """Инициализация примерных данных"""
        try:
            # Создание пользователя
            user1 = User("ivan_petrov", "Password123", "Иван Петров", "ivan@example.com")
            self._bank.register_user(user1)

            # Создание счетов
            savings = SavingsAccount(5000)
            checking = CheckingAccount(2000, overdraft_protection=True)
            credit = CreditAccount(10000)

            user1.add_account(savings)
            user1.add_account(checking)
            user1.add_account(credit)

            # Создание второго пользователя
            user2 = User("maria_ivanova", "SecurePass456", "Мария Иванова", "maria@example.com")
            self._bank.register_user(user2)

            checking2 = CheckingAccount(3000)
            user2.add_account(checking2)

        except BankingException as e:
            print(f"Ошибка инициализации: {str(e)}")

    def run(self):
        """Запуск приложения"""
        print("╔════════════════════════════════════════╗")
        print("║  Банковская система                    ║")
        print("╚════════════════════════════════════════╝\n")

        while True:
            try:
                if not self._current_user or not self._current_user.is_authenticated():
                    self._display_login_menu()
                    choice = int(input())

                    if choice == 4:
                        print("\nДо свидания!")
                        break

                    self._handle_login_menu(choice)
                else:
                    self._display_main_menu()
                    choice = int(input())

                    if choice == 15:
                        self._current_user.logout()
                        self._current_user = None
                        continue

                    self._handle_main_menu(choice)

            except ValueError:
                print("\nОшибка: Неверный ввод. Попробуйте снова.")
            except BankingException as e:
                print(f"\n✗ Ошибка: {str(e)}")
            except Exception as e:
                print(f"\n✗ Непредвиденная ошибка: {str(e)}")

    def _display_login_menu(self):
        """Меню входа"""
        print("\n=== Меню входа ===")
        print("1. Войти")
        print("2. Зарегистрироваться")
        print("3. О банке")
        print("4. Выход")
        print("Выбор: ", end='')

    def _handle_login_menu(self, choice):
        """Обработка меню входа"""
        if choice == 1:
            self._login()
        elif choice == 2:
            self._register()
        elif choice == 3:
            self._bank.display_statistics()

    def _login(self):
        """Вход в систему"""
        username = input("\nИмя пользователя: ")
        password = input("Пароль: ")

        user = self._bank.find_user(username)
        if not user:
            raise AuthenticationException("Пользователь не найден")

        user.login(username, password)
        self._current_user = user

    def _register(self):
        """Регистрация"""
        print("\n=== Регистрация ===")
        username = input("Имя пользователя: ")

        # Проверка занятости username
        if self._bank.find_user(username):
            print("✗ Это имя пользователя уже занято")
            return

        # Ввод пароля с проверкой
        while True:
            password = input("Пароль (мин. 8 символов, буквы и цифры): ")
            is_valid, message = validate_password_strength(password)
            if is_valid:
                break
            print(f"✗ {message}")

        full_name = input("Полное имя: ")

        # Ввод email с проверкой
        while True:
            email = input("Email: ")
            if validate_email(email):
                break
            print("✗ Некорректный email")

        # Создание пользователя
        user = User(username, password, full_name, email)
        self._bank.register_user(user)

        # Создание первого счета
        print("\nВыберите тип первого счета:")
        print("1. Сберегательный")
        print("2. Текущий")
        print("3. Кредитный")

        account_type = int(input("Выбор: "))
        initial_balance = float(input("Начальный баланс (0 для пропуска): ") or "0")

        if account_type == 1:
            account = SavingsAccount(initial_balance)
        elif account_type == 2:
            overdraft = input("Подключить овердрафт? (y/n): ").lower() == 'y'
            account = CheckingAccount(initial_balance, overdraft)
        elif account_type == 3:
            limit = float(input("Кредитный лимит: "))
            account = CreditAccount(limit)
        else:
            print("Некорректный выбор")
            return

        user.add_account(account)
        print(f"\n✓ Регистрация завершена! Можете войти в систему.")

    def _display_main_menu(self):
        """Главное меню"""
        print(f"\n=== Главное меню ({self._current_user.get_username()}) ===")
        print("1. Мои счета")
        print("2. Создать счет")
        print("3. Детали счета")
        print("4. Пополнить счет")
        print("5. Снять средства")
        print("6. Перевод между счетами")
        print("7. История транзакций")
        print("8. Выписка по счету")
        print("9. Профиль пользователя")
        print("10. Изменить пароль")
        print("11. Применить проценты")
        print("12. Списать комиссии")
        print("13. Проверка на мошенничество")
        print("14. Статистика банка")
        print("15. Выйти")
        print("Выбор: ", end='')

    def _handle_main_menu(self, choice):
        """Обработка главного меню"""
        actions = {
            1: self._view_accounts,
            2: self._create_account,
            3: self._view_account_details,
            4: self._deposit,
            5: self._withdraw,
            6: self._transfer,
            7: self._view_transactions,
            8: self._generate_statement,
            9: self._view_profile,
            10: self._change_password,
            11: self._apply_interest,
            12: self._charge_fees,
            13: self._check_fraud,
            14: self._bank.display_statistics
        }

        if choice in actions:
            actions[choice]()
        else:
            print("Неверный выбор")

    def _view_accounts(self):
        """Просмотр счетов"""
        self._current_user.display_accounts()

    def _create_account(self):
        """Создание счета"""
        print("\nВыберите тип счета:")
        print("1. Сберегательный (4% годовых)")
        print("2. Текущий (овердрафт)")
        print("3. Кредитный")

        account_type = int(input("Выбор: "))

        if account_type == 1:
            balance = float(input("Начальный баланс: ") or "0")
            account = SavingsAccount(balance)
        elif account_type == 2:
            balance = float(input("Начальный баланс: ") or "0")
            overdraft = input("Подключить овердрафт? (y/n): ").lower() == 'y'
            account = CheckingAccount(balance, overdraft)
        elif account_type == 3:
            limit = float(input("Кредитный лимит: "))
            account = CreditAccount(limit)
        else:
            print("Некорректный выбор")
            return

        self._current_user.add_account(account)

    def _view_account_details(self):
        """Детали счета"""
        account_number = input("\nНомер счета: ")
        account = self._current_user.find_account(account_number)

        if account:
            account.display_info()
        else:
            print("Счет не найден")

    def _deposit(self):
        """Пополнение"""
        account_number = input("\nНомер счета: ")
        account = self._current_user.find_account(account_number)

        if not account:
            print("Счет не найден")
            return

        amount = float(input("Сумма пополнения: "))
        description = input("Описание (опционально): ")

        transaction = account.deposit(amount, description)
        print(f"\n✓ Счет пополнен на ${amount:.2f}")
        print(f"Новый баланс: ${account.get_balance():.2f}")

    def _withdraw(self):
        """Снятие"""
        account_number = input("\nНомер счета: ")
        account = self._current_user.find_account(account_number)

        if not account:
            print("Счет не найден")
            return

        amount = float(input("Сумма снятия: "))
        description = input("Описание (опционально): ")

        transaction = account.withdraw(amount, description)
        print(f"\n✓ Снято ${amount:.2f}")
        print(f"Новый баланс: ${account.get_balance():.2f}")

    def _transfer(self):
        """Перевод"""
        from_account = input("\nС какого счета: ")
        to_account = input("На какой счет: ")
        amount = float(input("Сумма: "))
        description = input("Описание (опционально): ")

        self._bank.transfer(from_account, to_account, amount, description)

    def _view_transactions(self):
        """История транзакций"""
        account_number = input("\nНомер счета: ")
        account = self._current_user.find_account(account_number)

        if not account:
            print("Счет не найден")
            return

        limit_str = input("Количество последних транзакций (Enter для всех): ")
        limit = int(limit_str) if limit_str.strip() else None

        transactions = account.get_transaction_history()
        if limit:
            transactions = transactions[-limit:]

        print(f"\n=== История транзакций {account_number} ===")
        for transaction in reversed(transactions):
            transaction.display()
        print(f"\nВсего: {len(transactions)}")

    def _generate_statement(self):
        """Выписка"""
        account_number = input("\nНомер счета: ")

        start_str = input("Дата начала (ГГГГ-ММ-ДД) или Enter: ").strip()
        end_str = input("Дата окончания (ГГГГ-ММ-ДД) или Enter: ").strip()

        start_date = parse_date(start_str) if start_str else None
        end_date = parse_date(end_str) if end_str else None

        self._bank.generate_statement(account_number, start_date, end_date)

    def _view_profile(self):
        """Профиль"""
        self._current_user.display_info()

    def _change_password(self):
        """Изменение пароля"""
        old_password = input("\nТекущий пароль: ")

        while True:
            new_password = input("Новый пароль: ")
            is_valid, message = validate_password_strength(new_password)
            if is_valid:
                break
            print(f"✗ {message}")

        self._current_user.change_password(old_password, new_password)

    def _apply_interest(self):
        """Применить проценты"""
        self._bank.apply_interest_to_all()

    def _charge_fees(self):
        """Списать комиссии"""
        self._bank.charge_monthly_fees()

    def _check_fraud(self):
        """Проверка на мошенничество"""
        self._bank.detect_fraud_for_user(self._current_user.get_username())


def main():
    app = BankingSystemUI()
    app.run()


if __name__ == "__main__":
    main()