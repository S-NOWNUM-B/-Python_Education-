from enum import Enum
from datetime import date, timedelta

# Перечисление типов номеров
class RoomType(Enum):
    SINGLE = ("Single Room", 1, 100.0)
    DOUBLE = ("Double Room", 2, 150.0)
    SUITE = ("Suite", 4, 300.0)
    DELUXE = ("Deluxe Suite", 6, 500.0)

    def __init__(self, display_name, capacity, base_price):
        self._display_name = display_name
        self._capacity = capacity
        self._base_price = base_price

    def get_display_name(self):
        return self._display_name

    def get_capacity(self):
        return self._capacity

    def get_base_price(self):
        return self._base_price

# Перечисление статусов бронирования
class BookingStatus(Enum):
    CONFIRMED = 1
    CHECKED_IN = 2
    CHECKED_OUT = 3
    CANCELLED = 4

# Класс гостя
class Guest:
    _guest_counter = 1

    def __init__(self, name, email, phone_number, id_document):
        self._guest_id = Guest._guest_counter
        Guest._guest_counter += 1
        self._name = name
        self._email = email
        self._phone_number = phone_number
        self._id_document = id_document

    # Геттеры
    def get_guest_id(self):
        return self._guest_id
    def get_name(self):
        return self._name
    def get_email(self):
        return self._email
    def get_phone_number(self):
        return self._phone_number
    def get_id_document(self):
        return self._id_document

    # Отображение информации о госте
    def display_info(self):
        print("\n=== Guest Information ===")
        print(f"Guest ID: {self._guest_id}")
        print(f"Name: {self._name}")
        print(f"Email: {self._email}")
        print(f"Phone: {self._phone_number}")
        print(f"ID Document: {self._id_document}")
        print("---")

# Класс номера
class Room:
    def __init__(self, room_number, room_type, floor, has_balcony, has_sea_view):
        self._room_number = room_number
        self._type = room_type
        self._price_per_night = room_type.get_base_price()
        self._is_available = True
        self._floor = floor
        self._has_balcony = has_balcony
        self._has_sea_view = has_sea_view

        # Надбавка за балкон
        if has_balcony:
            self._price_per_night += 20.0

        # Надбавка за вид на море
        if has_sea_view:
            self._price_per_night += 50.0

    # Геттеры
    def get_room_number(self):
        return self._room_number
    def get_type(self):
        return self._type
    def get_price_per_night(self):
        return self._price_per_night
    def is_available(self):
        return self._is_available
    def get_floor(self):
        return self._floor
    def has_balcony(self):
        return self._has_balcony
    def has_sea_view(self):
        return self._has_sea_view

    # Сеттеры
    def set_available(self, available):
        self._is_available = available

    # Отображение информации о номере
    def display_info(self):
        print("\n=== Room Information ===")
        print(f"Room Number: {self._room_number}")
        print(f"Type: {self._type.get_display_name()}")
        print(f"Capacity: {self._type.get_capacity()} guests")
        print(f"Price per night: ${self._price_per_night:.2f}")
        print(f"Floor: {self._floor}")
        print(f"Balcony: {'Yes' if self._has_balcony else 'No'}")
        print(f"Sea View: {'Yes' if self._has_sea_view else 'No'}")
        print(f"Status: {'Available' if self._is_available else 'Occupied'}")
        print("---")

    # Краткое отображение номера
    def display_short(self):
        status = "[✓]" if self._is_available else "[✗]"
        features = ""
        if self._has_balcony:
            features += "🏖️ "
        if self._has_sea_view:
            features += "🌊 "

        print(f"{status} Room {self._room_number} | {self._type.get_display_name()} | Floor {self._floor} | ${self._price_per_night:.2f}/night {features}")

