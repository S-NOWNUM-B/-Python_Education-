"""
Утилиты для банковской системы
"""

import re
from datetime import date


def validate_email(email):
    """Проверка email"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


def validate_password_strength(password):
    """Проверка надежности пароля"""
    if len(password) < 8:
        return False, "Пароль должен содержать минимум 8 символов"

    if not any(c.isupper() for c in password):
        return False, "Пароль должен содержать хотя бы одну заглавную букву"

    if not any(c.islower() for c in password):
        return False, "Пароль должен содержать хотя бы одну строчную букву"

    if not any(c.isdigit() for c in password):
        return False, "Пароль должен содержать хотя бы одну цифру"

    return True, "Пароль надежный"


def parse_date(date_string):
    """Парсинг даты из строки"""
    try:
        return date.fromisoformat(date_string)
    except ValueError:
        return None


def format_currency(amount):
    """Форматирование суммы"""
    return f"${amount:,.2f}"


def generate_account_report(account):
    """Генерация отчета по счету"""
    report = {
        'account_number': account.get_account_number(),
        'account_type': account.get_account_type().get_display_name(),
        'balance': account.get_balance(),
        'transactions_count': len(account.get_transaction_history()),
        'creation_date': account.get_creation_date().isoformat(),
        'status': account.get_status().get_display_name()
    }
    return report
