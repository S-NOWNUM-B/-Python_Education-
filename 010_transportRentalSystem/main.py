from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime, date, timedelta
from decimal import Decimal


# Перечисление типов транспорта
class VehicleType(Enum):
    CAR = "Автомобиль"
    BIKE = "Велосипед"
    SCOOTER = "Самокат"
    MOTORCYCLE = "Мотоцикл"

    def __init__(self, display_name):
        self._display_name = display_name

    def get_display_name(self):
        return self._display_name


# Перечисление статусов транспорта
class VehicleStatus(Enum):
    AVAILABLE = "Доступен"
    RENTED = "Арендован"
    MAINTENANCE = "На обслуживании"
    OUT_OF_SERVICE = "Вне эксплуатации"

    def __init__(self, display_name):
        self._display_name = display_name

    def get_display_name(self):
        return self._display_name


# Перечисление типов топлива
class FuelType(Enum):
    GASOLINE = "Бензин"
    DIESEL = "Дизель"
    ELECTRIC = "Электро"
    HYBRID = "Гибрид"
    NONE = "Без топлива"

    def __init__(self, display_name):
        self._display_name = display_name

    def get_display_name(self):
        return self._display_name


# Перечисление статусов аренды
class RentalStatus(Enum):
    ACTIVE = "Активная"
    COMPLETED = "Завершена"
    CANCELLED = "Отменена"
    OVERDUE = "Просрочена"

    def __init__(self, display_name):
        self._display_name = display_name

    def get_display_name(self):
        return self._display_name


# Абстрактный класс транспортного средства
class Vehicle(ABC):
    _vehicle_counter = 1

    def __init__(self, model, daily_rate, year=2024):
        self._vehicle_id = f"VEH{Vehicle._vehicle_counter:04d}"
        Vehicle._vehicle_counter += 1
        self._model = model
        self._daily_rate = Decimal(str(daily_rate))
        self._year = year
        self._is_rented = False
        self._status = VehicleStatus.AVAILABLE
        self._mileage = 0
        self._registration_date = date.today()
        self._last_maintenance = date.today()
        self._total_rentals = 0

    # Геттеры
    def get_vehicle_id(self):
        return self._vehicle_id

    def get_model(self):
        return self._model

    def get_daily_rate(self):
        return float(self._daily_rate)

    def get_year(self):
        return self._year

    def is_rented(self):
        return self._is_rented

    def get_status(self):
        return self._status

    def get_mileage(self):
        return self._mileage

    def get_registration_date(self):
        return self._registration_date

    def get_last_maintenance(self):
        return self._last_maintenance

    def get_total_rentals(self):
        return self._total_rentals

    # Сеттеры
    def set_status(self, status):
        self._status = status

    def set_mileage(self, mileage):
        self._mileage = mileage

    def set_last_maintenance(self, maintenance_date):
        self._last_maintenance = maintenance_date

    # Абстрактные методы
    @abstractmethod
    def get_vehicle_type(self):
        pass

    @abstractmethod
    def get_specific_details(self):
        pass

    @abstractmethod
    def calculate_insurance_cost(self):
        pass

    # Метод аренды транспорта
    def rent(self):
        if self._is_rented:
            return False
        if self._status != VehicleStatus.AVAILABLE:
            return False

        self._is_rented = True
        self._status = VehicleStatus.RENTED
        self._total_rentals += 1
        return True

    # Метод возврата транспорта
    def return_vehicle(self, new_mileage=None):
        if not self._is_rented:
            return False

        self._is_rented = False
        self._status = VehicleStatus.AVAILABLE

        if new_mileage and new_mileage > self._mileage:
            self._mileage = new_mileage

        return True

    # Метод проверки необходимости обслуживания
    def needs_maintenance(self):
        days_since_maintenance = (date.today() - self._last_maintenance).days
        return days_since_maintenance > 90  # Каждые 90 дней

    # Метод отображения информации о транспорте
    def display_info(self):
        print("\n=== Информация о транспорте ===")
        print(f"ID: {self._vehicle_id}")
        print(f"Тип: {self.get_vehicle_type().get_display_name()}")
        print(f"Модель: {self._model}")
        print(f"Год выпуска: {self._year}")
        print(f"Тариф: ${self._daily_rate:.2f}/день")
        print(f"Статус: {self._status.get_display_name()}")
        print(f"Пробег: {self._mileage} км")
        print(f"Всего аренд: {self._total_rentals}")
        print(f"Последнее ТО: {self._last_maintenance}")

        if self.needs_maintenance():
            print("⚠️  Требуется техническое обслуживание")

        specific = self.get_specific_details()
        if specific:
            print(specific)

        print("---")

    # Метод краткого отображения транспорта
    def display_short(self):
        status_symbol = {
            VehicleStatus.AVAILABLE: "✓",
            VehicleStatus.RENTED: "🚗",
            VehicleStatus.MAINTENANCE: "🔧",
            VehicleStatus.OUT_OF_SERVICE: "✗"
        }
        symbol = status_symbol.get(self._status, "?")

        print(f"[{symbol}] {self._vehicle_id} | {self.get_vehicle_type().get_display_name():12} | "
              f"{self._model:25} | ${self._daily_rate:>7.2f}/день | {self._status.get_display_name()}")


