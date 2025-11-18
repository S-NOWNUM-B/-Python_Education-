from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime, date
from decimal import Decimal


# Перечисление типов транзакций
class TransactionType(Enum):
    DEPOSIT = 1
    WITHDRAWAL = 2
    TRANSFER_IN = 3
    TRANSFER_OUT = 4
    INTEREST = 5
    FEE = 6


# Перечисление статусов транзакций
class TransactionStatus(Enum):
    PENDING = 1
    COMPLETED = 2
    FAILED = 3
    CANCELLED = 4


# Перечисление типов счетов
class AccountType(Enum):
    SAVINGS = "Savings Account"
    CHECKING = "Checking Account"
    BUSINESS = "Business Account"

    def __init__(self, display_name):
        self._display_name = display_name

    def get_display_name(self):
        return self._display_name


# Класс транзакции
class Transaction:
    _transaction_counter = 10000

    def __init__(self, transaction_type, amount, description=""):
        self._transaction_id = Transaction._transaction_counter
        Transaction._transaction_counter += 1
        self._type = transaction_type
        self._amount = Decimal(str(amount))
        self._date = datetime.now()
        self._description = description
        self._status = TransactionStatus.COMPLETED
        self._balance_after = None

    # Геттеры
    def get_transaction_id(self):
        return self._transaction_id

    def get_type(self):
        return self._type

    def get_amount(self):
        return self._amount

    def get_date(self):
        return self._date

    def get_description(self):
        return self._description

    def get_status(self):
        return self._status

    def get_balance_after(self):
        return self._balance_after

    # Сеттеры
    def set_status(self, status):
        self._status = status

    def set_balance_after(self, balance):
        self._balance_after = Decimal(str(balance))

    # Метод отображения транзакции
    def display(self):
        type_symbol = {
            TransactionType.DEPOSIT: "+",
            TransactionType.WITHDRAWAL: "-",
            TransactionType.TRANSFER_IN: "+",
            TransactionType.TRANSFER_OUT: "-",
            TransactionType.INTEREST: "+",
            TransactionType.FEE: "-"
        }

        symbol = type_symbol.get(self._type, " ")
        print(f"[{self._transaction_id}] {self._date.strftime('%Y-%m-%d %H:%M:%S')} | "
              f"{self._type.name:15} | {symbol}${self._amount:>10.2f} | "
              f"Balance: ${self._balance_after:>10.2f}" if self._balance_after else "")
        if self._description:
            print(f"     Description: {self._description}")


# Интерфейс для транзакционных операций
class Transactionable(ABC):
    @abstractmethod
    def deposit(self, amount, description=""):
        pass

    @abstractmethod
    def withdraw(self, amount, description=""):
        pass

    @abstractmethod
    def can_withdraw(self, amount):
        pass


