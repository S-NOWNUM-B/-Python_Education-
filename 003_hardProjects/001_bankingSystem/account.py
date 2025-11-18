"""
Классы банковских счетов
"""

from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal
from interfaces import Transactionable
from transaction import Transaction
from enums import TransactionType, AccountType, AccountStatus
from exceptions import (
    InsufficientFundsException,
    InvalidTransactionException,
    AccountLockedException
)


class Account(Transactionable, ABC):
    """Абстрактный базовый класс счета"""
    _account_counter = 1000

    def __init__(self, initial_balance=0.0):
        self._account_number = f"ACC{Account._account_counter:08d}"
        Account._account_counter += 1
        self._balance = Decimal(str(initial_balance))
        self._transaction_history = []
        self._creation_date = date.today()
        self._status = AccountStatus.ACTIVE
        self._daily_transaction_count = 0
        self._last_transaction_date = None

        if initial_balance > 0:
            transaction = Transaction(TransactionType.DEPOSIT, initial_balance, "Начальный баланс")
            transaction.set_balance_after(self._balance)
            self._transaction_history.append(transaction)

    # Геттеры
    def get_account_number(self):
        return self._account_number

    def get_balance(self):
        return float(self._balance)

    def get_transaction_history(self):
        return self._transaction_history

    def get_creation_date(self):
        return self._creation_date

    def get_status(self):
        return self._status

    # Абстрактные методы
    @abstractmethod
    def get_account_type(self):
        pass

    @abstractmethod
    def get_interest_rate(self):
        pass

    @abstractmethod
    def get_monthly_fee(self):
        pass

    @abstractmethod
    def get_withdrawal_limit(self):
        pass

    # Проверка статуса счета
    def _check_account_status(self):
        if self._status == AccountStatus.CLOSED:
            raise AccountLockedException("Счет закрыт")
        if self._status == AccountStatus.FROZEN:
            raise AccountLockedException("Счет заморожен")
        if self._status == AccountStatus.SUSPENDED:
            raise AccountLockedException("Счет приостановлен")

    # Сброс дневного счетчика
    def _reset_daily_counter_if_needed(self):
        today = date.today()
        if self._last_transaction_date != today:
            self._daily_transaction_count = 0
            self._last_transaction_date = today

    # Реализация deposit из интерфейса
    def deposit(self, amount, description=""):
        if amount <= 0:
            raise InvalidTransactionException("Сумма пополнения должна быть положительной")

        self._check_account_status()
        self._reset_daily_counter_if_needed()

        self._balance += Decimal(str(amount))
        self._daily_transaction_count += 1

        transaction = Transaction(TransactionType.DEPOSIT, amount, description)
        transaction.set_balance_after(self._balance)
        self._transaction_history.append(transaction)

        return transaction

    # Реализация withdraw из интерфейса
    def withdraw(self, amount, description=""):
        if amount <= 0:
            raise InvalidTransactionException("Сумма снятия должна быть положительной")

        self._check_account_status()
        self._reset_daily_counter_if_needed()

        if not self._can_withdraw(amount):
            raise InsufficientFundsException(float(self._balance), amount)

        self._balance -= Decimal(str(amount))
        self._daily_transaction_count += 1

        transaction = Transaction(TransactionType.WITHDRAWAL, amount, description)
        transaction.set_balance_after(self._balance)
        self._transaction_history.append(transaction)

        return transaction

    def _can_withdraw(self, amount):
        """Базовая проверка возможности снятия"""
        return self._balance >= Decimal(str(amount))

    def apply_interest(self):
        """Начисление процентов"""
        interest_rate = self.get_interest_rate()
        if interest_rate <= 0:
            return 0

        interest = self._balance * Decimal(str(interest_rate))
        self._balance += interest

        transaction = Transaction(TransactionType.INTEREST, float(interest),
                                  f"Начисление процентов {interest_rate * 100:.2f}%")
        transaction.set_balance_after(self._balance)
        self._transaction_history.append(transaction)

        return float(interest)

    def charge_fee(self, fee_amount, description="Комиссия"):
        """Списание комиссии"""
        if fee_amount <= 0:
            return False

        self._balance -= Decimal(str(fee_amount))

        transaction = Transaction(TransactionType.FEE, fee_amount, description)
        transaction.set_balance_after(self._balance)
        self._transaction_history.append(transaction)

        return True

    def display_info(self):
        """Отображение информации о счете"""
        print(f"\n=== Информация о счете ===")
        print(f"Номер счета: {self._account_number}")
        print(f"Тип: {self.get_account_type().get_display_name()}")
        print(f"Баланс: ${self._balance:.2f}")
        print(f"Статус: {self._status.get_display_name()}")
        print(f"Дата открытия: {self._creation_date}")
        print(f"Процентная ставка: {self.get_interest_rate() * 100:.2f}%")
        print(f"Всего транзакций: {len(self._transaction_history)}")
        print("---")


