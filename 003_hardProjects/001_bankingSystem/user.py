"""
Класс пользователя банковской системы
"""

import hashlib
from datetime import datetime
from interfaces import Authenticable
from exceptions import (
    AuthenticationException,
    InvalidPasswordException,
    AccountNotFoundException
)


class User(Authenticable):
    """Пользователь банковской системы"""

    def __init__(self, username, password, full_name, email):
        self._username = username
        self._password_hash = self._hash_password(password)
        self._full_name = full_name
        self._email = email
        self._accounts = []
        self._is_authenticated = False
        self._registration_date = datetime.now()
        self._last_login = None
        self._failed_login_attempts = 0
        self._is_locked = False

    # Геттеры
    def get_username(self):
        return self._username

    def get_full_name(self):
        return self._full_name

    def get_email(self):
        return self._email

    def get_accounts(self):
        return self._accounts

    def is_locked(self):
        return self._is_locked

    @staticmethod
    def _hash_password(password):
        """Хеширование пароля"""
        return hashlib.sha256(password.encode()).hexdigest()

    def _verify_password(self, password):
        """Проверка пароля"""
        return self._password_hash == self._hash_password(password)

    # Реализация методов из интерфейса Authenticable
    def login(self, username, password):
        """Вход в систему"""
        if self._is_locked:
            raise AuthenticationException("Аккаунт заблокирован из-за множественных неудачных попыток входа")

        if username != self._username:
            raise AuthenticationException("Неверное имя пользователя")

        if not self._verify_password(password):
            self._failed_login_attempts += 1

            if self._failed_login_attempts >= 3:
                self._is_locked = True
                raise AuthenticationException("Аккаунт заблокирован после 3 неудачных попыток")

            raise AuthenticationException(
                f"Неверный пароль. Осталось попыток: {3 - self._failed_login_attempts}")

        self._is_authenticated = True
        self._last_login = datetime.now()
        self._failed_login_attempts = 0

        print(f"\n✓ Вход выполнен успешно")
        print(f"Добро пожаловать, {self._full_name}!")
        return True

    def logout(self):
        """Выход из системы"""
        if not self._is_authenticated:
            raise AuthenticationException("Пользователь не авторизован")

        self._is_authenticated = False
        print("\n✓ Выход выполнен успешно")
        return True

    def change_password(self, old_password, new_password):
        """Изменение пароля"""
        if not self._is_authenticated:
            raise AuthenticationException("Необходимо войти в систему")

        if not self._verify_password(old_password):
            raise InvalidPasswordException("Неверный текущий пароль")

        if len(new_password) < 8:
            raise InvalidPasswordException("Пароль должен содержать минимум 8 символов")

        self._password_hash = self._hash_password(new_password)
        print("\n✓ Пароль успешно изменен")
        return True

    def is_authenticated(self):
        """Проверка аутентификации"""
        return self._is_authenticated

    # Методы работы со счетами
    def add_account(self, account):
        """Добавление счета пользователю"""
        self._accounts.append(account)
        print(f"\n✓ Счет {account.get_account_number()} добавлен")

    def remove_account(self, account_number):
        """Удаление счета"""
        for i, account in enumerate(self._accounts):
            if account.get_account_number() == account_number:
                removed = self._accounts.pop(i)
                print(f"\n✓ Счет {account_number} удален")
                return removed

        raise AccountNotFoundException(f"Счет {account_number} не найден")

    def find_account(self, account_number):
        """Поиск счета по номеру"""
        for account in self._accounts:
            if account.get_account_number() == account_number:
                return account
        return None

    def get_total_balance(self):
        """Общий баланс по всем счетам"""
        return sum(acc.get_balance() for acc in self._accounts)

    def display_info(self):
        """Отображение информации о пользователе"""
        print(f"\n=== Информация о пользователе ===")
        print(f"Имя пользователя: {self._username}")
        print(f"Полное имя: {self._full_name}")
        print(f"Email: {self._email}")
        print(f"Дата регистрации: {self._registration_date.strftime('%Y-%m-%d')}")

        if self._last_login:
            print(f"Последний вход: {self._last_login.strftime('%Y-%m-%d %H:%M')}")

        print(f"Количество счетов: {len(self._accounts)}")
        print(f"Общий баланс: ${self.get_total_balance():.2f}")
        print(f"Статус: {'🔒 Заблокирован' if self._is_locked else '✓ Активен'}")
        print("---")

    def display_accounts(self):
        """Отображение всех счетов"""
        if not self._accounts:
            print("\nУ вас нет счетов")
            return

        print(f"\n=== Счета пользователя {self._username} ===")
        for account in self._accounts:
            print(f"  {account.get_account_number()} | {account.get_account_type().get_display_name():15} | "
                  f"${account.get_balance():>12.2f}")
        print(f"\nОбщий баланс: ${self.get_total_balance():.2f}")
