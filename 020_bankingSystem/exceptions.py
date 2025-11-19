"""
Пользовательские исключения для банковской системы
"""

class BankingException(Exception):
    """Базовое исключение для банковских операций"""
    pass

class InsufficientFundsException(BankingException):
    """Исключение при недостатке средств"""
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Недостаточно средств: баланс ${balance:.2f}, требуется ${amount:.2f}")

class InvalidTransactionException(BankingException):
    """Исключение при некорректной транзакции"""
    pass

class AccountNotFoundException(BankingException):
    """Исключение когда счет не найден"""
    pass

class AuthenticationException(BankingException):
    """Исключение при ошибке аутентификации"""
    pass

class InvalidPasswordException(BankingException):
    """Исключение при некорректном пароле"""
    pass

class FraudDetectedException(BankingException):
    """Исключение при обнаружении мошенничества"""
    pass

class AccountLockedException(BankingException):
    """Исключение когда счет заблокирован"""
    pass