# Абстрактный базовый класс счета
class Account(Transactionable, ABC):
    _account_counter = 1000

    def __init__(self, account_holder, initial_balance=0.0):
        self._account_number = f"ACC{Account._account_counter}"
        Account._account_counter += 1
        self._account_holder = account_holder
        self._balance = Decimal(str(initial_balance))
        self._transaction_history = []
        self._creation_date = date.today()
        self._is_active = True
        self._daily_transaction_count = 0
        self._last_transaction_date = None

        # Добавление начальной транзакции
        if initial_balance > 0:
            transaction = Transaction(TransactionType.DEPOSIT, initial_balance, "Initial deposit")
            transaction.set_balance_after(self._balance)
            self._transaction_history.append(transaction)

    # Геттеры
    def get_account_number(self):
        return self._account_number

    def get_account_holder(self):
        return self._account_holder

    def get_balance(self):
        return float(self._balance)

    def get_transaction_history(self):
        return self._transaction_history

    def get_creation_date(self):
        return self._creation_date

    def is_active(self):
        return self._is_active

    def get_daily_transaction_count(self):
        return self._daily_transaction_count

    # Абстрактные методы для конкретных типов счетов
    @abstractmethod
    def get_account_type(self):
        pass

    @abstractmethod
    def get_monthly_fee(self):
        pass

    @abstractmethod
    def get_interest_rate(self):
        pass

    # Метод сброса дневного счетчика транзакций
    def _reset_daily_counter_if_needed(self):
        today = date.today()
        if self._last_transaction_date != today:
            self._daily_transaction_count = 0
            self._last_transaction_date = today

    # Реализация метода deposit из интерфейса
    def deposit(self, amount, description=""):
        if amount <= 0:
            print("Error: Deposit amount must be positive")
            return False

        if not self._is_active:
            print("Error: Account is not active")
            return False

        self._reset_daily_counter_if_needed()

        self._balance += Decimal(str(amount))
        self._daily_transaction_count += 1

        transaction = Transaction(TransactionType.DEPOSIT, amount, description)
        transaction.set_balance_after(self._balance)
        self._transaction_history.append(transaction)

        print(f"\n✓ Deposit successful: ${amount:.2f}")
        print(f"New balance: ${self._balance:.2f}")
        return True

    # Реализация метода withdraw из интерфейса
    def withdraw(self, amount, description=""):
        if amount <= 0:
            print("Error: Withdrawal amount must be positive")
            return False

        if not self._is_active:
            print("Error: Account is not active")
            return False

        if not self.can_withdraw(amount):
            print("Error: Insufficient funds or withdrawal limit exceeded")
            return False

        self._reset_daily_counter_if_needed()

        self._balance -= Decimal(str(amount))
        self._daily_transaction_count += 1

        transaction = Transaction(TransactionType.WITHDRAWAL, amount, description)
        transaction.set_balance_after(self._balance)
        self._transaction_history.append(transaction)

        print(f"\n✓ Withdrawal successful: ${amount:.2f}")
        print(f"New balance: ${self._balance:.2f}")
        return True

    # Метод проверки возможности снятия (базовая реализация)
    def can_withdraw(self, amount):
        return self._balance >= Decimal(str(amount))

    # Метод перевода на другой счет
    def transfer(self, target_account, amount, description=""):
        if amount <= 0:
            print("Error: Transfer amount must be positive")
            return False

        if not self._is_active or not target_account.is_active():
            print("Error: One or both accounts are not active")
            return False

        if not self.can_withdraw(amount):
            print("Error: Insufficient funds for transfer")
            return False

        self._reset_daily_counter_if_needed()

        # Снятие со счета отправителя
        self._balance -= Decimal(str(amount))
        self._daily_transaction_count += 1

        transfer_out = Transaction(TransactionType.TRANSFER_OUT, amount,
                                   f"Transfer to {target_account.get_account_number()}: {description}")
        transfer_out.set_balance_after(self._balance)
        self._transaction_history.append(transfer_out)

        # Зачисление на счет получателя
        target_account._balance += Decimal(str(amount))
        transfer_in = Transaction(TransactionType.TRANSFER_IN, amount,
                                  f"Transfer from {self._account_number}: {description}")
        transfer_in.set_balance_after(target_account._balance)
        target_account._transaction_history.append(transfer_in)

        print(f"\n✓ Transfer successful: ${amount:.2f}")
        print(f"From: {self._account_number} (New balance: ${self._balance:.2f})")
        print(f"To: {target_account.get_account_number()} (New balance: ${target_account._balance:.2f})")
        return True

    # Метод начисления процентов (абстрактная реализация для переопределения)
    def apply_interest(self):
        interest_rate = self.get_interest_rate()
        if interest_rate <= 0:
            return 0

        interest = self._balance * Decimal(str(interest_rate))
        self._balance += interest

        transaction = Transaction(TransactionType.INTEREST, float(interest),
                                  f"Monthly interest at {interest_rate * 100:.2f}%")
        transaction.set_balance_after(self._balance)
        self._transaction_history.append(transaction)

        print(f"\n✓ Interest applied: ${interest:.2f}")
        print(f"New balance: ${self._balance:.2f}")
        return float(interest)

    # Метод списания комиссии
    def charge_fee(self, fee_amount, description="Monthly fee"):
        if fee_amount <= 0:
            return False

        self._balance -= Decimal(str(fee_amount))

        transaction = Transaction(TransactionType.FEE, fee_amount, description)
        transaction.set_balance_after(self._balance)
        self._transaction_history.append(transaction)

        print(f"\n✓ Fee charged: ${fee_amount:.2f}")
        print(f"New balance: ${self._balance:.2f}")
        return True

    # Метод получения транзакций за период
    def get_transactions_by_period(self, start_date, end_date):
        return [t for t in self._transaction_history
                if start_date <= t.get_date().date() <= end_date]

    # Метод получения транзакций по типу
    def get_transactions_by_type(self, transaction_type):
        return [t for t in self._transaction_history if t.get_type() == transaction_type]

    # Метод отображения информации о счете
    def display_info(self):
        print("\n=== Account Information ===")
        print(f"Account Number: {self._account_number}")
        print(f"Account Holder: {self._account_holder}")
        print(f"Account Type: {self.get_account_type().get_display_name()}")
        print(f"Balance: ${self._balance:.2f}")
        print(f"Status: {'Active' if self._is_active else 'Inactive'}")
        print(f"Creation Date: {self._creation_date}")
        print(f"Monthly Fee: ${self.get_monthly_fee():.2f}")
        print(f"Interest Rate: {self.get_interest_rate() * 100:.2f}%")
        print(f"Total Transactions: {len(self._transaction_history)}")
        print("---")

    # Метод краткого отображения счета
    def display_short(self):
        status = "✓" if self._is_active else "✗"
        print(f"[{status}] {self._account_number} | {self._account_holder:20} | "
              f"{self.get_account_type().name:10} | ${self._balance:>12.2f}")

    # Метод отображения истории транзакций
    def display_transaction_history(self, limit=None):
        if not self._transaction_history:
            print("\nNo transactions found")
            return

        print(f"\n=== Transaction History for {self._account_number} ===")
        transactions = self._transaction_history[-limit:] if limit else self._transaction_history

        for transaction in reversed(transactions):
            transaction.display()

        print(f"\nShowing {len(transactions)} of {len(self._transaction_history)} transactions")