# Класс автомобиля
class Car(Vehicle):
    def __init__(self, model, daily_rate, year, fuel_type, seats, transmission="Автомат"):
        super().__init__(model, daily_rate, year)
        self._fuel_type = fuel_type
        self._seats = seats
        self._transmission = transmission
        self._has_ac = True
        self._trunk_capacity = 400  # литры

    def get_fuel_type(self):
        return self._fuel_type

    def get_seats(self):
        return self._seats

    def get_transmission(self):
        return self._transmission

    def has_ac(self):
        return self._has_ac

    def get_vehicle_type(self):
        return VehicleType.CAR

    def calculate_insurance_cost(self):
        # Страховка зависит от стоимости аренды и года выпуска
        base_insurance = float(self._daily_rate) * 0.15
        age_discount = max(0, (2024 - self._year) * 0.5)
        return base_insurance - age_discount

    def get_specific_details(self):
        return (f"Топливо: {self._fuel_type.get_display_name()} | "
                f"Мест: {self._seats} | КПП: {self._transmission} | "
                f"Кондиционер: {'Да' if self._has_ac else 'Нет'}")


# Класс велосипеда
class Bike(Vehicle):
    def __init__(self, model, daily_rate, year, bike_type="Городской", gears=21):
        super().__init__(model, daily_rate, year)
        self._bike_type = bike_type
        self._gears = gears
        self._has_basket = True
        self._frame_size = "M"

    def get_bike_type(self):
        return self._bike_type

    def get_gears(self):
        return self._gears

    def has_basket(self):
        return self._has_basket

    def get_vehicle_type(self):
        return VehicleType.BIKE

    def calculate_insurance_cost(self):
        # Минимальная страховка для велосипедов
        return 2.0

    def get_specific_details(self):
        return (f"Тип: {self._bike_type} | Передач: {self._gears} | "
                f"Корзина: {'Да' if self._has_basket else 'Нет'} | "
                f"Размер рамы: {self._frame_size}")


# Класс самоката
class Scooter(Vehicle):
    def __init__(self, model, daily_rate, year, max_speed=25, battery_range=30):
        super().__init__(model, daily_rate, year)
        self._max_speed = max_speed  # км/ч
        self._battery_range = battery_range  # км
        self._battery_level = 100  # процент
        self._is_electric = True

    def get_max_speed(self):
        return self._max_speed

    def get_battery_range(self):
        return self._battery_range

    def get_battery_level(self):
        return self._battery_level

    def set_battery_level(self, level):
        self._battery_level = max(0, min(100, level))

    def get_vehicle_type(self):
        return VehicleType.SCOOTER

    def calculate_insurance_cost(self):
        # Средняя страховка для самокатов
        return 3.0

    def get_specific_details(self):
        return (f"Макс. скорость: {self._max_speed} км/ч | "
                f"Запас хода: {self._battery_range} км | "
                f"Заряд батареи: {self._battery_level}%")


# Класс мотоцикла
class Motorcycle(Vehicle):
    def __init__(self, model, daily_rate, year, engine_capacity, fuel_type=FuelType.GASOLINE):
        super().__init__(model, daily_rate, year)
        self._engine_capacity = engine_capacity  # куб.см
        self._fuel_type = fuel_type
        self._has_abs = True

    def get_engine_capacity(self):
        return self._engine_capacity

    def get_fuel_type(self):
        return self._fuel_type

    def get_vehicle_type(self):
        return VehicleType.MOTORCYCLE

    def calculate_insurance_cost(self):
        # Высокая страховка для мотоциклов
        base = float(self._daily_rate) * 0.20
        engine_factor = self._engine_capacity / 1000 * 2
        return base + engine_factor

    def get_specific_details(self):
        return (f"Объем двигателя: {self._engine_capacity} см³ | "
                f"Топливо: {self._fuel_type.get_display_name()} | "
                f"ABS: {'Да' if self._has_abs else 'Нет'}")


