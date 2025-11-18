"""
Класс шахматной игры
"""

from board import Board
from move import Move
from enums import GameStatus, PieceColor, MoveType, PieceType
from exceptions import InvalidMoveException, GameOverException, KingInCheckException
from piece import Queen, Rook, Bishop, Knight


class ChessGame:
    """Шахматная партия"""

    def __init__(self, white_player, black_player):
        self._board = Board()
        self._white_player = white_player
        self._black_player = black_player
        self._current_turn = PieceColor.WHITE
        self._move_history = []
        self._status = GameStatus.IN_PROGRESS
        self._move_count = 0
        self._fifty_move_counter = 0
        self._position_history = []

    def get_board(self):
        return self._board

    def get_current_turn(self):
        return self._current_turn

    def get_status(self):
        return self._status

    def get_move_history(self):
        return self._move_history

    def get_current_player(self):
        return self._white_player if self._current_turn == PieceColor.WHITE else self._black_player

    def make_move(self, from_pos, to_pos, promotion_piece=None):
        """Сделать ход"""
        if self._status not in [GameStatus.IN_PROGRESS, GameStatus.CHECK]:
            raise GameOverException("Игра завершена")

        from_row, from_col = from_pos
        to_row, to_col = to_pos

        piece = self._board.get_piece(from_row, from_col)

        if not piece:
            raise InvalidMoveException("Нет фигуры на начальной позиции")

        if piece.get_color() != self._current_turn:
            raise InvalidMoveException("Сейчас ход другого игрока")

        # Проверка корректности хода
        if not piece.is_valid_move(self._board, from_pos, to_pos):
            raise InvalidMoveException("Некорректный ход для этой фигуры")

        # Проверка, не откроет ли ход короля под шах
        if self._would_be_in_check_after_move(from_pos, to_pos):
            raise KingInCheckException("Этот ход подставляет короля под шах")

        # Определение типа хода
        captured_piece = self._board.get_piece(to_row, to_col)
        move_type = MoveType.CAPTURE if captured_piece else MoveType.NORMAL

        # Специальные ходы
        if piece.get_type() == PieceType.KING:
            if abs(to_col - from_col) == 2:
                move_type = MoveType.CASTLING_KINGSIDE if to_col > from_col else MoveType.CASTLING_QUEENSIDE

        if piece.get_type() == PieceType.PAWN:
            if self._board.en_passant_target == to_pos:
                move_type = MoveType.EN_PASSANT
            if to_row == 0 or to_row == 7:
                move_type = MoveType.PROMOTION

        # Создание хода
        move = Move(from_pos, to_pos, piece, captured_piece, move_type)

        # Выполнение хода
        self._execute_move(move, promotion_piece)

        # Обновление состояния игры
        self._move_history.append(move)
        self._move_count += 1

        # Проверка на шах/мат
        opponent_color = self._current_turn.opposite()
        if self._board.is_in_check(opponent_color):
            move.set_check(True)
            if self._is_checkmate(opponent_color):
                move.set_checkmate(True)
                self._status = GameStatus.CHECKMATE_WHITE if self._current_turn == PieceColor.WHITE else GameStatus.CHECKMATE_BLACK
            else:
                self._status = GameStatus.CHECK
        else:
            if self._is_stalemate(opponent_color):
                self._status = GameStatus.STALEMATE
            else:
                self._status = GameStatus.IN_PROGRESS

        # Проверка на ничью
        self._check_draw_conditions()

        # Смена хода
        self._current_turn = opponent_color

        return move

    def _execute_move(self, move, promotion_piece=None):
        """Выполнить ход на доске"""
        from_pos = move.get_from_pos()
        to_pos = move.get_to_pos()
        piece = move.get_piece()
        move_type = move.get_move_type()

        # Обычный ход или взятие
        if move_type in [MoveType.NORMAL, MoveType.CAPTURE]:
            self._board.remove_piece(*from_pos)

            if move.get_captured_piece():
                self._board.capture_piece(move.get_captured_piece())
                self._fifty_move_counter = 0

            self._board.set_piece(*to_pos, piece)
            piece.set_moved()

        # Рокировка
        elif move_type == MoveType.CASTLING_KINGSIDE:
            row = from_pos[0]
            self._board.remove_piece(row, 4)  # Король
            self._board.remove_piece(row, 7)  # Ладья
            self._board.set_piece(row, 6, piece)  # Король на новое место
            rook = self._board.get_piece(row, 7) if self._board.get_piece(row, 7) else piece  # Временно
            self._board.set_piece(row, 5, rook)  # Ладья на новое место
            piece.set_moved()

        elif move_type == MoveType.CASTLING_QUEENSIDE:
            row = from_pos[0]
            self._board.remove_piece(row, 4)
            self._board.remove_piece(row, 0)
            self._board.set_piece(row, 2, piece)
            rook = self._board.get_piece(row, 0) if self._board.get_piece(row, 0) else piece
            self._board.set_piece(row, 3, rook)
            piece.set_moved()

        # Взятие на проходе
        elif move_type == MoveType.EN_PASSANT:
            self._board.remove_piece(*from_pos)
            self._board.set_piece(*to_pos, piece)
            # Убираем взятую пешку
            captured_row = from_pos[0]
            captured_col = to_pos[1]
            captured = self._board.remove_piece(captured_row, captured_col)
            self._board.capture_piece(captured)
            piece.set_moved()
            self._fifty_move_counter = 0

        # Превращение пешки
        elif move_type == MoveType.PROMOTION:
            self._board.remove_piece(*from_pos)

            if move.get_captured_piece():
                self._board.capture_piece(move.get_captured_piece())

            # Создаем новую фигуру
            promotion_type = promotion_piece or PieceType.QUEEN
            piece_classes = {
                PieceType.QUEEN: Queen,
                PieceType.ROOK: Rook,
                PieceType.BISHOP: Bishop,
                PieceType.KNIGHT: Knight
            }

            new_piece = piece_classes[promotion_type](piece.get_color())
            self._board.set_piece(*to_pos, new_piece)
            move.set_promotion_piece(promotion_type)
            self._fifty_move_counter = 0

        # Обновление en passant
        self._board.en_passant_target = None
        if piece.get_type() == PieceType.PAWN:
            if abs(to_pos[0] - from_pos[0]) == 2:
                en_passant_row = (from_pos[0] + to_pos[0]) // 2
                self._board.en_passant_target = (en_passant_row, from_pos[1])
            self._fifty_move_counter = 0

        # Правило 50 ходов
        if piece.get_type() != PieceType.PAWN and not move.get_captured_piece():
            self._fifty_move_counter += 1

    def _would_be_in_check_after_move(self, from_pos, to_pos):
        """Проверка, будет ли король под шахом после хода"""
        # Создаем копию доски
        temp_board = self._board.clone()

        # Делаем ход на копии
        piece = temp_board.get_piece(*from_pos)
        temp_board.remove_piece(*from_pos)
        temp_board.set_piece(*to_pos, piece)

        # Проверяем шах
        return temp_board.is_in_check(self._current_turn)

    def _is_checkmate(self, color):
        """Проверка на мат"""
        if not self._board.is_in_check(color):
            return False

        # Проверяем, есть ли хоть один легальный ход
        return len(self._get_legal_moves(color)) == 0

    def _is_stalemate(self, color):
        """Проверка на пат"""
        if self._board.is_in_check(color):
            return False

        # Нет легальных ходов, но король не под шахом
        return len(self._get_legal_moves(color)) == 0

    def _get_legal_moves(self, color):
        """Получить все легальные ходы"""
        legal_moves = []
        all_moves = self._board.get_all_possible_moves(color)

        for from_pos, to_pos in all_moves:
            if not self._would_be_in_check_after_move(from_pos, to_pos):
                legal_moves.append((from_pos, to_pos))

        return legal_moves

    def _check_draw_conditions(self):
        """Проверка условий ничьей"""
        # Правило 50 ходов
        if self._fifty_move_counter >= 50:
            self._status = GameStatus.DRAW_BY_50_MOVES

        # Троекратное повторение позиции
        # (упрощенная реализация)

    def offer_draw(self):
        """Предложение ничьей"""
        self._status = GameStatus.DRAW_BY_AGREEMENT

    def resign(self, color):
        """Сдаться"""
        if color == PieceColor.WHITE:
            self._status = GameStatus.CHECKMATE_BLACK
            self._black_player.add_win()
            self._white_player.add_loss()
        else:
            self._status = GameStatus.CHECKMATE_WHITE
            self._white_player.add_win()
            self._black_player.add_loss()

    def display_status(self):
        """Отобразить статус игры"""
        print(f"\n=== Статус игры ===")
        print(f"Ход: {self._move_count}")
        print(f"Текущий игрок: {self.get_current_player().get_name()} ({self._current_turn.get_display_name()})")
        print(f"Статус: {self._status.get_display_name()}")

        if self._move_history:
            last_move = self._move_history[-1]
            print(f"Последний ход: {last_move.to_algebraic()}")

        print("---\n")