# Класс сберегательного счета
class SavingsAccount(Account):
    INTEREST_RATE = 0.03  # 3% годовых
    MONTHLY_FEE = 2.00
    MINIMUM_BALANCE = 100.00
    WITHDRAWAL_LIMIT_PER_MONTH = 6

    def __init__(self, account_holder, initial_balance=0.0):
        super().__init__(account_holder, initial_balance)
        self._withdrawal_count_this_month = 0
        self._last_withdrawal_month = None

    def get_account_type(self):
        return AccountType.SAVINGS

    def get_monthly_fee(self):
        # Нет комиссии, если баланс выше минимального
        return 0.0 if self._balance >= Decimal(str(self.MINIMUM_BALANCE)) else self.MONTHLY_FEE

    def get_interest_rate(self):
        return self.INTEREST_RATE / 12  # Месячная ставка

    def _reset_withdrawal_counter_if_needed(self):
        current_month = (date.today().year, date.today().month)
        if self._last_withdrawal_month != current_month:
            self._withdrawal_count_this_month = 0
            self._last_withdrawal_month = current_month

    def can_withdraw(self, amount):
        self._reset_withdrawal_counter_if_needed()

        # Проверка лимита снятий
        if self._withdrawal_count_this_month >= self.WITHDRAWAL_LIMIT_PER_MONTH:
            print(f"Error: Monthly withdrawal limit ({self.WITHDRAWAL_LIMIT_PER_MONTH}) exceeded")
            return False

        # Проверка баланса
        return super().can_withdraw(amount)

    def withdraw(self, amount, description=""):
        self._reset_withdrawal_counter_if_needed()

        if super().withdraw(amount, description):
            self._withdrawal_count_this_month += 1
            remaining = self.WITHDRAWAL_LIMIT_PER_MONTH - self._withdrawal_count_this_month
            print(f"Remaining withdrawals this month: {remaining}")
            return True
        return False

    def display_info(self):
        super().display_info()
        self._reset_withdrawal_counter_if_needed()
        remaining = self.WITHDRAWAL_LIMIT_PER_MONTH - self._withdrawal_count_this_month
        print(f"Withdrawals this month: {self._withdrawal_count_this_month}/{self.WITHDRAWAL_LIMIT_PER_MONTH}")
        print(f"Minimum balance requirement: ${self.MINIMUM_BALANCE:.2f}")