# Класс бронирования
class Booking:
    _booking_counter = 1000

    def __init__(self, guest, room, check_in_date, check_out_date):
        self._booking_id = Booking._booking_counter
        Booking._booking_counter += 1
        self._guest = guest
        self._room = room
        self._check_in_date = check_in_date
        self._check_out_date = check_out_date
        self._booking_date = date.today()
        self._status = BookingStatus.CONFIRMED
        self._total_cost = self.calculate_total_cost()

    # Геттеры
    def get_booking_id(self):
        return self._booking_id
    def get_guest(self):
        return self._guest
    def get_room(self):
        return self._room
    def get_check_in_date(self):
        return self._check_in_date
    def get_check_out_date(self):
        return self._check_out_date
    def get_booking_date(self):
        return self._booking_date
    def get_status(self):
        return self._status
    def get_total_cost(self):
        return self._total_cost

    # Сеттер для статуса
    def set_status(self, status):
        self._status = status

    # Расчет количества ночей
    def get_number_of_nights(self):
        return (self._check_out_date - self._check_in_date).days

    # Расчет общей стоимости
    def calculate_total_cost(self):
        nights = self.get_number_of_nights()
        base_cost = self._room.get_price_per_night() * nights

        # Скидка при длительном проживании (более 7 ночей - 10% скидка)
        if nights >= 7:
            base_cost *= 0.90

        # Налог 10%
        tax = base_cost * 0.10

        return base_cost + tax

    # Проверка пересечения дат с другим бронированием
    def overlaps_with(self, new_check_in, new_check_out):
        return not (new_check_out <= self._check_in_date or new_check_in >= self._check_out_date)

    # Проверка, активно ли бронирование
    def is_active(self):
        return self._status in [BookingStatus.CONFIRMED, BookingStatus.CHECKED_IN]

    # Отображение информации о бронировании
    def display_info(self):
        print("\n=== Booking Information ===")
        print(f"Booking ID: {self._booking_id}")
        print(f"Guest: {self._guest.get_name()}")
        print(f"Room Number: {self._room.get_room_number()}")
        print(f"Room Type: {self._room.get_type().get_display_name()}")
        print(f"Check-in: {self._check_in_date}")
        print(f"Check-out: {self._check_out_date}")
        print(f"Number of nights: {self.get_number_of_nights()}")
        print(f"Booking Date: {self._booking_date}")
        print(f"Status: {self._status.name}")
        print(f"Total Cost: ${self._total_cost:.2f}")
        print("---")

    # Краткое отображение бронирования
    def display_short(self):
        status_symbols = {
            BookingStatus.CONFIRMED: "✓",
            BookingStatus.CHECKED_IN: "🔑",
            BookingStatus.CHECKED_OUT: "✔",
            BookingStatus.CANCELLED: "✗"
        }
        status_symbol = status_symbols[self._status]

        print(f"[{status_symbol}] Booking #{self._booking_id} | Guest: {self._guest.get_name()} | Room {self._room.get_room_number()} | {self._check_in_date} to {self._check_out_date} | ${self._total_cost:.2f}")