# Класс клиента
class Customer:
    _customer_counter = 1

    def __init__(self, name, phone, email, driver_license=""):
        self._customer_id = f"CUST{Customer._customer_counter:04d}"
        Customer._customer_counter += 1
        self._name = name
        self._phone = phone
        self._email = email
        self._driver_license = driver_license
        self._registration_date = date.today()
        self._rental_history = []
        self._total_spent = Decimal('0')

    # Геттеры
    def get_customer_id(self):
        return self._customer_id

    def get_name(self):
        return self._name

    def get_phone(self):
        return self._phone

    def get_email(self):
        return self._email

    def get_driver_license(self):
        return self._driver_license

    def get_rental_history(self):
        return self._rental_history

    def get_total_spent(self):
        return float(self._total_spent)

    # Метод добавления аренды в историю
    def add_rental(self, rental):
        self._rental_history.append(rental)

    # Метод обновления потраченной суммы
    def add_to_total_spent(self, amount):
        self._total_spent += Decimal(str(amount))

    # Метод получения активных аренд
    def get_active_rentals(self):
        return [r for r in self._rental_history if r.get_status() == RentalStatus.ACTIVE]

    # Метод отображения информации о клиенте
    def display_info(self):
        print("\n=== Информация о клиенте ===")
        print(f"ID: {self._customer_id}")
        print(f"Имя: {self._name}")
        print(f"Телефон: {self._phone}")
        print(f"Email: {self._email}")
        if self._driver_license:
            print(f"Водительское удостоверение: {self._driver_license}")
        print(f"Дата регистрации: {self._registration_date}")
        print(f"Всего аренд: {len(self._rental_history)}")
        print(f"Активных аренд: {len(self.get_active_rentals())}")
        print(f"Всего потрачено: ${self._total_spent:.2f}")
        print("---")

    # Метод краткого отображения клиента
    def display_short(self):
        active = len(self.get_active_rentals())
        print(f"{self._customer_id} | {self._name:25} | {self._phone:15} | "
              f"Аренд: {len(self._rental_history):>3} | Активных: {active}")