# Класс текущего счета
class CheckingAccount(Account):
    INTEREST_RATE = 0.01  # 1% годовых
    MONTHLY_FEE = 5.00
    OVERDRAFT_LIMIT = 500.00
    OVERDRAFT_FEE = 35.00
    DAILY_TRANSACTION_LIMIT = 20

    def __init__(self, account_holder, initial_balance=0.0, overdraft_protection=False):
        super().__init__(account_holder, initial_balance)
        self._overdraft_protection = overdraft_protection

    def get_account_type(self):
        return AccountType.CHECKING

    def get_monthly_fee(self):
        return self.MONTHLY_FEE

    def get_interest_rate(self):
        return self.INTEREST_RATE / 12  # Месячная ставка

    def has_overdraft_protection(self):
        return self._overdraft_protection

    def set_overdraft_protection(self, enabled):
        self._overdraft_protection = enabled
        print(f"\n✓ Overdraft protection {'enabled' if enabled else 'disabled'}")

    def can_withdraw(self, amount):
        # Проверка дневного лимита транзакций
        if self._daily_transaction_count >= self.DAILY_TRANSACTION_LIMIT:
            print(f"Error: Daily transaction limit ({self.DAILY_TRANSACTION_LIMIT}) exceeded")
            return False

        # Обычная проверка баланса
        if self._balance >= Decimal(str(amount)):
            return True

        # Проверка овердрафта
        if self._overdraft_protection:
            deficit = Decimal(str(amount)) - self._balance
            if deficit <= Decimal(str(self.OVERDRAFT_LIMIT)):
                return True
            else:
                print(f"Error: Overdraft limit (${self.OVERDRAFT_LIMIT:.2f}) exceeded")
                return False

        return False

    def withdraw(self, amount, description=""):
        # Проверка на овердрафт
        will_overdraft = self._balance < Decimal(str(amount))

        if super().withdraw(amount, description):
            # Списание комиссии за овердрафт
            if will_overdraft and self._overdraft_protection:
                self.charge_fee(self.OVERDRAFT_FEE, "Overdraft fee")
            return True
        return False

    def display_info(self):
        super().display_info()
        print(f"Overdraft Protection: {'Yes' if self._overdraft_protection else 'No'}")
        if self._overdraft_protection:
            print(f"Overdraft Limit: ${self.OVERDRAFT_LIMIT:.2f}")
            print(f"Overdraft Fee: ${self.OVERDRAFT_FEE:.2f}")
        print(f"Daily transaction limit: {self.DAILY_TRANSACTION_LIMIT}")
        print(f"Today's transactions: {self._daily_transaction_count}/{self.DAILY_TRANSACTION_LIMIT}")


