"""
Класс транзакции
"""

from datetime import datetime
from decimal import Decimal
from enums import TransactionType, TransactionStatus


class Transaction:
    _transaction_counter = 10000

    def __init__(self, transaction_type, amount, description=""):
        self._transaction_id = f"TXN{Transaction._transaction_counter}"
        Transaction._transaction_counter += 1
        self._type = transaction_type
        self._amount = Decimal(str(amount))
        self._timestamp = datetime.now()
        self._description = description
        self._status = TransactionStatus.COMPLETED
        self._balance_after = None
        self._from_account = None
        self._to_account = None

    # Геттеры
    def get_transaction_id(self):
        return self._transaction_id

    def get_type(self):
        return self._type

    def get_amount(self):
        return float(self._amount)

    def get_timestamp(self):
        return self._timestamp

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

    def set_from_account(self, account_number):
        self._from_account = account_number

    def set_to_account(self, account_number):
        self._to_account = account_number

    def display(self):
        """Отображение транзакции"""
        type_symbol = {
            TransactionType.DEPOSIT: "+",
            TransactionType.WITHDRAWAL: "-",
            TransactionType.TRANSFER_IN: "+",
            TransactionType.TRANSFER_OUT: "-",
            TransactionType.INTEREST: "+",
            TransactionType.FEE: "-",
            TransactionType.LOAN_DISBURSEMENT: "+",
            TransactionType.LOAN_PAYMENT: "-"
        }

        symbol = type_symbol.get(self._type, " ")
        status_icon = "✓" if self._status == TransactionStatus.COMPLETED else "⚠"

        print(f"{status_icon} [{self._transaction_id}] {self._timestamp.strftime('%Y-%m-%d %H:%M')} | "
              f"{self._type.get_display_name():20} | {symbol}${self._amount:>10.2f}")

        if self._description:
            print(f"   Описание: {self._description}")

        if self._balance_after is not None:
            print(f"   Баланс после: ${self._balance_after:.2f}")

    def to_dict(self):
        """Преобразование в словарь для отчета"""
        return {
            'id': self._transaction_id,
            'type': self._type.get_display_name(),
            'amount': float(self._amount),
            'timestamp': self._timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'description': self._description,
            'status': self._status.get_display_name()
        }
