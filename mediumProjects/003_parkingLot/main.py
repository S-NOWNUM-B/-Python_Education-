from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime, timedelta
import math

# Перечисление типов парковочных мест
class SpotType(Enum):
    COMPACT = ("Compact", 1)
    REGULAR = ("Regular", 1)
    LARGE = ("Large", 2)
    HANDICAPPED = ("Handicapped", 1)

    def __init__(self, display_name, multiplier):
        self._display_name = display_name
        self._multiplier = multiplier

    def get_display_name(self):
        return self._display_name

    def get_multiplier(self):
        return self._multiplier

# Перечисление статусов парковочного талона
class TicketStatus(Enum):
    ACTIVE = 1
    PAID = 2
    CANCELLED = 3

# Абстрактный класс транспортного средства
class Vehicle(ABC):
    def __init__(self, license_plate, color, owner_name):
        self._license_plate = license_plate
        self._color = color
        self._owner_name = owner_name

    # Геттеры
    def get_license_plate(self):
        return self._license_plate
    def get_color(self):
        return self._color
    def get_owner_name(self):
        return self._owner_name

    # Абстрактный метод получения типа транспорта
    @abstractmethod
    def get_vehicle_type(self):
        pass

    # Абстрактный метод получения подходящих типов мест
    @abstractmethod
    def get_suitable_spot_types(self):
        pass

    # Абстрактный метод расчета базового тарифа (за час)
    @abstractmethod
    def get_hourly_rate(self):
        pass

    # Метод отображения информации
    def display_info(self):
        print(f"Type: {self.get_vehicle_type()}")
        print(f"License Plate: {self._license_plate}")
        print(f"Color: {self._color}")
        print(f"Owner: {self._owner_name}")
        print(f"Hourly Rate: ${self.get_hourly_rate():.2f}")

# Класс мотоцикла
class Motorcycle(Vehicle):
    def __init__(self, license_plate, color, owner_name, engine_capacity):
        super().__init__(license_plate, color, owner_name)
        self._engine_capacity = engine_capacity

    def get_engine_capacity(self):
        return self._engine_capacity

    def get_vehicle_type(self):
        return "Motorcycle"

    def get_suitable_spot_types(self):
        return [SpotType.COMPACT, SpotType.REGULAR]

    def get_hourly_rate(self):
        return 2.0  # $2 в час для мотоциклов

    def display_info(self):
        super().display_info()
        print(f"Engine Capacity: {self._engine_capacity}cc")

# Класс легкового автомобиля
class Car(Vehicle):
    def __init__(self, license_plate, color, owner_name, model, is_electric):
        super().__init__(license_plate, color, owner_name)
        self._model = model
        self._is_electric = is_electric

    def get_model(self):
        return self._model

    def is_electric(self):
        return self._is_electric

    def get_vehicle_type(self):
        return "Electric Car" if self._is_electric else "Car"

    def get_suitable_spot_types(self):
        return [SpotType.REGULAR, SpotType.HANDICAPPED]

    def get_hourly_rate(self):
        return 3.0 if self._is_electric else 4.0  # Скидка для электромобилей

    def display_info(self):
        super().display_info()
        print(f"Model: {self._model}")
        print(f"Electric: {'Yes' if self._is_electric else 'No'}")

# Класс грузовика
class Truck(Vehicle):
    def __init__(self, license_plate, color, owner_name, weight_capacity, number_of_axles):
        super().__init__(license_plate, color, owner_name)
        self._weight_capacity = weight_capacity
        self._number_of_axles = number_of_axles

    def get_weight_capacity(self):
        return self._weight_capacity

    def get_number_of_axles(self):
        return self._number_of_axles

    def get_vehicle_type(self):
        return "Truck"

    def get_suitable_spot_types(self):
        return [SpotType.LARGE]

    def get_hourly_rate(self):
        # Тариф зависит от количества осей
        return 6.0 + (self._number_of_axles - 2) * 2.0

    def display_info(self):
        super().display_info()
        print(f"Weight Capacity: {self._weight_capacity:.1f} tons")
        print(f"Number of Axles: {self._number_of_axles}")

