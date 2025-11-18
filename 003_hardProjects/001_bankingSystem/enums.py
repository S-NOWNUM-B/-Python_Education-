"""
Перечисления для банковской системы
"""

from enum import Enum

class TransactionType(Enum):
    DEPOSIT = "Пополнение"
    WITHDRAWAL = "Снятие"
    TRANSFER_IN = "Входящий перевод"
    TRANSFER_OUT = "Исходящий перевод"
    INTEREST = "Начисление процентов"
    FEE = "Комиссия"
    LOAN_DISBURSEMENT = "Выдача кредита"
    LOAN_PAYMENT = "Платеж по кредиту"

    def __init__(self, display_name):
        self._display_name = display_name

    def get_display_name(self):
        return self._display_name

class TransactionStatus(Enum):
    PENDING = "Ожидает"
    COMPLETED = "Завершена"
    FAILED = "Не удалась"
    CANCELLED = "Отменена"
    FRAUD_DETECTED = "Обнаружено мошенничество"

    def __init__(self, display_name):
        self._display_name = display_name

    def get_display_name(self):
        return self._display_name

class AccountType(Enum):
    SAVINGS = "Сберегательный"
    CHECKING = "Текущий"
    CREDIT = "Кредитный"

    def __init__(self, display_name):
        self._display_name = display_name

    def get_display_name(self):
        return self._display_name

class AccountStatus(Enum):
    ACTIVE = "Активный"
    FROZEN = "Заморожен"
    CLOSED = "Закрыт"
    SUSPENDED = "Приостановлен"

    def __init__(self, display_name):
        self._display_name = display_name

    def get_display_name(self):
        return self._display_name