class SavingsAccount(Account):
    """Сберегательный счет"""
    INTEREST_RATE = 0.04  # 4% годовых
    MONTHLY_FEE = 0.0
    MINIMUM_BALANCE = 100.0
    WITHDRAWAL_LIMIT = 50000.0
    MONTHLY_WITHDRAWAL_LIMIT = 6

    def __init__(self, initial_balance=0.0):
        super().__init__(initial_balance)
        self._withdrawal_count_this_month = 0
        self._last_withdrawal_month = None

    def get_account_type(self):
        return AccountType.SAVINGS

    def get_interest_rate(self):
        return self.INTEREST_RATE / 12  # Месячная ставка

    def get_monthly_fee(self):
        return 0.0 if self._balance >= Decimal(str(self.MINIMUM_BALANCE)) else 5.0

    def get_withdrawal_limit(self):
        return self.WITHDRAWAL_LIMIT

    def _reset_withdrawal_counter_if_needed(self):
        current_month = (date.today().year, date.today().month)
        if self._last_withdrawal_month != current_month:
            self._withdrawal_count_this_month = 0
            self._last_withdrawal_month = current_month

    def _can_withdraw(self, amount):
        self._reset_withdrawal_counter_if_needed()

        if self._withdrawal_count_this_month >= self.MONTHLY_WITHDRAWAL_LIMIT:
            raise InvalidTransactionException(
                f"Превышен лимит снятий в месяц ({self.MONTHLY_WITHDRAWAL_LIMIT})")

        if amount > self.WITHDRAWAL_LIMIT:
            raise InvalidTransactionException(
                f"Сумма превышает разовый лимит (${self.WITHDRAWAL_LIMIT:.2f})")

        return super()._can_withdraw(amount)

    def withdraw(self, amount, description=""):
        self._reset_withdrawal_counter_if_needed()
        transaction = super().withdraw(amount, description)
        self._withdrawal_count_this_month += 1
        return transaction


class CheckingAccount(Account):
    """Текущий счет"""
    INTEREST_RATE = 0.01  # 1% годовых
    MONTHLY_FEE = 10.0
    OVERDRAFT_LIMIT = 1000.0
    OVERDRAFT_FEE = 35.0
    WITHDRAWAL_LIMIT = 100000.0

    def __init__(self, initial_balance=0.0, overdraft_protection=False):
        super().__init__(initial_balance)
        self._overdraft_protection = overdraft_protection

    def get_account_type(self):
        return AccountType.CHECKING

    def get_interest_rate(self):
        return self.INTEREST_RATE / 12

    def get_monthly_fee(self):
        return self.MONTHLY_FEE

    def get_withdrawal_limit(self):
        return self.WITHDRAWAL_LIMIT

    def has_overdraft_protection(self):
        return self._overdraft_protection

    def set_overdraft_protection(self, enabled):
        self._overdraft_protection = enabled

    def _can_withdraw(self, amount):
        amount_decimal = Decimal(str(amount))

        if self._balance >= amount_decimal:
            return True

        if self._overdraft_protection:
            deficit = amount_decimal - self._balance
            if deficit <= Decimal(str(self.OVERDRAFT_LIMIT)):
                return True
            else:
                raise InvalidTransactionException(
                    f"Превышен лимит овердрафта (${self.OVERDRAFT_LIMIT:.2f})")

        return False

    def withdraw(self, amount, description=""):
        will_overdraft = self._balance < Decimal(str(amount))

        transaction = super().withdraw(amount, description)

        if will_overdraft and self._overdraft_protection:
            self.charge_fee(self.OVERDRAFT_FEE, "Комиссия за овердрафт")

        return transaction