# Класс отеля
class Hotel:
    def __init__(self, hotel_name):
        self._hotel_name = hotel_name
        self._rooms = []
        self._bookings = []
        self._guests = []
        self._initialize_rooms()

    # Инициализация номеров отеля
    def _initialize_rooms(self):
        # Первый этаж - одноместные и двухместные
        self._rooms.append(Room(101, RoomType.SINGLE, 1, False, False))
        self._rooms.append(Room(102, RoomType.SINGLE, 1, False, False))
        self._rooms.append(Room(103, RoomType.DOUBLE, 1, False, False))
        self._rooms.append(Room(104, RoomType.DOUBLE, 1, False, False))

        # Второй этаж - двухместные с балконами
        self._rooms.append(Room(201, RoomType.DOUBLE, 2, True, False))
        self._rooms.append(Room(202, RoomType.DOUBLE, 2, True, False))
        self._rooms.append(Room(203, RoomType.SUITE, 2, True, False))

        # Третий этаж - люксы с видом на море
        self._rooms.append(Room(301, RoomType.SUITE, 3, True, True))
        self._rooms.append(Room(302, RoomType.SUITE, 3, True, True))
        self._rooms.append(Room(303, RoomType.DELUXE, 3, True, True))

    # Добавление гостя
    def add_guest(self, name, email, phone, id_document):
        guest = Guest(name, email, phone, id_document)
        self._guests.append(guest)
        return guest

    # Поиск гостя по ID
    def find_guest_by_id(self, guest_id):
        for guest in self._guests:
            if guest.get_guest_id() == guest_id:
                return guest
        return None

    # Поиск номера по номеру комнаты
    def find_room_by_number(self, room_number):
        for room in self._rooms:
            if room.get_room_number() == room_number:
                return room
        return None

    # Проверка доступности номера
    def check_availability(self, room, check_in, check_out):
        # Проверка базовой доступности номера
        if not room.is_available():
            return False

        # Проверка пересечения с существующими бронированиями
        for booking in self._bookings:
            if (booking.get_room().get_room_number() == room.get_room_number() and
                    booking.is_active() and
                    booking.overlaps_with(check_in, check_out)):
                return False

        return True

    # Получение доступных номеров
    def get_available_rooms(self, check_in, check_out):
        return [room for room in self._rooms if self.check_availability(room, check_in, check_out)]

    # Получение доступных номеров по типу
    def get_available_rooms_by_type(self, room_type, check_in, check_out):
        return [room for room in self._rooms
                if room.get_type() == room_type and self.check_availability(room, check_in, check_out)]

    # Бронирование номера
    def book_room(self, guest, room, check_in, check_out):
        # Валидация дат
        if check_in < date.today():
            print("Error: Check-in date cannot be in the past")
            return None

        if check_out <= check_in:
            print("Error: Check-out date must be after check-in date")
            return None

        # Проверка доступности
        if not self.check_availability(room, check_in, check_out):
            print("Error: Room is not available for the selected dates")
            return None

        # Создание бронирования
        booking = Booking(guest, room, check_in, check_out)
        self._bookings.append(booking)

        print("\n✓ Booking created successfully!")
        print(f"Booking ID: {booking.get_booking_id()}")
        print(f"Total Cost: ${booking.get_total_cost():.2f}")

        return booking

    # Отмена бронирования
    def cancel_booking(self, booking_id):
        booking = self.find_booking_by_id(booking_id)

        if booking is None:
            print("Error: Booking not found")
            return False

        if booking.get_status() == BookingStatus.CANCELLED:
            print("Error: Booking is already cancelled")
            return False

        if booking.get_status() == BookingStatus.CHECKED_OUT:
            print("Error: Cannot cancel completed booking")
            return False

        booking.set_status(BookingStatus.CANCELLED)
        booking.get_room().set_available(True)

        print("\n✓ Booking cancelled successfully!")
        print(f"Booking ID: {booking_id}")

        # Расчет возврата средств
        days_until_check_in = (booking.get_check_in_date() - date.today()).days
        refund = 0

        if days_until_check_in >= 7:
            refund = booking.get_total_cost()  # Полный возврат
            print(f"Full refund: ${refund:.2f}")
        elif days_until_check_in >= 3:
            refund = booking.get_total_cost() * 0.50  # 50% возврат
            print(f"50% refund: ${refund:.2f}")
        else:
            print("No refund (less than 3 days before check-in)")

        return True

    # Поиск бронирования по ID
    def find_booking_by_id(self, booking_id):
        for booking in self._bookings:
            if booking.get_booking_id() == booking_id:
                return booking
        return None

    # Получение бронирований гостя
    def get_guest_bookings(self, guest):
        return [booking for booking in self._bookings
                if booking.get_guest().get_guest_id() == guest.get_guest_id()]

    # Заселение
    def check_in(self, booking_id):
        booking = self.find_booking_by_id(booking_id)

        if booking is None:
            print("Error: Booking not found")
            return False

        if booking.get_status() != BookingStatus.CONFIRMED:
            print("Error: Booking status must be CONFIRMED")
            return False

        if date.today() < booking.get_check_in_date():
            print("Error: Check-in date has not arrived yet")
            return False

        booking.set_status(BookingStatus.CHECKED_IN)
        booking.get_room().set_available(False)

        print("\n✓ Check-in successful!")
        print(f"Welcome, {booking.get_guest().get_name()}!")
        print(f"Room: {booking.get_room().get_room_number()}")

        return True

    # Выселение
    def check_out(self, booking_id):
        booking = self.find_booking_by_id(booking_id)

        if booking is None:
            print("Error: Booking not found")
            return False

        if booking.get_status() != BookingStatus.CHECKED_IN:
            print("Error: Guest is not checked in")
            return False

        booking.set_status(BookingStatus.CHECKED_OUT)
        booking.get_room().set_available(True)

        print("\n✓ Check-out successful!")
        print(f"Thank you for staying with us, {booking.get_guest().get_name()}!")
        print(f"Total paid: ${booking.get_total_cost():.2f}")

        return True

    # Отображение всех номеров
    def display_all_rooms(self):
        print(f"\n=== {self._hotel_name} - All Rooms ===")
        for room in self._rooms:
            room.display_short()
        print(f"\nTotal rooms: {len(self._rooms)}")

    # Отображение всех бронирований
    def display_all_bookings(self):
        if not self._bookings:
            print("\nNo bookings found")
            return

        print("\n=== All Bookings ===")
        for booking in self._bookings:
            booking.display_short()
        print(f"\nTotal bookings: {len(self._bookings)}")

    # Отображение активных бронирований
    def display_active_bookings(self):
        active_bookings = [b for b in self._bookings if b.is_active()]

        if not active_bookings:
            print("\nNo active bookings")
            return

        print("\n=== Active Bookings ===")
        for booking in active_bookings:
            booking.display_short()
        print(f"\nTotal active bookings: {len(active_bookings)}")

    # Отображение статистики отеля
    def display_statistics(self):
        total_rooms = len(self._rooms)
        occupied_rooms = sum(1 for room in self._rooms if not room.is_available())
        total_bookings = len(self._bookings)
        active_bookings = sum(1 for b in self._bookings if b.is_active())
        cancelled_bookings = sum(1 for b in self._bookings if b.get_status() == BookingStatus.CANCELLED)
        total_revenue = sum(b.get_total_cost() for b in self._bookings
                           if b.get_status() == BookingStatus.CHECKED_OUT)

        occupancy_rate = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0

        print(f"\n=== {self._hotel_name} Statistics ===")
        print(f"Total Rooms: {total_rooms}")
        print(f"Occupied Rooms: {occupied_rooms}")
        print(f"Occupancy Rate: {occupancy_rate:.1f}%")
        print("\nBookings:")
        print(f"  Total: {total_bookings}")
        print(f"  Active: {active_bookings}")
        print(f"  Cancelled: {cancelled_bookings}")
        print(f"\nTotal Revenue: ${total_revenue:.2f}")
        print(f"Total Guests: {len(self._guests)}")

