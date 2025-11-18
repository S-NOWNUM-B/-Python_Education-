"""
Класс банка с паттерном Singleton
"""

from datetime import date, datetime
from decimal import Decimal
from transaction import Transaction
from enums import TransactionType, TransactionStatus
from exceptions import (
    InvalidTransactionException,
    AccountNotFoundException,
    FraudDetectedException,
    InsufficientFundsException
)


class Bank:
    """Банк (Singleton)"""
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, bank_name="Центральный Банк"):
        # Инициализация только один раз
        if Bank._initialized:
            return

        self._bank_name = bank_name
        self._users = []
        self._all_transactions = []
        self._fraud_patterns = []
        self._daily_revenue = Decimal('0')
        self._foundation_date = date.today()

        Bank._initialized = True

    def get_bank_name(self):
        return self._bank_name

    # Управление пользователями
    def register_user(self, user):
        """Регистрация пользователя"""
        # Проверка уникальности username
        for existing_user in self._users:
            if existing_user.get_username() == user.get_username():
                raise InvalidTransactionException(
                    f"Пользователь {user.get_username()} уже зарегистрирован")

        self._users.append(user)
        print(f"\n✓ Пользователь {user.get_username()} зарегистрирован")
        return user

    def find_user(self, username):
        """Поиск пользователя"""
        for user in self._users:
            if user.get_username() == username:
                return user
        return None

    def find_account(self, account_number):
        """Поиск счета среди всех пользователей"""
        for user in self._users:
            account = user.find_account(account_number)
            if account:
                return account
        return None

    # Операции перевода
    def transfer(self, from_account_number, to_account_number, amount, description=""):
        """Перевод между счетами"""
        if amount <= 0:
            raise InvalidTransactionException("Сумма перевода должна быть положительной")

        # Поиск счетов
        from_account = self.find_account(from_account_number)
        to_account = self.find_account(to_account_number)

        if not from_account:
            raise AccountNotFoundException(f"Счет отправителя {from_account_number} не найден")

        if not to_account:
            raise AccountNotFoundException(f"Счет получателя {to_account_number} не найден")

        if from_account_number == to_account_number:
            raise InvalidTransactionException("Нельзя переводить на тот же счет")

        # Проверка на мошенничество
        if self._detect_fraud(from_account, amount):
            raise FraudDetectedException(
                "Обнаружена подозрительная активность. Транзакция заблокирована")

        # Выполнение перевода
        try:
            # Снятие со счета отправителя
            from_account.withdraw(amount, f"Перевод на {to_account_number}")

            # Зачисление на счет получателя
            to_account.deposit(amount, f"Перевод от {from_account_number}")

            # Создание транзакций для истории
            transfer_out = Transaction(TransactionType.TRANSFER_OUT, amount,
                                       f"Перевод на {to_account_number}: {description}")
            transfer_out.set_from_account(from_account_number)
            transfer_out.set_to_account(to_account_number)
            self._all_transactions.append(transfer_out)

            print(f"\n✓ Перевод выполнен успешно")
            print(f"От: {from_account_number}")
            print(f"На: {to_account_number}")
            print(f"Сумма: ${amount:.2f}")

            return transfer_out

        except InsufficientFundsException as e:
            print(f"\n✗ Ошибка перевода: {str(e)}")
            raise

    def _detect_fraud(self, account, amount):
        """Обнаружение мошенничества"""
        # Проверка 1: Слишком большая сумма за раз
        if amount > 50000:
            return True

        # Проверка 2: Много транзакций за короткий период
        recent_transactions = [t for t in account.get_transaction_history()
                               if (datetime.now() - t.get_timestamp()).seconds < 3600]

        if len(recent_transactions) > 10:
            return True

        # Проверка 3: Сумма транзакций за день превышает лимит
        today_transactions = [t for t in account.get_transaction_history()
                              if t.get_timestamp().date() == date.today()]

        total_today = sum(t.get_amount() for t in today_transactions)
        if total_today > 100000:
            return True

        return False

    def detect_fraud_for_user(self, username):
        """Проверка пользователя на подозрительную активность"""
        user = self.find_user(username)
        if not user:
            raise AccountNotFoundException(f"Пользователь {username} не найден")

        suspicious = []

        for account in user.get_accounts():
            # Анализ транзакций
            history = account.get_transaction_history()

            # Проверка крупных транзакций
            large_transactions = [t for t in history if t.get_amount() > 10000]
            if large_transactions:
                suspicious.append({
                    'account': account.get_account_number(),
                    'reason': 'Крупные транзакции',
                    'count': len(large_transactions)
                })

            # Проверка частых транзакций
            today_transactions = [t for t in history
                                  if t.get_timestamp().date() == date.today()]
            if len(today_transactions) > 20:
                suspicious.append({
                    'account': account.get_account_number(),
                    'reason': 'Частые транзакции',
                    'count': len(today_transactions)
                })

        if suspicious:
            print(f"\n⚠️  Обнаружена подозрительная активность для {username}:")
            for item in suspicious:
                print(f"  Счет {item['account']}: {item['reason']} ({item['count']})")
        else:
            print(f"\n✓ Подозрительная активность не обнаружена для {username}")

        return suspicious

    # Операции с процентами и комиссиями
    def apply_interest_to_all(self):
        """Начисление процентов на все счета"""
        print(f"\n=== Начисление процентов ({self._bank_name}) ===")
        total_interest = 0

        for user in self._users:
            for account in user.get_accounts():
                try:
                    interest = account.apply_interest()
                    total_interest += interest
                    if interest > 0:
                        print(f"Счет {account.get_account_number()}: +${interest:.2f}")
                except Exception as e:
                    print(f"Ошибка для счета {account.get_account_number()}: {str(e)}")

        print(f"\nВсего начислено процентов: ${total_interest:.2f}")
        return total_interest

    def charge_monthly_fees(self):
        """Списание месячных комиссий"""
        print(f"\n=== Списание месячных комиссий ({self._bank_name}) ===")
        total_fees = 0

        for user in self._users:
            for account in user.get_accounts():
                try:
                    fee = account.get_monthly_fee()
                    if fee > 0:
                        account.charge_fee(fee, "Месячная комиссия")
                        total_fees += fee
                        print(f"Счет {account.get_account_number()}: -${fee:.2f}")
                except Exception as e:
                    print(f"Ошибка для счета {account.get_account_number()}: {str(e)}")

        print(f"\nВсего списано комиссий: ${total_fees:.2f}")
        self._daily_revenue += Decimal(str(total_fees))
        return total_fees

    # Генерация выписки
    def generate_statement(self, account_number, start_date=None, end_date=None):
        """Генерация выписки по счету"""
        account = self.find_account(account_number)

        if not account:
            raise AccountNotFoundException(f"Счет {account_number} не найден")

        transactions = account.get_transaction_history()

        # Фильтрация по датам
        if start_date or end_date:
            filtered = []
            for t in transactions:
                t_date = t.get_timestamp().date()
                if start_date and t_date < start_date:
                    continue
                if end_date and t_date > end_date:
                    continue
                filtered.append(t)
            transactions = filtered

        # Формирование выписки
        print(f"\n{'=' * 70}")
        print(f"ВЫПИСКА ПО СЧЕТУ".center(70))
        print(f"{'=' * 70}")
        print(f"Банк: {self._bank_name}")
        print(f"Номер счета: {account_number}")
        print(f"Тип счета: {account.get_account_type().get_display_name()}")
        print(f"Текущий баланс: ${account.get_balance():.2f}")

        if start_date or end_date:
            period = f"{start_date or 'начало'} - {end_date or 'сегодня'}"
            print(f"Период: {period}")

        print(f"\n{'-' * 70}")
        print(f"{'Дата':20} {'Тип':20} {'Сумма':>15} {'Баланс':>15}")
        print(f"{'-' * 70}")

        for transaction in transactions:
            t_date = transaction.get_timestamp().strftime('%Y-%m-%d %H:%M')
            t_type = transaction.get_type().get_display_name()
            t_amount = transaction.get_amount()

            # Определение знака
            if transaction.get_type() in [TransactionType.DEPOSIT,
                                          TransactionType.TRANSFER_IN,
                                          TransactionType.INTEREST]:
                sign = "+"
            else:
                sign = "-"

            balance_after = transaction.get_balance_after()
            balance_str = f"${balance_after:.2f}" if balance_after else "-"

            print(f"{t_date:20} {t_type:20} {sign}${t_amount:>13.2f} {balance_str:>15}")

        print(f"{'-' * 70}")
        print(f"Всего транзакций: {len(transactions)}")
        print(f"{'=' * 70}\n")

        return transactions

    # Статистика
    def display_statistics(self):
        """Отображение статистики банка"""
        total_users = len(self._users)
        total_accounts = sum(len(u.get_accounts()) for u in self._users)
        total_balance = sum(u.get_total_balance() for u in self._users)
        total_transactions = len(self._all_transactions)

        print(f"\n=== Статистика {self._bank_name} ===")
        print(f"Дата основания: {self._foundation_date}")
        print(f"\nПользователи:")
        print(f"  Всего: {total_users}")
        print(f"  Активных: {sum(1 for u in self._users if not u.is_locked())}")
        print(f"\nСчета:")
        print(f"  Всего: {total_accounts}")
        print(f"  Общий баланс: ${total_balance:.2f}")
        print(f"\nТранзакции:")
        print(f"  Всего: {total_transactions}")
        print(f"\nВыручка:")
        print(f"  За сегодня: ${float(self._daily_revenue):.2f}")

    def display_all_users(self):
        """Отображение всех пользователей"""
        if not self._users:
            print("\nНет зарегистрированных пользователей")
            return

        print(f"\n=== Все пользователи {self._bank_name} ===")
        for user in self._users:
            status = "🔒" if user.is_locked() else "✓"
            print(f"{status} {user.get_username():20} | {user.get_full_name():30} | "
                  f"Счетов: {len(user.get_accounts()):>2} | Баланс: ${user.get_total_balance():>12.2f}")
        print(f"\nВсего пользователей: {len(self._users)}")