# Класс парковочного места
class ParkingSpot:
    def __init__(self, spot_number, spot_type, floor):
        self._spot_number = spot_number
        self._type = spot_type
        self._is_occupied = False
        self._vehicle = None
        self._floor = floor

    # Геттеры
    def get_spot_number(self):
        return self._spot_number
    def get_type(self):
        return self._type
    def is_occupied(self):
        return self._is_occupied
    def get_vehicle(self):
        return self._vehicle
    def get_floor(self):
        return self._floor

    # Метод занятия места
    def occupy(self, vehicle):
        if self._is_occupied:
            return False

        # Проверка совместимости типа места с транспортом
        if self._type not in vehicle.get_suitable_spot_types():
            return False

        self._vehicle = vehicle
        self._is_occupied = True
        return True

    # Метод освобождения места
    def vacate(self):
        self._vehicle = None
        self._is_occupied = False

    # Метод отображения информации о месте
    def display_info(self):
        print("\n=== Parking Spot Information ===")
        print(f"Spot Number: {self._spot_number}")
        print(f"Type: {self._type.get_display_name()}")
        print(f"Floor: {self._floor}")
        print(f"Status: {'Occupied' if self._is_occupied else 'Available'}")

        if self._is_occupied and self._vehicle:
            print("\nParked Vehicle:")
            self._vehicle.display_info()
        print("---")

    # Метод краткого отображения места
    def display_short(self):
        status = "[X]" if self._is_occupied else "[✓]"
        vehicle_info = f" - {self._vehicle.get_vehicle_type()} ({self._vehicle.get_license_plate()})" if self._is_occupied and self._vehicle else ""

        print(f"{status} Spot #{self._spot_number} | Floor {self._floor} | {self._type.get_display_name()}{vehicle_info}")