# Класс пользовательского интерфейса
class HotelUI:
    def __init__(self, hotel_name):
        self._hotel = Hotel(hotel_name)

    def run(self):
        print("╔════════════════════════════════════════╗")
        print("║  Hotel Booking System                  ║")
        print("╚════════════════════════════════════════╝\n")

        while True:
            try:
                self._display_main_menu()
                choice = int(input())

                if choice == 13:
                    print("\nThank you for using Hotel Booking System!")
                    break

                self._handle_menu_choice(choice)

            except Exception:
                print("\nError: Invalid input. Please try again.")

    # Отображение главного меню
    def _display_main_menu(self):
        print("\n=== Main Menu ===")
        print("1. View all rooms")
        print("2. Check room availability")
        print("3. Make a booking")
        print("4. Cancel booking")
        print("5. View booking details")
        print("6. View all bookings")
        print("7. View active bookings")
        print("8. Check-in")
        print("9. Check-out")
        print("10. Register new guest")
        print("11. View guest bookings")
        print("12. View hotel statistics")
        print("13. Exit")
        print("Enter choice (1-13): ", end='')

    # Обработка выбора меню
    def _handle_menu_choice(self, choice):
        actions = {
            1: self._hotel.display_all_rooms, 2: self._check_availability,
            3: self._make_booking, 4: self._cancel_booking,
            5: self._view_booking_details, 6: self._hotel.display_all_bookings,
            7: self._hotel.display_active_bookings, 8: self._check_in,
            9: self._check_out, 10: self._register_guest,
            11: self._view_guest_bookings, 12: self._hotel.display_statistics
        }
        if choice in actions:
            actions[choice]()
        else:
            print("Invalid choice. Please try again.")

    def _check_availability(self):
        check_in_str = input("\nEnter check-in date (YYYY-MM-DD): ")
        check_out_str = input("Enter check-out date (YYYY-MM-DD): ")

        try:
            check_in = date.fromisoformat(check_in_str)
            check_out = date.fromisoformat(check_out_str)

            available_rooms = self._hotel.get_available_rooms(check_in, check_out)

            if not available_rooms:
                print("\nNo rooms available for these dates")
                return

            print("\n=== Available Rooms ===")
            for room in available_rooms:
                room.display_short()
            print(f"\nAvailable rooms: {len(available_rooms)}")

        except ValueError:
            print("Error: Invalid date format. Use YYYY-MM-DD")

    def _make_booking(self):
        guest_id = int(input("\nEnter guest ID: "))
        guest = self._hotel.find_guest_by_id(guest_id)
        if not guest:
            print("Error: Guest not found. Please register the guest first.")
            return

        room_number = int(input("Enter room number: "))
        room = self._hotel.find_room_by_number(room_number)
        if not room:
            print("Error: Room not found")
            return

        check_in_str = input("Enter check-in date (YYYY-MM-DD): ")
        check_out_str = input("Enter check-out date (YYYY-MM-DD): ")

        try:
            check_in = date.fromisoformat(check_in_str)
            check_out = date.fromisoformat(check_out_str)

            booking = self._hotel.book_room(guest, room, check_in, check_out)

            if booking:
                booking.display_info()

        except ValueError:
            print("Error: Invalid date format. Use YYYY-MM-DD")

    def _cancel_booking(self):
        booking_id = int(input("\nEnter booking ID to cancel: "))
        self._hotel.cancel_booking(booking_id)

    def _view_booking_details(self):
        booking_id = int(input("\nEnter booking ID: "))
        booking = self._hotel.find_booking_by_id(booking_id)
        if booking:
            booking.display_info()
        else:
            print("Error: Booking not found")

    def _check_in(self):
        booking_id = int(input("\nEnter booking ID for check-in: "))
        self._hotel.check_in(booking_id)

    def _check_out(self):
        booking_id = int(input("\nEnter booking ID for check-out: "))
        self._hotel.check_out(booking_id)

    def _register_guest(self):
        name = input("\nEnter guest name: ")
        email = input("Enter email: ")
        phone = input("Enter phone number: ")
        id_document = input("Enter ID document: ")

        guest = self._hotel.add_guest(name, email, phone, id_document)
        print("\n✓ Guest registered successfully!")
        print(f"Guest ID: {guest.get_guest_id()}")

    def _view_guest_bookings(self):
        guest_id = int(input("\nEnter guest ID: "))
        guest = self._hotel.find_guest_by_id(guest_id)
        if not guest:
            print("Error: Guest not found")
            return

        guest_bookings = self._hotel.get_guest_bookings(guest)

        if not guest_bookings:
            print("\nNo bookings found for this guest")
            return

        print(f"\n=== Bookings for {guest.get_name()} ===")
        for booking in guest_bookings:
            booking.display_short()
        print(f"\nTotal bookings: {len(guest_bookings)}")

def main():
    ui = HotelUI("Grand Hotel")
    ui.run()

if __name__ == "__main__":
    main()