class CreditAccount(Account):
    """Кредитный счет"""
    INTEREST_RATE = 0.18  # 18% годовых
    MONTHLY_FEE = 0.0
    MINIMUM_PAYMENT_PERCENT = 0.05  # 5% от задолженности

    def __init__(self, credit_limit):
        super().__init__(0.0)
        self._credit_limit = Decimal(str(credit_limit))
        self._debt = Decimal('0')
        self._available_credit = self._credit_limit

    def get_account_type(self):
        return AccountType.CREDIT

    def get_interest_rate(self):
        return self.INTEREST_RATE / 12

    def get_monthly_fee(self):
        return self.MONTHLY_FEE

    def get_withdrawal_limit(self):
        return float(self._available_credit)

    def get_debt(self):
        return float(self._debt)

    def get_credit_limit(self):
        return float(self._credit_limit)

    def get_available_credit(self):
        return float(self._available_credit)

    def _can_withdraw(self, amount):
        return Decimal(str(amount)) <= self._available_credit

    def withdraw(self, amount, description=""):
        """Снятие средств по кредиту"""
        if amount <= 0:
            raise InvalidTransactionException("Сумма должна быть положительной")

        self._check_account_status()

        amount_decimal = Decimal(str(amount))

        if amount_decimal > self._available_credit:
            raise InvalidTransactionException(
                f"Недостаточно кредитного лимита (Доступно: ${self._available_credit:.2f})")

        self._debt += amount_decimal
        self._available_credit -= amount_decimal
        self._balance -= amount_decimal

        transaction = Transaction(TransactionType.LOAN_DISBURSEMENT, amount, description)
        transaction.set_balance_after(self._balance)
        self._transaction_history.append(transaction)

        return transaction

    def deposit(self, amount, description=""):
        """Погашение кредита"""
        if amount <= 0:
            raise InvalidTransactionException("Сумма должна быть положительной")

        self._check_account_status()

        amount_decimal = Decimal(str(amount))
        payment = min(amount_decimal, self._debt)

        self._debt -= payment
        self._available_credit += payment
        self._balance += payment

        transaction = Transaction(TransactionType.LOAN_PAYMENT, float(payment), description)
        transaction.set_balance_after(self._balance)
        self._transaction_history.append(transaction)

        return transaction

    def calculate_minimum_payment(self):
        """Расчет минимального платежа"""
        minimum = self._debt * Decimal(str(self.MINIMUM_PAYMENT_PERCENT))
        return float(max(minimum, Decimal('25')))  # Минимум $25

    def apply_interest(self):
        """Начисление процентов на задолженность"""
        if self._debt <= 0:
            return 0

        interest_rate = self.get_interest_rate()
        interest = self._debt * Decimal(str(interest_rate))
        self._debt += interest
        self._balance -= interest

        transaction = Transaction(TransactionType.INTEREST, float(interest),
                                  f"Проценты на задолженность {interest_rate * 100:.2f}%")
        transaction.set_balance_after(self._balance)
        self._transaction_history.append(transaction)

        return float(interest)

    def display_info(self):
        """Отображение информации о кредитном счете"""
        super().display_info()
        print(f"Кредитный лимит: ${self._credit_limit:.2f}")
        print(f"Задолженность: ${self._debt:.2f}")
        print(f"Доступный кредит: ${self._available_credit:.2f}")
        print(f"Минимальный платеж: ${self.calculate_minimum_payment():.2f}")