# Класс банка
class Bank:
    def __init__(self, bank_name):
        self._bank_name = bank_name
        self._accounts = []

    # Метод создания сберегательного счета
    def create_savings_account(self, account_holder, initial_balance=0.0):
        account = SavingsAccount(account_holder, initial_balance)
        self._accounts.append(account)
        print(f"\n✓ Savings account created successfully!")
        print(f"Account Number: {account.get_account_number()}")
        print(f"Account Holder: {account_holder}")
        print(f"Initial Balance: ${initial_balance:.2f}")
        return account

    # Метод создания текущего счета
    def create_checking_account(self, account_holder, initial_balance=0.0, overdraft_protection=False):
        account = CheckingAccount(account_holder, initial_balance, overdraft_protection)
        self._accounts.append(account)
        print(f"\n✓ Checking account created successfully!")
        print(f"Account Number: {account.get_account_number()}")
        print(f"Account Holder: {account_holder}")
        print(f"Initial Balance: ${initial_balance:.2f}")
        print(f"Overdraft Protection: {'Yes' if overdraft_protection else 'No'}")
        return account

    # Метод поиска счета по номеру
    def find_account(self, account_number):
        for account in self._accounts:
            if account.get_account_number() == account_number:
                return account
        return None

    # Метод поиска счетов по владельцу
    def find_accounts_by_holder(self, holder_name):
        term = holder_name.lower()
        return [acc for acc in self._accounts if term in acc.get_account_holder().lower()]

    # Метод отображения всех счетов
    def display_all_accounts(self):
        if not self._accounts:
            print("\nNo accounts in the bank")
            return

        print(f"\n=== {self._bank_name} - All Accounts ===")
        for account in self._accounts:
            account.display_short()
        print(f"\nTotal accounts: {len(self._accounts)}")

    # Метод применения месячных процентов ко всем счетам
    def apply_monthly_interest(self):
        print(f"\n=== Applying Monthly Interest ({self._bank_name}) ===")
        total_interest = 0

        for account in self._accounts:
            if account.is_active():
                interest = account.apply_interest()
                total_interest += interest

        print(f"\nTotal interest paid: ${total_interest:.2f}")
        return total_interest

    # Метод списания месячных комиссий
    def charge_monthly_fees(self):
        print(f"\n=== Charging Monthly Fees ({self._bank_name}) ===")
        total_fees = 0

        for account in self._accounts:
            if account.is_active():
                fee = account.get_monthly_fee()
                if fee > 0:
                    account.charge_fee(fee)
                    total_fees += fee

        print(f"\nTotal fees charged: ${total_fees:.2f}")
        return total_fees

    # Метод отображения статистики банка
    def display_statistics(self):
        total_accounts = len(self._accounts)
        active_accounts = sum(1 for acc in self._accounts if acc.is_active())
        savings_count = sum(1 for acc in self._accounts if isinstance(acc, SavingsAccount))
        checking_count = sum(1 for acc in self._accounts if isinstance(acc, CheckingAccount))
        total_balance = sum(acc.get_balance() for acc in self._accounts)
        total_transactions = sum(len(acc.get_transaction_history()) for acc in self._accounts)

        print(f"\n=== {self._bank_name} Statistics ===")
        print(f"Total Accounts: {total_accounts}")
        print(f"Active Accounts: {active_accounts}")
        print(f"\nAccount Types:")
        print(f"  Savings Accounts: {savings_count}")
        print(f"  Checking Accounts: {checking_count}")
        print(f"\nTotal Balance: ${total_balance:.2f}")
        print(f"Total Transactions: {total_transactions}")

        if total_accounts > 0:
            print(f"Average Balance per Account: ${total_balance / total_accounts:.2f}")


