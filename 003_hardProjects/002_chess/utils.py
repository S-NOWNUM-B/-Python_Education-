"""
Утилиты для шахматной игры
"""


def position_to_notation(position):
    """Преобразовать позицию в шахматную нотацию"""
    row, col = position
    col_letter = chr(ord('a') + col)
    row_number = str(8 - row)
    return f"{col_letter}{row_number}"


def notation_to_position(notation):
    """Преобразовать нотацию в позицию"""
    if len(notation) != 2:
        return None

    col_letter = notation[0].lower()
    row_number = notation[1]

    if col_letter < 'a' or col_letter > 'h':
        return None
    if row_number < '1' or row_number > '8':
        return None

    col = ord(col_letter) - ord('a')
    row = 8 - int(row_number)

    return (row, col)


def parse_move_input(move_str):
    """Парсинг ввода хода"""
    move_str = move_str.strip().lower()

    # Формат: e2e4 или e2-e4
    if len(move_str) == 4:
        from_notation = move_str[:2]
        to_notation = move_str[2:]
    elif len(move_str) == 5 and move_str[2] in ['-', ' ']:
        from_notation = move_str[:2]
        to_notation = move_str[3:]
    else:
        return None, None

    from_pos = notation_to_position(from_notation)
    to_pos = notation_to_position(to_notation)

    return from_pos, to_pos