# Класс парковочного талона
class ParkingTicket:
    _ticket_counter = 1000

    def __init__(self, vehicle, spot):
        self._ticket_id = ParkingTicket._ticket_counter
        ParkingTicket._ticket_counter += 1
        self._vehicle = vehicle
        self._spot = spot
        self._entry_time = datetime.now()
        self._exit_time = None
        self._status = TicketStatus.ACTIVE
        self._fee = 0.0

    # Геттеры
    def get_ticket_id(self):
        return self._ticket_id
    def get_vehicle(self):
        return self._vehicle
    def get_spot(self):
        return self._spot
    def get_entry_time(self):
        return self._entry_time
    def get_exit_time(self):
        return self._exit_time
    def get_status(self):
        return self._status
    def get_fee(self):
        return self._fee

    # Метод расчета продолжительности парковки
    def get_parking_duration(self):
        end = self._exit_time if self._exit_time else datetime.now()
        return end - self._entry_time

    # Метод расчета стоимости парковки
    def calculate_fee(self):
        duration = self.get_parking_duration()
        minutes = duration.total_seconds() / 60

        # Минимум 1 час
        hours = max(1.0, math.ceil(minutes / 60.0))

        # Базовый тариф транспорта * множитель типа места
        base_rate = self._vehicle.get_hourly_rate()
        spot_multiplier = self._spot.get_type().get_multiplier()

        base_fee = hours * base_rate * spot_multiplier

        # Скидка за длительную парковку (более 24 часов - 20% скидка)
        if hours > 24:
            base_fee *= 0.80

        # Налог 10%
        tax = base_fee * 0.10

        return base_fee + tax

    # Метод завершения парковки
    def complete(self):
        self._exit_time = datetime.now()
        self._fee = self.calculate_fee()
        self._status = TicketStatus.PAID

    # Метод отмены талона
    def cancel(self):
        self._status = TicketStatus.CANCELLED

    # Метод отображения информации о талоне
    def display_info(self):
        print("\n=== Parking Ticket ===")
        print(f"Ticket ID: {self._ticket_id}")
        print(f"Status: {self._status.name}")
        print("\nVehicle:")
        self._vehicle.display_info()
        print(f"\nParking Spot: #{self._spot.get_spot_number()} ({self._spot.get_type().get_display_name()})")
        print(f"Floor: {self._spot.get_floor()}")
        print(f"\nEntry Time: {self._entry_time.strftime('%Y-%m-%d %H:%M:%S')}")

        if self._exit_time:
            print(f"Exit Time: {self._exit_time.strftime('%Y-%m-%d %H:%M:%S')}")

        duration = self.get_parking_duration()
        hours = int(duration.total_seconds() // 3600)
        minutes = int((duration.total_seconds() % 3600) // 60)
        print(f"Duration: {hours} hours {minutes} minutes")

        print(f"Fee: ${self._fee if self._status == TicketStatus.PAID else self.calculate_fee():.2f}")
        print("---")

# Класс парковки
class ParkingLot:
    def __init__(self, name, total_floors):
        self._name = name
        self._spots = []
        self._tickets = []
        self._total_floors = total_floors
        self._initialize_parking_spots()

    # Инициализация парковочных мест
    def _initialize_parking_spots(self):
        spot_number = 1

        for floor in range(1, self._total_floors + 1):
            # На каждом этаже:
            # 5 компактных мест для мотоциклов
            for _ in range(5):
                self._spots.append(ParkingSpot(spot_number, SpotType.COMPACT, floor))
                spot_number += 1

            # 10 обычных мест для легковых
            for _ in range(10):
                self._spots.append(ParkingSpot(spot_number, SpotType.REGULAR, floor))
                spot_number += 1

            # 3 больших места для грузовиков
            for _ in range(3):
                self._spots.append(ParkingSpot(spot_number, SpotType.LARGE, floor))
                spot_number += 1

            # 2 места для инвалидов
            for _ in range(2):
                self._spots.append(ParkingSpot(spot_number, SpotType.HANDICAPPED, floor))
                spot_number += 1

    # Метод получения доступных мест
    def get_available_spots(self):
        return [spot for spot in self._spots if not spot.is_occupied()]

    # Метод получения доступных мест по типу
    def get_available_spots_by_type(self, spot_type):
        return [spot for spot in self._spots if not spot.is_occupied() and spot.get_type() == spot_type]

    # Метод получения доступных мест для транспорта
    def get_available_spots_for_vehicle(self, vehicle):
        suitable_types = vehicle.get_suitable_spot_types()
        return [spot for spot in self._spots if not spot.is_occupied() and spot.get_type() in suitable_types]

    # Метод парковки транспорта
    def park_vehicle(self, vehicle, spot_number):
        # Поиск места
        spot = self.find_spot_by_number(spot_number)

        if not spot:
            print("Error: Parking spot not found")
            return None

        if spot.is_occupied():
            print("Error: Parking spot is already occupied")
            return None

        # Попытка занять место
        if not spot.occupy(vehicle):
            print("Error: Vehicle type not compatible with spot type")
            return None

        # Создание талона
        ticket = ParkingTicket(vehicle, spot)
        self._tickets.append(ticket)

        print("\n✓ Vehicle parked successfully!")
        print(f"Ticket ID: {ticket.get_ticket_id()}")
        print(f"Spot: #{spot.get_spot_number()} (Floor {spot.get_floor()})")
        print(f"Hourly Rate: ${vehicle.get_hourly_rate():.2f}")

        return ticket

    # Метод выезда транспорта
    def remove_vehicle(self, ticket_id):
        ticket = self.find_ticket_by_id(ticket_id)

        if not ticket:
            print("Error: Ticket not found")
            return False

        if ticket.get_status() != TicketStatus.ACTIVE:
            print("Error: Ticket is not active")
            return False

        # Завершение парковки
        ticket.complete()
        ticket.get_spot().vacate()

        print("\n✓ Vehicle removed successfully!")
        ticket.display_info()

        return True

    # Метод поиска места по номеру
    def find_spot_by_number(self, spot_number):
        for spot in self._spots:
            if spot.get_spot_number() == spot_number:
                return spot
        return None

    # Метод поиска талона по ID
    def find_ticket_by_id(self, ticket_id):
        for ticket in self._tickets:
            if ticket.get_ticket_id() == ticket_id:
                return ticket
        return None

    # Метод поиска талона по номеру места
    def find_active_ticket_by_spot(self, spot_number):
        for ticket in self._tickets:
            if (ticket.get_spot().get_spot_number() == spot_number and
                    ticket.get_status() == TicketStatus.ACTIVE):
                return ticket
        return None

    # Метод отображения всех мест
    def display_all_spots(self):
        print(f"\n=== {self._name} - All Parking Spots ===")

        for floor in range(1, self._total_floors + 1):
            print(f"\n--- Floor {floor} ---")
            for spot in self._spots:
                if spot.get_floor() == floor:
                    spot.display_short()

        print(f"\nTotal spots: {len(self._spots)}")

    # Метод отображения доступных мест
    def display_available_spots(self):
        available = self.get_available_spots()

        if not available:
            print("\nNo available spots")
            return

        print("\n=== Available Parking Spots ===")
        for spot in available:
            spot.display_short()
        print(f"\nAvailable spots: {len(available)}")

    # Метод отображения активных талонов
    def display_active_tickets(self):
        active_tickets = [t for t in self._tickets if t.get_status() == TicketStatus.ACTIVE]

        if not active_tickets:
            print("\nNo active tickets")
            return

        print("\n=== Active Parking Tickets ===")
        for ticket in active_tickets:
            print(f"Ticket #{ticket.get_ticket_id()} | Spot #{ticket.get_spot().get_spot_number()} | "
                  f"{ticket.get_vehicle().get_vehicle_type()} | {ticket.get_vehicle().get_license_plate()}")
        print(f"\nActive tickets: {len(active_tickets)}")

    # Метод отображения статистики
    def display_statistics(self):
        total_spots = len(self._spots)
        occupied_spots = sum(1 for spot in self._spots if spot.is_occupied())
        total_tickets = len(self._tickets)
        active_tickets = sum(1 for t in self._tickets if t.get_status() == TicketStatus.ACTIVE)
        total_revenue = sum(t.get_fee() for t in self._tickets if t.get_status() == TicketStatus.PAID)

        # Подсчет по типам транспорта
        motorcycle_count = 0
        car_count = 0
        truck_count = 0

        for spot in self._spots:
            if spot.is_occupied():
                v = spot.get_vehicle()
                if isinstance(v, Motorcycle):
                    motorcycle_count += 1
                elif isinstance(v, Car):
                    car_count += 1
                elif isinstance(v, Truck):
                    truck_count += 1

        occupancy_rate = (occupied_spots / total_spots * 100) if total_spots > 0 else 0

        print(f"\n=== {self._name} Statistics ===")
        print(f"Total Parking Spots: {total_spots}")
        print(f"Occupied Spots: {occupied_spots}")
        print(f"Available Spots: {total_spots - occupied_spots}")
        print(f"Occupancy Rate: {occupancy_rate:.1f}%")

        print("\nVehicle Distribution:")
        print(f"  Motorcycles: {motorcycle_count}")
        print(f"  Cars: {car_count}")
        print(f"  Trucks: {truck_count}")

        print("\nTickets:")
        print(f"  Total Issued: {total_tickets}")
        print(f"  Active: {active_tickets}")
        print(f"  Completed: {total_tickets - active_tickets}")

        print(f"\nTotal Revenue: ${total_revenue:.2f}")

        if total_tickets - active_tickets > 0:
            avg_revenue = total_revenue / (total_tickets - active_tickets)
            print(f"Average Revenue per Ticket: ${avg_revenue:.2f}")

# Класс пользовательского интерфейса
class ParkingLotUI:
    def __init__(self, parking_lot_name, floors):
        self._parking_lot = ParkingLot(parking_lot_name, floors)

    def run(self):
        print("╔════════════════════════════════════════╗")
        print("║  Parking Lot Management System         ║")
        print("╚════════════════════════════════════════╝\n")

        while True:
            try:
                self._display_main_menu()
                choice = int(input())

                if choice == 10:
                    print("\nThank you for using Parking Lot System!")
                    break

                self._handle_menu_choice(choice)

            except Exception:
                print("\nError: Invalid input. Please try again.")

    # Отображение главного меню
    def _display_main_menu(self):
        print("\n=== Main Menu ===")
        print("1. View all parking spots")
        print("2. View available spots")
        print("3. Park vehicle")
        print("4. Remove vehicle")
        print("5. View ticket details")
        print("6. View active tickets")
        print("7. Calculate parking fee")
        print("8. View spot details")
        print("9. View statistics")
        print("10. Exit")
        print("Enter choice (1-10): ", end='')

    # Обработка выбора меню
    def _handle_menu_choice(self, choice):
        actions = {
            1: self._parking_lot.display_all_spots,
            2: self._parking_lot.display_available_spots,
            3: self._park_vehicle,
            4: self._remove_vehicle,
            5: self._view_ticket_details,
            6: self._parking_lot.display_active_tickets,
            7: self._calculate_fee,
            8: self._view_spot_details,
            9: self._parking_lot.display_statistics
        }
        if choice in actions:
            actions[choice]()
        else:
            print("Invalid choice. Please try again.")

    # Парковка транспорта
    def _park_vehicle(self):
        print("\nSelect vehicle type:")
        print("1. Motorcycle")
        print("2. Car")
        print("3. Truck")
        vehicle_type = int(input("Enter choice (1-3): "))

        plate = input("Enter license plate: ")
        color = input("Enter color: ")
        owner = input("Enter owner name: ")

        vehicle = None

        if vehicle_type == 1:  # Motorcycle
            capacity = int(input("Enter engine capacity (cc): "))
            vehicle = Motorcycle(plate, color, owner, capacity)
        elif vehicle_type == 2:  # Car
            model = input("Enter model: ")
            is_electric = input("Is it electric? (y/n): ").lower().startswith('y')
            vehicle = Car(plate, color, owner, model, is_electric)
        elif vehicle_type == 3:  # Truck
            weight = float(input("Enter weight capacity (tons): "))
            axles = int(input("Enter number of axles: "))
            vehicle = Truck(plate, color, owner, weight, axles)
        else:
            print("Invalid vehicle type")
            return

        # Показать доступные места для этого транспорта
        available_spots = self._parking_lot.get_available_spots_for_vehicle(vehicle)

        if not available_spots:
            print("\nNo suitable parking spots available")
            return

        print(f"\n=== Available Spots for {vehicle.get_vehicle_type()} ===")
        for spot in available_spots:
            spot.display_short()

        spot_number = int(input("\nEnter spot number to park: "))

        self._parking_lot.park_vehicle(vehicle, spot_number)

    def _remove_vehicle(self):
        ticket_id = int(input("\nEnter ticket ID: "))
        self._parking_lot.remove_vehicle(ticket_id)

    def _view_ticket_details(self):
        ticket_id = int(input("\nEnter ticket ID: "))
        ticket = self._parking_lot.find_ticket_by_id(ticket_id)

        if ticket:
            ticket.display_info()
        else:
            print("Error: Ticket not found")

    def _calculate_fee(self):
        ticket_id = int(input("\nEnter ticket ID: "))
        ticket = self._parking_lot.find_ticket_by_id(ticket_id)

        if not ticket:
            print("Error: Ticket not found")
            return

        print("\n=== Parking Fee Calculation ===")
        print(f"Ticket ID: {ticket.get_ticket_id()}")
        print(f"Vehicle: {ticket.get_vehicle().get_vehicle_type()} ({ticket.get_vehicle().get_license_plate()})")

        duration = ticket.get_parking_duration()
        hours = int(duration.total_seconds() // 3600)
        minutes = int((duration.total_seconds() % 3600) // 60)
        print(f"Duration: {hours} hours {minutes} minutes")

        print(f"Estimated Fee: ${ticket.calculate_fee():.2f}")

    def _view_spot_details(self):
        spot_number = int(input("\nEnter spot number: "))
        spot = self._parking_lot.find_spot_by_number(spot_number)

        if spot:
            spot.display_info()
        else:
            print("Error: Spot not found")

def main():
    ui = ParkingLotUI("Central Parking", 3)
    ui.run()

if __name__ == "__main__":
    main()