# Класс аренды
class Rental:
    _rental_counter = 1

    def __init__(self, customer, vehicle, start_date, planned_end_date):
        self._rental_id = f"RENT{Rental._rental_counter:04d}"
        Rental._rental_counter += 1
        self._customer = customer
        self._vehicle = vehicle
        self._start_date = start_date
        self._planned_end_date = planned_end_date
        self._actual_end_date = None
        self._status = RentalStatus.ACTIVE
        self._rental_cost = Decimal('0')
        self._late_fee = Decimal('0')
        self._insurance_cost = Decimal(str(vehicle.calculate_insurance_cost()))
        self._total_cost = Decimal('0')
        self._payment_completed = False

    # Геттеры
    def get_rental_id(self):
        return self._rental_id

    def get_customer(self):
        return self._customer

    def get_vehicle(self):
        return self._vehicle

    def get_start_date(self):
        return self._start_date

    def get_planned_end_date(self):
        return self._planned_end_date

    def get_actual_end_date(self):
        return self._actual_end_date

    def get_status(self):
        return self._status

    def get_total_cost(self):
        return float(self._total_cost)

    def is_payment_completed(self):
        return self._payment_completed

    # Метод расчета количества дней аренды
    def calculate_rental_days(self):
        end_date = self._actual_end_date if self._actual_end_date else date.today()
        days = (end_date - self._start_date).days
        return max(1, days)  # Минимум 1 день

    # Метод расчета стоимости аренды
    def calculate_rental_cost(self):
        days = self.calculate_rental_days()
        daily_rate = Decimal(str(self._vehicle.get_daily_rate()))

        # Скидка за длительную аренду
        discount = Decimal('0')
        if days >= 7:
            discount = daily_rate * Decimal(str(days)) * Decimal('0.10')  # 10% скидка
        elif days >= 3:
            discount = daily_rate * Decimal(str(days)) * Decimal('0.05')  # 5% скидка

        base_cost = daily_rate * Decimal(str(days)) - discount
        return base_cost

    # Метод расчета штрафа за просрочку
    def calculate_late_fee(self):
        if not self._actual_end_date:
            return Decimal('0')

        if self._actual_end_date <= self._planned_end_date:
            return Decimal('0')

        late_days = (self._actual_end_date - self._planned_end_date).days
        daily_rate = Decimal(str(self._vehicle.get_daily_rate()))

        # Штраф = 150% от дневной ставки за каждый день просрочки
        late_fee = daily_rate * Decimal('1.5') * Decimal(str(late_days))
        return late_fee

    # Метод расчета общей стоимости
    def calculate_total_cost(self):
        rental_cost = self.calculate_rental_cost()
        late_fee = self.calculate_late_fee()
        insurance = self._insurance_cost * Decimal(str(self.calculate_rental_days()))

        total = rental_cost + late_fee + insurance
        return total

    # Метод проверки просрочки
    def is_overdue(self):
        if self._status != RentalStatus.ACTIVE:
            return False
        return date.today() > self._planned_end_date

    # Метод завершения аренды
    def complete_rental(self, return_date=None):
        if self._status != RentalStatus.ACTIVE:
            print("Ошибка: Аренда уже завершена")
            return False

        self._actual_end_date = return_date if return_date else date.today()

        # Расчет стоимости
        self._rental_cost = self.calculate_rental_cost()
        self._late_fee = self.calculate_late_fee()
        self._total_cost = self.calculate_total_cost()

        # Обновление статуса
        if self._late_fee > 0:
            self._status = RentalStatus.OVERDUE
        else:
            self._status = RentalStatus.COMPLETED

        # Возврат транспорта
        self._vehicle.return_vehicle()

        print(f"\n✓ Аренда завершена")
        print(f"Стоимость аренды: ${self._rental_cost:.2f}")
        if self._late_fee > 0:
            print(f"Штраф за просрочку: ${self._late_fee:.2f}")
        print(f"Страховка: ${float(self._insurance_cost * Decimal(str(self.calculate_rental_days()))):.2f}")
        print(f"Итого к оплате: ${self._total_cost:.2f}")

        return True

    # Метод оплаты
    def complete_payment(self):
        if self._status == RentalStatus.ACTIVE:
            print("Ошибка: Сначала завершите аренду")
            return False

        if self._payment_completed:
            print("Ошибка: Оплата уже произведена")
            return False

        self._payment_completed = True
        self._customer.add_to_total_spent(float(self._total_cost))

        print(f"\n✓ Оплата получена: ${self._total_cost:.2f}")
        return True

    # Метод отмены аренды
    def cancel_rental(self):
        if self._status != RentalStatus.ACTIVE:
            print("Ошибка: Можно отменить только активную аренду")
            return False

        self._status = RentalStatus.CANCELLED
        self._vehicle.return_vehicle()

        print(f"\n✓ Аренда отменена")
        return True

    # Метод отображения информации об аренде
    def display_info(self):
        print("\n=== Информация об аренде ===")
        print(f"ID аренды: {self._rental_id}")
        print(f"Клиент: {self._customer.get_name()}")
        print(f"Транспорт: {self._vehicle.get_model()} ({self._vehicle.get_vehicle_id()})")
        print(f"Тип: {self._vehicle.get_vehicle_type().get_display_name()}")
        print(f"Статус: {self._status.get_display_name()}")
        print(f"Начало: {self._start_date}")
        print(f"Плановое окончание: {self._planned_end_date}")

        if self._actual_end_date:
            print(f"Фактическое окончание: {self._actual_end_date}")

        days = self.calculate_rental_days()
        print(f"Дней аренды: {days}")

        if self._status != RentalStatus.ACTIVE:
            print(f"\nСтоимость аренды: ${self._rental_cost:.2f}")
            if self._late_fee > 0:
                print(f"Штраф за просрочку: ${self._late_fee:.2f}")
            insurance_total = float(self._insurance_cost * Decimal(str(days)))
            print(f"Страховка: ${insurance_total:.2f}")
            print(f"Итого: ${self._total_cost:.2f}")
            print(f"Оплачено: {'Да' if self._payment_completed else 'Нет'}")
        else:
            estimated_cost = self.calculate_total_cost()
            print(f"\nОценочная стоимость: ${estimated_cost:.2f}")

            if self.is_overdue():
                days_overdue = (date.today() - self._planned_end_date).days
                print(f"⚠️  ПРОСРОЧЕНО на {days_overdue} дней")

        print("---")

    # Метод краткого отображения аренды
    def display_short(self):
        status_symbol = {
            RentalStatus.ACTIVE: "🔄",
            RentalStatus.COMPLETED: "✅",
            RentalStatus.CANCELLED: "❌",
            RentalStatus.OVERDUE: "⚠️"
        }
        symbol = status_symbol.get(self._status, "?")

        overdue = ""
        if self.is_overdue() and self._status == RentalStatus.ACTIVE:
            overdue = " [ПРОСРОЧЕНО]"

        print(f"{symbol} {self._rental_id} | {self._customer.get_name():20} | "
              f"{self._vehicle.get_model():25} | {self._start_date} → {self._planned_end_date} | "
              f"{self._status.get_display_name()}{overdue}")