# Класс пользовательского интерфейса
class BankUI:
    def __init__(self, bank_name):
        self._bank = Bank(bank_name)
        self._initialize_sample_data()

    # Инициализация примерных данных
    def _initialize_sample_data(self):
        acc1 = self._bank.create_savings_account("John Doe", 5000.0)
        acc2 = self._bank.create_checking_account("Jane Smith", 2000.0, True)

    def run(self):
        print("╔════════════════════════════════════════╗")
        print("║  Banking System                        ║")
        print("╚════════════════════════════════════════╝\n")

        while True:
            try:
                self._display_main_menu()
                choice = int(input())

                if choice == 15:
                    print("\nThank you for banking with us!")
                    break

                self._handle_menu_choice(choice)

            except Exception as e:
                print(f"\nError: Invalid input. Please try again.")

    # Отображение главного меню
    def _display_main_menu(self):
        print("\n=== Main Menu ===")
        print("1. Create savings account")
        print("2. Create checking account")
        print("3. View account details")
        print("4. View all accounts")
        print("5. Deposit")
        print("6. Withdraw")
        print("7. Transfer")
        print("8. View transaction history")
        print("9. Apply interest to all accounts")
        print("10. Charge monthly fees")
        print("11. Search accounts by holder")
        print("12. View bank statistics")
        print("13. Toggle overdraft protection")
        print("14. View transactions by type")
        print("15. Exit")
        print("Enter choice (1-15): ", end='')

    # Обработка выбора меню
    def _handle_menu_choice(self, choice):
        actions = {
            1: self._create_savings_account,
            2: self._create_checking_account,
            3: self._view_account_details,
            4: self._bank.display_all_accounts,
            5: self._deposit,
            6: self._withdraw,
            7: self._transfer,
            8: self._view_transaction_history,
            9: self._bank.apply_monthly_interest,
            10: self._bank.charge_monthly_fees,
            11: self._search_accounts,
            12: self._bank.display_statistics,
            13: self._toggle_overdraft,
            14: self._view_transactions_by_type
        }
        if choice in actions:
            actions[choice]()
        else:
            print("Invalid choice. Please try again.")

    def _create_savings_account(self):
        holder = input("\nEnter account holder name: ")
        initial = float(input("Enter initial balance: $"))
        self._bank.create_savings_account(holder, initial)

    def _create_checking_account(self):
        holder = input("\nEnter account holder name: ")
        initial = float(input("Enter initial balance: $"))
        overdraft = input("Enable overdraft protection? (y/n): ").lower().startswith('y')
        self._bank.create_checking_account(holder, initial, overdraft)

    def _view_account_details(self):
        acc_number = input("\nEnter account number: ")
        account = self._bank.find_account(acc_number)
        if account:
            account.display_info()
        else:
            print("Error: Account not found")

    def _deposit(self):
        acc_number = input("\nEnter account number: ")
        account = self._bank.find_account(acc_number)
        if not account:
            print("Error: Account not found")
            return

        amount = float(input("Enter deposit amount: $"))
        description = input("Enter description (optional): ")
        account.deposit(amount, description)

    def _withdraw(self):
        acc_number = input("\nEnter account number: ")
        account = self._bank.find_account(acc_number)
        if not account:
            print("Error: Account not found")
            return

        amount = float(input("Enter withdrawal amount: $"))
        description = input("Enter description (optional): ")
        account.withdraw(amount, description)

    def _transfer(self):
        from_acc = input("\nEnter source account number: ")
        source = self._bank.find_account(from_acc)
        if not source:
            print("Error: Source account not found")
            return

        to_acc = input("Enter destination account number: ")
        destination = self._bank.find_account(to_acc)
        if not destination:
            print("Error: Destination account not found")
            return

        amount = float(input("Enter transfer amount: $"))
        description = input("Enter description (optional): ")
        source.transfer(destination, amount, description)

    def _view_transaction_history(self):
        acc_number = input("\nEnter account number: ")
        account = self._bank.find_account(acc_number)
        if not account:
            print("Error: Account not found")
            return

        limit_str = input("Enter number of recent transactions to show (or press Enter for all): ")
        limit = int(limit_str) if limit_str.strip() else None
        account.display_transaction_history(limit)

    def _search_accounts(self):
        holder = input("\nEnter account holder name: ")
        accounts = self._bank.find_accounts_by_holder(holder)
        if not accounts:
            print("\nNo accounts found")
            return

        print(f"\n=== Accounts for '{holder}' ===")
        for account in accounts:
            account.display_short()
        print(f"\nFound: {len(accounts)} account(s)")

    def _toggle_overdraft(self):
        acc_number = input("\nEnter account number: ")
        account = self._bank.find_account(acc_number)
        if not account:
            print("Error: Account not found")
            return

        if not isinstance(account, CheckingAccount):
            print("Error: Overdraft protection is only available for checking accounts")
            return

        enabled = input("Enable overdraft protection? (y/n): ").lower().startswith('y')
        account.set_overdraft_protection(enabled)

    def _view_transactions_by_type(self):
        acc_number = input("\nEnter account number: ")
        account = self._bank.find_account(acc_number)
        if not account:
            print("Error: Account not found")
            return

        print("\nSelect transaction type:")
        for i, t_type in enumerate(TransactionType, 1):
            print(f"{i}. {t_type.name}")
        choice = int(input("Enter choice: "))

        transaction_type = list(TransactionType)[choice - 1]
        transactions = account.get_transactions_by_type(transaction_type)

        if not transactions:
            print(f"\nNo {transaction_type.name} transactions found")
            return

        print(f"\n=== {transaction_type.name} Transactions ===")
        for transaction in reversed(transactions):
            transaction.display()
        print(f"\nTotal: {len(transactions)} transaction(s)")

def main():
    ui = BankUI("FirstBank International")
    ui.run()

if __name__ == "__main__":
    main()