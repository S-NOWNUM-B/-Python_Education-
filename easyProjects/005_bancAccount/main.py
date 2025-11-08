class Account:
    def __init__(self, account_number, owner_name, initial_balance):
        self._account_number = account_number
        self._owner_name = owner_name
        self._balance = initial_balance if initial_balance >= 0 else 0
        self._transaction_history = []

        if initial_balance > 0:
            self._transaction_history.append(f"Initial deposit: ${initial_balance:.2f}")

    # Геттеры
    def get_account_number(self):
        return self._account_number

    def get_owner_name(self):
        return self._owner_name

    def get_balance(self):
        return self._balance

    # Пополнение счета
    def deposit(self, amount):
        if amount <= 0:
            print("Ошибка: Сумма пополнения должна быть положительной")
            return False
        self._balance += amount
        transaction = f"Deposit: +${amount:.2f} | New balance: ${self._balance:.2f}"
        self._transaction_history.append(transaction)
        print(f"Успешно пополнено: ${amount:.2f}")
        return True

    # Снятие средств
    def withdraw(self, amount):
        if amount <= 0:
            print("Ошибка: Сумма снятия должна быть положительной")
            return False
        if amount > self._balance:
            print("Ошибка: Недостаточно средств")
            print(f"Текущий баланс: ${self._balance:.2f}")
            print(f"Запрошенная сумма: ${amount:.2f}")
            return False
        self._balance -= amount
        transaction = f"Withdrawal: -${amount:.2f} | New balance: ${self._balance:.2f}"
        self._transaction_history.append(transaction)
        print(f"Успешно снято: ${amount:.2f}")
        return True

    # Перевод другому счету
    def transfer(self, target_account, amount):
        if amount <= 0:
            print("Ошибка: Сумма перевода должна быть положительной")
            return False
        if amount > self._balance:
            print("Ошибка: Недостаточно средств для перевода")
            return False
        self._balance -= amount
        target_account._balance += amount

        sender_transaction = (f"Transfer to {target_account.get_account_number()}: -${amount:.2f} | "
                              f"New balance: ${self._balance:.2f}")
        self._transaction_history.append(sender_transaction)

        receiver_transaction = (f"Transfer from {self._account_number}: +${amount:.2f} | "
                               f"New balance: ${target_account._balance:.2f}")
        target_account._transaction_history.append(receiver_transaction)

        print(f"Успешно переведено: ${amount:.2f}")
        return True

    # Информация о счете
    def display_account_info(self):
        print("\n=== Информация о счете ===")
        print(f"Номер счета: {self._account_number}")
        print(f"Владелец: {self._owner_name}")
        print(f"Текущий баланс: ${self._balance:.2f}")

    # История операций
    def display_transaction_history(self):
        print("\n=== История операций ===")
        if not self._transaction_history:
            print("Транзакций нет")
        else:
            for i, t in enumerate(self._transaction_history, 1):
                print(f"{i}. {t}")


class BankSystem:
    def __init__(self):
        self._accounts = []
        self._next_account_number = 1000

    # Новый счет
    def create_account(self, owner_name, initial_balance):
        account_number = f"ACC{self._next_account_number}"
        self._next_account_number += 1
        new_account = Account(account_number, owner_name, initial_balance)
        self._accounts.append(new_account)
        print("\nСчет успешно создан!")
        print(f"Номер счета: {account_number}")
        print(f"Владелец: {owner_name}")
        print(f"Начальный баланс: ${initial_balance:.2f}")
        return new_account

    # Поиск по номеру
    def find_account(self, account_number):
        for acc in self._accounts:
            if acc.get_account_number() == account_number:
                return acc
        return None

    # Информация по всем счетам
    def display_all_accounts(self):
        if not self._accounts:
            print("\nНет счетов в системе")
            return
        print("\n=== Все счета ===")
        for acc in self._accounts:
            print(f"Счет: {acc.get_account_number()} | Владелец: {acc.get_owner_name()} | Баланс: ${acc.get_balance():.2f}")


class BankUI:
    def __init__(self):
        self._bank_system = BankSystem()

    def run(self):
        print("=== Система управления банковскими счетами ===\n")
        while True:
            try:
                self._display_main_menu()
                choice = int(input())
                if choice == 9:
                    print("\nСпасибо за использование банковской системы!")
                    break
                self._handle_menu_choice(choice)
            except Exception:
                print("\nОшибка: Неверный ввод. Попробуйте еще раз.")

    def _display_main_menu(self):
        print("\n=== Главное меню ===")
        print("1. Создать новый счет")
        print("2. Пополнить счет")
        print("3. Снять средства")
        print("4. Перевести деньги")
        print("5. Проверить баланс")
        print("6. Информация о счете")
        print("7. История операций")
        print("8. Все счета")
        print("9. Выйти")
        print("Выберите действие (1-9): ", end='')

    def _handle_menu_choice(self, choice):
        if choice == 1:
            self._create_new_account()
        elif choice == 2:
            self._deposit_money()
        elif choice == 3:
            self._withdraw_money()
        elif choice == 4:
            self._transfer_money()
        elif choice == 5:
            self._check_balance()
        elif choice == 6:
            self._view_account_info()
        elif choice == 7:
            self._view_transaction_history()
        elif choice == 8:
            self._bank_system.display_all_accounts()
        else:
            print("Неверный выбор. Попробуйте еще раз.")

    def _create_new_account(self):
        owner_name = input("\nВведите имя владельца: ")
        try:
            initial_balance = float(input("Введите сумму первого депозита: $"))
            if initial_balance < 0:
                print("Ошибка: Сумма не может быть отрицательной")
                return
            self._bank_system.create_account(owner_name, initial_balance)
        except ValueError:
            print("Ошибка: Введите корректную сумму")

    def _deposit_money(self):
        acc = self._prompt_account("\nВведите номер счета: ")
        if acc:
            try:
                amount = float(input("Введите сумму пополнения: $"))
                acc.deposit(amount)
            except ValueError:
                print("Ошибка: Введите корректную сумму")

    def _withdraw_money(self):
        acc = self._prompt_account("\nВведите номер счета: ")
        if acc:
            try:
                amount = float(input("Введите сумму снятия: $"))
                acc.withdraw(amount)
            except ValueError:
                print("Ошибка: Введите корректную сумму")

    def _transfer_money(self):
        print("\n--- Перевод средств ---")
        sender = self._prompt_account("Введите номер счета отправителя: ")
        if not sender:
            return
        receiver = self._prompt_account("Введите номер счета получателя: ")
        if not receiver:
            return
        try:
            amount = float(input("Введите сумму перевода: $"))
            sender.transfer(receiver, amount)
        except ValueError:
            print("Ошибка: Введите корректную сумму")

    def _check_balance(self):
        acc = self._prompt_account("\nВведите номер счета: ")
        if acc:
            print(f"\nТекущий баланс: ${acc.get_balance():.2f}")

    def _view_account_info(self):
        acc = self._prompt_account("\nВведите номер счета: ")
        if acc:
            acc.display_account_info()

    def _view_transaction_history(self):
        acc = self._prompt_account("\nВведите номер счета: ")
        if acc:
            acc.display_transaction_history()

    def _prompt_account(self, prompt_text):
        acc_number = input(prompt_text)
        acc = self._bank_system.find_account(acc_number)
        if not acc:
            print("Ошибка: Счет не найден")
        return acc


def main():
    ui = BankUI()
    ui.run()


if __name__ == "__main__":
    main()