# Класс сервиса аренды
class RentalService:
    def __init__(self, service_name):
        self._service_name = service_name
        self._vehicles = []
        self._customers = []
        self._rentals = []
        self._total_revenue = Decimal('0')

    # Метод добавления транспорта
    def add_vehicle(self, vehicle):
        self._vehicles.append(vehicle)
        print(f"\n✓ Транспорт добавлен: {vehicle.get_model()}")
        return vehicle

    # Метод добавления клиента
    def add_customer(self, customer):
        self._customers.append(customer)
        print(f"\n✓ Клиент зарегистрирован: {customer.get_name()}")
        return customer

    # Метод поиска транспорта по ID
    def find_vehicle(self, vehicle_id):
        for vehicle in self._vehicles:
            if vehicle.get_vehicle_id() == vehicle_id:
                return vehicle
        return None

    # Метод поиска клиента по ID
    def find_customer(self, customer_id):
        for customer in self._customers:
            if customer.get_customer_id() == customer_id:
                return customer
        return None

    # Метод поиска аренды по ID
    def find_rental(self, rental_id):
        for rental in self._rentals:
            if rental.get_rental_id() == rental_id:
                return rental
        return None

    # Метод получения доступного транспорта
    def get_available_vehicles(self, vehicle_type=None):
        available = [v for v in self._vehicles if v.get_status() == VehicleStatus.AVAILABLE]

        if vehicle_type:
            available = [v for v in available if v.get_vehicle_type() == vehicle_type]

        return available

    # Метод аренды транспорта
    def rent_vehicle(self, customer_id, vehicle_id, start_date, planned_end_date):
        customer = self.find_customer(customer_id)
        if not customer:
            print("Ошибка: Клиент не найден")
            return None

        vehicle = self.find_vehicle(vehicle_id)
        if not vehicle:
            print("Ошибка: Транспорт не найден")
            return None

        if vehicle.get_status() != VehicleStatus.AVAILABLE:
            print(f"Ошибка: Транспорт недоступен (Статус: {vehicle.get_status().get_display_name()})")
            return None

        # Проверка дат
        if start_date > planned_end_date:
            print("Ошибка: Дата начала не может быть позже даты окончания")
            return None

        if start_date < date.today():
            print("Ошибка: Дата начала не может быть в прошлом")
            return None

        # Создание аренды
        rental = Rental(customer, vehicle, start_date, planned_end_date)

        # Аренда транспорта
        if vehicle.rent():
            self._rentals.append(rental)
            customer.add_rental(rental)

            days = (planned_end_date - start_date).days
            estimated_cost = rental.calculate_total_cost()

            print(f"\n✓ Транспорт арендован")
            print(f"ID аренды: {rental.get_rental_id()}")
            print(f"Транспорт: {vehicle.get_model()}")
            print(f"Период: {start_date} - {planned_end_date} ({days} дней)")
            print(f"Оценочная стоимость: ${estimated_cost:.2f}")

            return rental

        print("Ошибка: Не удалось арендовать транспорт")
        return None

    # Метод возврата транспорта
    def return_vehicle(self, rental_id, return_date=None):
        rental = self.find_rental(rental_id)
        if not rental:
            print("Ошибка: Аренда не найдена")
            return False

        return rental.complete_rental(return_date)

    # Метод расчета штрафа за просрочку
    def calculate_late_fee(self, rental_id):
        rental = self.find_rental(rental_id)
        if not rental:
            print("Ошибка: Аренда не найдена")
            return None

        late_fee = rental.calculate_late_fee()

        if late_fee > 0:
            print(f"\n=== Штраф за просрочку ===")
            print(f"ID аренды: {rental_id}")
            print(f"Штраф: ${late_fee:.2f}")
        else:
            print("\n✓ Просрочки нет")

        return float(late_fee)

    # Метод получения истории аренд клиента
    def get_rental_history(self, customer_id):
        customer = self.find_customer(customer_id)
        if not customer:
            print("Ошибка: Клиент не найден")
            return []

        return customer.get_rental_history()

    # Метод получения активных аренд
    def get_active_rentals(self):
        return [r for r in self._rentals if r.get_status() == RentalStatus.ACTIVE]

    # Метод получения просроченных аренд
    def get_overdue_rentals(self):
        return [r for r in self._rentals if r.is_overdue()]

    # Метод отображения доступного транспорта
    def display_available_vehicles(self, vehicle_type=None):
        vehicles = self.get_available_vehicles(vehicle_type)

        if not vehicles:
            type_msg = f" ({vehicle_type.get_display_name()})" if vehicle_type else ""
            print(f"\nНет доступного транспорта{type_msg}")
            return

        type_title = f" - {vehicle_type.get_display_name()}" if vehicle_type else ""
        print(f"\n=== Доступный транспорт{type_title} ===")
        for vehicle in vehicles:
            vehicle.display_short()
        print(f"\nВсего доступно: {len(vehicles)}")

    # Метод отображения всего транспорта
    def display_all_vehicles(self):
        if not self._vehicles:
            print("\nНет транспорта в парке")
            return

        print(f"\n=== Весь транспорт ===")
        for vehicle in self._vehicles:
            vehicle.display_short()
        print(f"\nВсего транспорта: {len(self._vehicles)}")

    # Метод отображения всех клиентов
    def display_all_customers(self):
        if not self._customers:
            print("\nНет зарегистрированных клиентов")
            return

        print(f"\n=== Все клиенты ===")
        for customer in self._customers:
            customer.display_short()
        print(f"\nВсего клиентов: {len(self._customers)}")

    # Метод отображения активных аренд
    def display_active_rentals(self):
        rentals = self.get_active_rentals()

        if not rentals:
            print("\nНет активных аренд")
            return

        print("\n=== Активные аренды ===")
        for rental in rentals:
            rental.display_short()
        print(f"\nВсего активных: {len(rentals)}")

    # Метод отображения просроченных аренд
    def display_overdue_rentals(self):
        rentals = self.get_overdue_rentals()

        if not rentals:
            print("\n✓ Нет просроченных аренд")
            return

        print("\n⚠️  === Просроченные аренды ===")
        for rental in rentals:
            rental.display_short()
        print(f"\nВсего просроченных: {len(rentals)}")

    # Метод отображения статистики
    def display_statistics(self):
        total_vehicles = len(self._vehicles)
        available_vehicles = len(self.get_available_vehicles())
        rented_vehicles = sum(1 for v in self._vehicles if v.is_rented())
        maintenance_vehicles = sum(1 for v in self._vehicles
                                   if v.get_status() == VehicleStatus.MAINTENANCE)

        total_customers = len(self._customers)
        total_rentals = len(self._rentals)
        active_rentals = len(self.get_active_rentals())
        completed_rentals = sum(1 for r in self._rentals
                                if r.get_status() == RentalStatus.COMPLETED)
        overdue_rentals = len(self.get_overdue_rentals())

        # Расчет выручки
        revenue = sum(r.get_total_cost() for r in self._rentals
                      if r.is_payment_completed())

        print(f"\n=== Статистика '{self._service_name}' ===")
        print(f"\nТранспорт:")
        print(f"  Всего: {total_vehicles}")
        print(f"  Доступно: {available_vehicles}")
        print(f"  Арендовано: {rented_vehicles}")
        print(f"  На обслуживании: {maintenance_vehicles}")

        print(f"\nКлиенты:")
        print(f"  Всего: {total_customers}")

        print(f"\nАренды:")
        print(f"  Всего: {total_rentals}")
        print(f"  Активных: {active_rentals}")
        print(f"  Завершенных: {completed_rentals}")
        if overdue_rentals > 0:
            print(f"  ⚠️  Просроченных: {overdue_rentals}")

        print(f"\nВыручка: ${revenue:.2f}")

        # Топ транспорта по популярности
        if self._vehicles:
            top_vehicles = sorted(self._vehicles,
                                  key=lambda v: v.get_total_rentals(),
                                  reverse=True)[:3]
            print(f"\nТоп-3 популярного транспорта:")
            for i, vehicle in enumerate(top_vehicles, 1):
                if vehicle.get_total_rentals() > 0:
                    print(f"  {i}. {vehicle.get_model()} - {vehicle.get_total_rentals()} аренд")


