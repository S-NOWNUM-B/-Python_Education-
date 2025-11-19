"""
Интерфейсы для банковской системы
"""

from abc import ABC, abstractmethod


class Authenticable(ABC):
    """Интерфейс для аутентификации пользователей"""

    @abstractmethod
    def login(self, username, password):
        """Вход в систему"""
        pass

    @abstractmethod
    def logout(self):
        """Выход из системы"""
        pass

    @abstractmethod
    def change_password(self, old_password, new_password):
        """Изменение пароля"""
        pass

    @abstractmethod
    def is_authenticated(self):
        """Проверка аутентификации"""
        pass


class Transactionable(ABC):
    """Интерфейс для транзакционных операций"""

    @abstractmethod
    def deposit(self, amount, description=""):
        """Внести средства"""
        pass

    @abstractmethod
    def withdraw(self, amount, description=""):
        """Снять средства"""
        pass

    @abstractmethod
    def get_balance(self):
        """Получить баланс"""
        pass