# Класс пользовательского интерфейса
class RentalServiceUI:
    def __init__(self, service_name):
        self._service = RentalService(service_name)
        self._initialize_sample_data()

    # Инициализация примерных данных
    def _initialize_sample_data(self):
        # Добавление транспорта
        car1 = Car("Toyota Camry 2023", 50, 2023, FuelType.GASOLINE, 5, "Автомат")
        car2 = Car("Tesla Model 3", 80, 2024, FuelType.ELECTRIC, 5, "Автомат")
        bike1 = Bike("Giant Escape 3", 15, 2023, "Городской", 21)
        bike2 = Bike("Trek FX 2", 18, 2024, "Гибрид", 24)
        scooter1 = Scooter("Xiaomi Mi Electric", 10, 2024, 25, 30)
        scooter2 = Scooter("Ninebot ES4", 12, 2024, 30, 45)
        moto1 = Motorcycle("Honda CB500F", 60, 2023, 471, FuelType.GASOLINE)

        self._service.add_vehicle(car1)
        self._service.add_vehicle(car2)
        self._service.add_vehicle(bike1)
        self._service.add_vehicle(bike2)
        self._service.add_vehicle(scooter1)
        self._service.add_vehicle(scooter2)
        self._service.add_vehicle(moto1)

        # Добавление клиентов
        customer1 = Customer("Алексей Петров", "+7-999-123-4567", "alexey@example.com", "7712345678")
        customer2 = Customer("Мария Иванова", "+7-999-987-6543", "maria@example.com", "7798765432")

        self._service.add_customer(customer1)
        self._service.add_customer(customer2)

    def run(self):
        print("╔════════════════════════════════════════╗")
        print("║  Система аренды транспорта             ║")
        print("╚════════════════════════════════════════╝\n")

        while True:
            try:
                self._display_main_menu()
                choice = int(input())

                if choice == 20:
                    print("\nСпасибо за использование нашего сервиса!")
                    break

                self._handle_menu_choice(choice)

            except Exception:
                print("\nОшибка: Неверный ввод. Попробуйте снова.")

    # Отображение главного меню
    def _display_main_menu(self):
        print("\n=== Главное меню ===")
        print("\n--- Транспорт ---")
        print("1. Добавить транспорт")
        print("2. Просмотреть весь транспорт")
        print("3. Просмотреть доступный транспорт")
        print("4. Просмотреть детали транспорта")
        print("5. Установить статус транспорта")

        print("\n--- Клиенты ---")
        print("6. Зарегистрировать клиента")
        print("7. Просмотреть всех клиентов")
        print("8. Просмотреть детали клиента")
        print("9. История аренд клиента")

        print("\n--- Аренда ---")
        print("10. Арендовать транспорт")
        print("11. Вернуть транспорт")
        print("12. Просмотреть детали аренды")
        print("13. Просмотреть активные аренды")
        print("14. Просмотреть просроченные аренды")
        print("15. Рассчитать штраф")
        print("16. Оплатить аренду")
        print("17. Отменить аренду")

        print("\n--- Система ---")
        print("18. Фильтр по типу транспорта")
        print("19. Статистика")
        print("20. Выход")
        print("Введите выбор (1-20): ", end='')

    # Обработка выбора меню
    def _handle_menu_choice(self, choice):
        actions = {
            1: self._add_vehicle,
            2: self._service.display_all_vehicles,
            3: self._display_available_vehicles,
            4: self._view_vehicle_details,
            5: self._set_vehicle_status,
            6: self._register_customer,
            7: self._service.display_all_customers,
            8: self._view_customer_details,
            9: self._view_customer_history,
            10: self._rent_vehicle,
            11: self._return_vehicle,
            12: self._view_rental_details,
            13: self._service.display_active_rentals,
            14: self._service.display_overdue_rentals,
            15: self._calculate_late_fee,
            16: self._complete_payment,
            17: self._cancel_rental,
            18: self._filter_by_type,
            19: self._service.display_statistics
        }

        if choice in actions:
            actions[choice]()
        else:
            print("Неверный выбор. Попробуйте снова.")

    def _add_vehicle(self):
        print("\nВыберите тип транспорта:")
        print("1. Автомобиль")
        print("2. Велосипед")
        print("3. Самокат")
        print("4. Мотоцикл")

        vehicle_type = int(input("Введите выбор (1-4): "))
        model = input("Модель: ")
        daily_rate = float(input("Тариф ($/день): "))
        year = int(input("Год выпуска: "))

        vehicle = None

        if vehicle_type == 1:  # Автомобиль
            print("\nВыберите тип топлива:")
            for i, fuel in enumerate(FuelType, 1):
                if fuel != FuelType.NONE:
                    print(f"{i}. {fuel.get_display_name()}")
            fuel_choice = int(input("Введите выбор: "))
            fuel_type = list(FuelType)[fuel_choice - 1]

            seats = int(input("Количество мест: "))
            transmission = input("КПП (Автомат/Механика): ")

            vehicle = Car(model, daily_rate, year, fuel_type, seats, transmission)

        elif vehicle_type == 2:  # Велосипед
            bike_type = input("Тип велосипеда (Городской/Горный/Шоссейный): ")
            gears = int(input("Количество передач: "))

            vehicle = Bike(model, daily_rate, year, bike_type, gears)

        elif vehicle_type == 3:  # Самокат
            max_speed = int(input("Максимальная скорость (км/ч): "))
            battery_range = int(input("Запас хода (км): "))

            vehicle = Scooter(model, daily_rate, year, max_speed, battery_range)

        elif vehicle_type == 4:  # Мотоцикл
            engine = int(input("Объем двигателя (см³): "))

            print("\nВыберите тип топлива:")
            for i, fuel in enumerate([FuelType.GASOLINE, FuelType.DIESEL], 1):
                print(f"{i}. {fuel.get_display_name()}")
            fuel_choice = int(input("Введите выбор: "))
            fuel_type = [FuelType.GASOLINE, FuelType.DIESEL][fuel_choice - 1]

            vehicle = Motorcycle(model, daily_rate, year, engine, fuel_type)

        if vehicle:
            self._service.add_vehicle(vehicle)

    def _display_available_vehicles(self):
        print("\nФильтр по типу? (Enter для пропуска)")
        print("1. Все")
        print("2. Автомобили")
        print("3. Велосипеды")
        print("4. Самокаты")
        print("5. Мотоциклы")

        choice_str = input("Выбор: ").strip()

        if not choice_str or choice_str == "1":
            self._service.display_available_vehicles()
        else:
            choice = int(choice_str)
            type_map = {
                2: VehicleType.CAR,
                3: VehicleType.BIKE,
                4: VehicleType.SCOOTER,
                5: VehicleType.MOTORCYCLE
            }
            if choice in type_map:
                self._service.display_available_vehicles(type_map[choice])

    def _view_vehicle_details(self):
        vehicle_id = input("\nВведите ID транспорта: ")
        vehicle = self._service.find_vehicle(vehicle_id)

        if vehicle:
            vehicle.display_info()
        else:
            print("Транспорт не найден")

    def _set_vehicle_status(self):
        vehicle_id = input("\nВведите ID транспорта: ")
        vehicle = self._service.find_vehicle(vehicle_id)

        if not vehicle:
            print("Транспорт не найден")
            return

        print("\nВыберите статус:")
        for i, status in enumerate(VehicleStatus, 1):
            print(f"{i}. {status.get_display_name()}")

        status_choice = int(input("Введите выбор: "))
        new_status = list(VehicleStatus)[status_choice - 1]

        vehicle.set_status(new_status)
        print(f"\n✓ Статус обновлен: {new_status.get_display_name()}")

    def _register_customer(self):
        name = input("\nИмя клиента: ")
        phone = input("Телефон: ")
        email = input("Email: ")
        license = input("Водительское удостоверение (опционально): ")

        customer = Customer(name, phone, email, license)
        self._service.add_customer(customer)

    def _view_customer_details(self):
        customer_id = input("\nВведите ID клиента: ")
        customer = self._service.find_customer(customer_id)

        if customer:
            customer.display_info()
        else:
            print("Клиент не найден")

    def _view_customer_history(self):
        customer_id = input("\nВведите ID клиента: ")
        rentals = self._service.get_rental_history(customer_id)

        if not rentals:
            print("\nУ клиента нет истории аренд")
            return

        print(f"\n=== История аренд клиента ===")
        for rental in rentals:
            rental.display_short()
        print(f"\nВсего аренд: {len(rentals)}")

    def _rent_vehicle(self):
        customer_id = input("\nID клиента: ")
        vehicle_id = input("ID транспорта: ")

        start_str = input("Дата начала (ГГГГ-ММ-ДД) или Enter для сегодня: ").strip()
        start_date = date.fromisoformat(start_str) if start_str else date.today()

        days = int(input("Количество дней аренды: "))
        end_date = start_date + timedelta(days=days)

        self._service.rent_vehicle(customer_id, vehicle_id, start_date, end_date)

    def _return_vehicle(self):
        rental_id = input("\nID аренды: ")

        return_str = input("Дата возврата (ГГГГ-ММ-ДД) или Enter для сегодня: ").strip()
        return_date = date.fromisoformat(return_str) if return_str else date.today()

        self._service.return_vehicle(rental_id, return_date)

    def _view_rental_details(self):
        rental_id = input("\nВведите ID аренды: ")
        rental = self._service.find_rental(rental_id)

        if rental:
            rental.display_info()
        else:
            print("Аренда не найдена")

    def _calculate_late_fee(self):
        rental_id = input("\nВведите ID аренды: ")
        self._service.calculate_late_fee(rental_id)

    def _complete_payment(self):
        rental_id = input("\nВведите ID аренды: ")
        rental = self._service.find_rental(rental_id)

        if rental:
            rental.complete_payment()
        else:
            print("Аренда не найдена")

    def _cancel_rental(self):
        rental_id = input("\nВведите ID аренды: ")
        rental = self._service.find_rental(rental_id)

        if rental:
            rental.cancel_rental()
        else:
            print("Аренда не найдена")

    def _filter_by_type(self):
        print("\nВыберите тип транспорта:")
        for i, vehicle_type in enumerate(VehicleType, 1):
            print(f"{i}. {vehicle_type.get_display_name()}")

        choice = int(input("Введите выбор: "))
        vehicle_type = list(VehicleType)[choice - 1]

        self._service.display_available_vehicles(vehicle_type)


def main():
    ui = RentalServiceUI("Rent&Go")
    ui.run()


if __name__ == "__main__":
    main()