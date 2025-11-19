from enum import Enum
from datetime import datetime, date
from decimal import Decimal


# Перечисление категорий меню
class MenuCategory(Enum):
    APPETIZER = "Appetizer"
    MAIN_COURSE = "Main Course"
    DESSERT = "Dessert"
    BEVERAGE = "Beverage"
    SIDE_DISH = "Side Dish"
    SALAD = "Salad"
    SOUP = "Soup"

    def __init__(self, display_name):
        self._display_name = display_name

    def get_display_name(self):
        return self._display_name


# Перечисление статусов заказа
class OrderStatus(Enum):
    PENDING = 1
    CONFIRMED = 2
    PREPARING = 3
    READY = 4
    SERVED = 5
    COMPLETED = 6
    CANCELLED = 7


# Перечисление статусов стола
class TableStatus(Enum):
    AVAILABLE = 1
    OCCUPIED = 2
    RESERVED = 3
    CLEANING = 4


# Перечисление методов оплаты
class PaymentMethod(Enum):
    CASH = 1
    CREDIT_CARD = 2
    DEBIT_CARD = 3
    MOBILE_PAYMENT = 4


# Класс элемента меню
class MenuItem:
    _item_counter = 1

    def __init__(self, name, price, category, description="", preparation_time=15):
        self._item_id = f"ITM{MenuItem._item_counter}"
        MenuItem._item_counter += 1
        self._name = name
        self._price = Decimal(str(price))
        self._category = category
        self._description = description
        self._is_available = True
        self._preparation_time = preparation_time  # в минутах
        self._popularity_count = 0
        self._ingredients = []

    # Геттеры
    def get_item_id(self):
        return self._item_id

    def get_name(self):
        return self._name

    def get_price(self):
        return float(self._price)

    def get_category(self):
        return self._category

    def get_description(self):
        return self._description

    def is_available(self):
        return self._is_available

    def get_preparation_time(self):
        return self._preparation_time

    def get_popularity_count(self):
        return self._popularity_count

    def get_ingredients(self):
        return self._ingredients

    # Сеттеры
    def set_name(self, name):
        self._name = name

    def set_price(self, price):
        self._price = Decimal(str(price))

    def set_available(self, available):
        self._is_available = available

    def set_description(self, description):
        self._description = description

    def add_ingredient(self, ingredient):
        if ingredient not in self._ingredients:
            self._ingredients.append(ingredient)

    # Метод увеличения счетчика популярности
    def increment_popularity(self):
        self._popularity_count += 1

    # Метод отображения информации о позиции меню
    def display_info(self):
        print("\n=== Menu Item Information ===")
        print(f"Item ID: {self._item_id}")
        print(f"Name: {self._name}")
        print(f"Category: {self._category.get_display_name()}")
        print(f"Price: ${self._price:.2f}")
        print(f"Available: {'Yes' if self._is_available else 'No'}")
        print(f"Preparation Time: {self._preparation_time} minutes")
        print(f"Times Ordered: {self._popularity_count}")

        if self._description:
            print(f"Description: {self._description}")

        if self._ingredients:
            print(f"Ingredients: {', '.join(self._ingredients)}")

        print("---")

    # Метод краткого отображения позиции меню
    def display_short(self):
        status = "✓" if self._is_available else "✗"
        print(f"[{status}] {self._item_id} | {self._name:30} | {self._category.name:12} | "
              f"${self._price:>8.2f} | {self._preparation_time:>3} min")


# Класс элемента заказа
class OrderItem:
    def __init__(self, menu_item, quantity=1, special_instructions=""):
        self._menu_item = menu_item
        self._quantity = quantity
        self._special_instructions = special_instructions
        self._subtotal = menu_item.get_price() * quantity

    # Геттеры
    def get_menu_item(self):
        return self._menu_item

    def get_quantity(self):
        return self._quantity

    def get_special_instructions(self):
        return self._special_instructions

    def get_subtotal(self):
        return self._subtotal

    # Сеттеры
    def set_quantity(self, quantity):
        self._quantity = quantity
        self._subtotal = self._menu_item.get_price() * quantity

    def set_special_instructions(self, instructions):
        self._special_instructions = instructions

    # Метод увеличения количества
    def increase_quantity(self, amount=1):
        self._quantity += amount
        self._subtotal = self._menu_item.get_price() * self._quantity

    # Метод отображения элемента заказа
    def display(self):
        print(f"  {self._menu_item.get_name()} x{self._quantity} - "
              f"${self._menu_item.get_price():.2f} each = ${self._subtotal:.2f}")
        if self._special_instructions:
            print(f"    Note: {self._special_instructions}")


# Класс заказа
class Order:
    _order_counter = 1000

    def __init__(self, table_number, waiter_name=""):
        self._order_number = f"ORD{Order._order_counter}"
        Order._order_counter += 1
        self._table_number = table_number
        self._items = []
        self._order_time = datetime.now()
        self._status = OrderStatus.PENDING
        self._waiter_name = waiter_name
        self._special_requests = ""
        self._subtotal = Decimal('0.00')
        self._tax_rate = Decimal('0.10')  # 10% налог
        self._service_charge_rate = Decimal('0.15')  # 15% за обслуживание
        self._discount = Decimal('0.00')

    # Геттеры
    def get_order_number(self):
        return self._order_number

    def get_table_number(self):
        return self._table_number

    def get_items(self):
        return self._items

    def get_order_time(self):
        return self._order_time

    def get_status(self):
        return self._status

    def get_waiter_name(self):
        return self._waiter_name

    def get_special_requests(self):
        return self._special_requests

    def get_discount(self):
        return float(self._discount)

    # Сеттеры
    def set_status(self, status):
        self._status = status

    def set_waiter_name(self, waiter_name):
        self._waiter_name = waiter_name

    def set_special_requests(self, requests):
        self._special_requests = requests

    def set_discount(self, discount):
        self._discount = Decimal(str(discount))

    # Метод добавления элемента в заказ
    def add_item(self, menu_item, quantity=1, special_instructions=""):
        if not menu_item.is_available():
            print(f"Error: {menu_item.get_name()} is not available")
            return False

        # Проверка, есть ли уже такой элемент в заказе
        for order_item in self._items:
            if order_item.get_menu_item().get_item_id() == menu_item.get_item_id():
                order_item.increase_quantity(quantity)
                self._recalculate_subtotal()
                print(f"\n✓ Updated quantity for {menu_item.get_name()}")
                print(f"New quantity: {order_item.get_quantity()}")
                return True

        # Добавление нового элемента
        order_item = OrderItem(menu_item, quantity, special_instructions)
        self._items.append(order_item)
        menu_item.increment_popularity()
        self._recalculate_subtotal()

        print(f"\n✓ Added to order: {menu_item.get_name()} x{quantity}")
        return True

    # Метод удаления элемента из заказа
    def remove_item(self, item_id):
        for i, order_item in enumerate(self._items):
            if order_item.get_menu_item().get_item_id() == item_id:
                removed = self._items.pop(i)
                self._recalculate_subtotal()
                print(f"\n✓ Removed from order: {removed.get_menu_item().get_name()}")
                return True

        print(f"Error: Item {item_id} not found in order")
        return False

    # Метод обновления количества элемента
    def update_item_quantity(self, item_id, new_quantity):
        if new_quantity <= 0:
            return self.remove_item(item_id)

        for order_item in self._items:
            if order_item.get_menu_item().get_item_id() == item_id:
                order_item.set_quantity(new_quantity)
                self._recalculate_subtotal()
                print(f"\n✓ Updated quantity to {new_quantity}")
                return True

        print(f"Error: Item {item_id} not found in order")
        return False

    # Метод пересчета промежуточной суммы
    def _recalculate_subtotal(self):
        self._subtotal = sum(Decimal(str(item.get_subtotal())) for item in self._items)

    # Метод расчета налога
    def calculate_tax(self):
        return float(self._subtotal * self._tax_rate)

    # Метод расчета платы за обслуживание
    def calculate_service_charge(self):
        return float(self._subtotal * self._service_charge_rate)

    # Метод расчета общей суммы
    def calculate_total(self):
        tax = self._subtotal * self._tax_rate
        service = self._subtotal * self._service_charge_rate
        total = self._subtotal + tax + service - self._discount
        return float(total)

    # Метод расчета времени приготовления
    def estimate_preparation_time(self):
        if not self._items:
            return 0
        return max(item.get_menu_item().get_preparation_time() for item in self._items)

    # Метод проверки, пуст ли заказ
    def is_empty(self):
        return len(self._items) == 0

    # Метод подтверждения заказа
    def confirm(self):
        if self.is_empty():
            print("Error: Cannot confirm empty order")
            return False

        self._status = OrderStatus.CONFIRMED
        print(f"\n✓ Order {self._order_number} confirmed")
        print(f"Estimated preparation time: {self.estimate_preparation_time()} minutes")
        return True

    # Метод отображения информации о заказе
    def display_info(self):
        print("\n=== Order Information ===")
        print(f"Order Number: {self._order_number}")
        print(f"Table Number: {self._table_number}")
        print(f"Status: {self._status.name}")
        print(f"Order Time: {self._order_time.strftime('%Y-%m-%d %H:%M:%S')}")

        if self._waiter_name:
            print(f"Waiter: {self._waiter_name}")

        if self.is_empty():
            print("\nNo items in order")
        else:
            print(f"\nItems ({len(self._items)}):")
            for item in self._items:
                item.display()

        if self._special_requests:
            print(f"\nSpecial Requests: {self._special_requests}")

        print("\n--- Bill ---")
        print(f"Subtotal: ${float(self._subtotal):.2f}")
        print(f"Tax ({self._tax_rate * 100:.0f}%): ${self.calculate_tax():.2f}")
        print(f"Service Charge ({self._service_charge_rate * 100:.0f}%): ${self.calculate_service_charge():.2f}")

        if self._discount > 0:
            print(f"Discount: -${float(self._discount):.2f}")

        print(f"Total: ${self.calculate_total():.2f}")
        print("---")

    # Метод краткого отображения заказа
    def display_short(self):
        status_symbol = {
            OrderStatus.PENDING: "⏳",
            OrderStatus.CONFIRMED: "✓",
            OrderStatus.PREPARING: "🔥",
            OrderStatus.READY: "✔",
            OrderStatus.SERVED: "🍽️",
            OrderStatus.COMPLETED: "✅",
            OrderStatus.CANCELLED: "✗"
        }
        symbol = status_symbol.get(self._status, "?")

        print(f"[{symbol}] {self._order_number} | Table {self._table_number:>2} | "
              f"{len(self._items):>2} items | ${self.calculate_total():>8.2f} | {self._status.name}")


# Класс стола
class Table:
    def __init__(self, table_number, capacity, location=""):
        self._table_number = table_number
        self._capacity = capacity
        self._location = location
        self._status = TableStatus.AVAILABLE
        self._current_order = None
        self._reservation_name = ""
        self._seated_at = None

    # Геттеры
    def get_table_number(self):
        return self._table_number

    def get_capacity(self):
        return self._capacity

    def get_location(self):
        return self._location

    def get_status(self):
        return self._status

    def get_current_order(self):
        return self._current_order

    def get_reservation_name(self):
        return self._reservation_name

    def get_seated_at(self):
        return self._seated_at

    # Метод проверки доступности
    def is_available(self):
        return self._status == TableStatus.AVAILABLE

    # Метод проверки занятости
    def is_occupied(self):
        return self._status == TableStatus.OCCUPIED

    # Метод занятия стола
    def occupy(self, party_size, order=None):
        if not self.is_available():
            print(f"Error: Table {self._table_number} is not available")
            return False

        if party_size > self._capacity:
            print(f"Error: Party size ({party_size}) exceeds table capacity ({self._capacity})")
            return False

        self._status = TableStatus.OCCUPIED
        self._current_order = order
        self._seated_at = datetime.now()

        print(f"\n✓ Table {self._table_number} occupied")
        print(f"Party size: {party_size}/{self._capacity}")
        return True

    # Метод резервирования стола
    def reserve(self, reservation_name):
        if not self.is_available():
            print(f"Error: Table {self._table_number} is not available for reservation")
            return False

        self._status = TableStatus.RESERVED
        self._reservation_name = reservation_name

        print(f"\n✓ Table {self._table_number} reserved for {reservation_name}")
        return True

    # Метод освобождения стола
    def release(self):
        self._status = TableStatus.CLEANING
        self._current_order = None
        self._reservation_name = ""
        self._seated_at = None

        print(f"\n✓ Table {self._table_number} released for cleaning")
        return True

    # Метод завершения уборки
    def finish_cleaning(self):
        if self._status != TableStatus.CLEANING:
            print("Error: Table is not in cleaning state")
            return False

        self._status = TableStatus.AVAILABLE
        print(f"\n✓ Table {self._table_number} is now available")
        return True

    # Метод привязки заказа к столу
    def assign_order(self, order):
        if not self.is_occupied():
            print("Error: Table must be occupied to assign order")
            return False

        self._current_order = order
        print(f"\n✓ Order {order.get_order_number()} assigned to table {self._table_number}")
        return True

    # Метод расчета времени занятости
    def get_occupancy_duration(self):
        if self._seated_at:
            return datetime.now() - self._seated_at
        return None

    # Метод отображения информации о столе
    def display_info(self):
        print("\n=== Table Information ===")
        print(f"Table Number: {self._table_number}")
        print(f"Capacity: {self._capacity} people")
        print(f"Location: {self._location if self._location else 'N/A'}")
        print(f"Status: {self._status.name}")

        if self._status == TableStatus.RESERVED:
            print(f"Reserved for: {self._reservation_name}")

        if self._status == TableStatus.OCCUPIED:
            if self._seated_at:
                duration = self.get_occupancy_duration()
                minutes = int(duration.total_seconds() / 60)
                print(f"Occupied for: {minutes} minutes")

            if self._current_order:
                print(f"Current Order: {self._current_order.get_order_number()}")

        print("---")

    # Метод краткого отображения стола
    def display_short(self):
        status_symbol = {
            TableStatus.AVAILABLE: "✓",
            TableStatus.OCCUPIED: "👥",
            TableStatus.RESERVED: "🔒",
            TableStatus.CLEANING: "🧹"
        }
        symbol = status_symbol.get(self._status, "?")

        extra_info = ""
        if self._status == TableStatus.OCCUPIED and self._current_order:
            extra_info = f" | Order: {self._current_order.get_order_number()}"
        elif self._status == TableStatus.RESERVED:
            extra_info = f" | Reserved: {self._reservation_name}"

        print(f"[{symbol}] Table {self._table_number:>2} | Capacity: {self._capacity:>2} | "
              f"{self._status.name:10}{extra_info}")


# Класс ресторана
class Restaurant:
    def __init__(self, restaurant_name, address=""):
        self._restaurant_name = restaurant_name
        self._address = address
        self._menu_items = []
        self._tables = []
        self._orders = []
        self._daily_revenue = Decimal('0.00')

    # Метод добавления позиции меню
    def add_menu_item(self, menu_item):
        # Проверка на дубликаты
        for item in self._menu_items:
            if item.get_name().lower() == menu_item.get_name().lower():
                print(f"Warning: Menu item '{menu_item.get_name()}' already exists")
                return False

        self._menu_items.append(menu_item)
        print(f"\n✓ Menu item added: {menu_item.get_name()}")
        return True

    # Метод добавления стола
    def add_table(self, table):
        # Проверка на дубликаты номеров столов
        for t in self._tables:
            if t.get_table_number() == table.get_table_number():
                print(f"Error: Table {table.get_table_number()} already exists")
                return False

        self._tables.append(table)
        print(f"\n✓ Table {table.get_table_number()} added (Capacity: {table.get_capacity()})")
        return True

    # Метод поиска позиции меню по ID
    def find_menu_item(self, item_id):
        for item in self._menu_items:
            if item.get_item_id() == item_id:
                return item
        return None

    # Метод поиска стола по номеру
    def find_table(self, table_number):
        for table in self._tables:
            if table.get_table_number() == table_number:
                return table
        return None

    # Метод поиска заказа по номеру
    def find_order(self, order_number):
        for order in self._orders:
            if order.get_order_number() == order_number:
                return order
        return None

    # Метод создания заказа
    def place_order(self, table_number, waiter_name=""):
        table = self.find_table(table_number)

        if not table:
            print(f"Error: Table {table_number} not found")
            return None

        if not table.is_occupied():
            print(f"Error: Table {table_number} is not occupied")
            return None

        order = Order(table_number, waiter_name)
        self._orders.append(order)
        table.assign_order(order)

        print(f"\n✓ Order created: {order.get_order_number()}")
        print(f"Table: {table_number}")
        return order

    # Метод добавления элемента в заказ
    def add_item_to_order(self, order_number, item_id, quantity=1, special_instructions=""):
        order = self.find_order(order_number)
        if not order:
            print(f"Error: Order {order_number} not found")
            return False

        menu_item = self.find_menu_item(item_id)
        if not menu_item:
            print(f"Error: Menu item {item_id} not found")
            return False

        return order.add_item(menu_item, quantity, special_instructions)

    # Метод расчета счета
    def calculate_bill(self, order_number):
        order = self.find_order(order_number)
        if not order:
            print(f"Error: Order {order_number} not found")
            return None

        order.display_info()
        return order.calculate_total()

    # Метод закрытия стола (оплата и освобождение)
    def close_table(self, table_number, payment_method, tip_amount=0.0):
        table = self.find_table(table_number)
        if not table:
            print(f"Error: Table {table_number} not found")
            return False

        if not table.is_occupied():
            print(f"Error: Table {table_number} is not occupied")
            return False

        order = table.get_current_order()
        if not order:
            print("Error: No order found for this table")
            return False

        # Расчет финальной суммы с чаевыми
        total = order.calculate_total()
        final_amount = total + tip_amount

        # Обновление статуса заказа
        order.set_status(OrderStatus.COMPLETED)

        # Добавление к дневной выручке
        self._daily_revenue += Decimal(str(final_amount))

        # Освобождение стола
        table.release()

        print("\n" + "=" * 50)
        print("RECEIPT".center(50))
        print("=" * 50)
        print(f"Restaurant: {self._restaurant_name}")
        print(f"Table: {table_number}")
        print(f"Order: {order.get_order_number()}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)

        order.display_info()

        if tip_amount > 0:
            print(f"Tip: ${tip_amount:.2f}")
            print(f"Final Total: ${final_amount:.2f}")

        print(f"\nPayment Method: {payment_method.name}")
        print("=" * 50)
        print("Thank you for dining with us!".center(50))
        print("=" * 50)

        return True

    # Метод получения доступных столов
    def get_available_tables(self, min_capacity=1):
        return [t for t in self._tables
                if t.is_available() and t.get_capacity() >= min_capacity]

    # Метод получения занятых столов
    def get_occupied_tables(self):
        return [t for t in self._tables if t.is_occupied()]

    # Метод получения меню по категории
    def get_menu_by_category(self, category):
        return [item for item in self._menu_items if item.get_category() == category]

    # Метод получения доступных позиций меню
    def get_available_menu_items(self):
        return [item for item in self._menu_items if item.is_available()]

    # Метод получения активных заказов
    def get_active_orders(self):
        return [o for o in self._orders
                if o.get_status() not in [OrderStatus.COMPLETED, OrderStatus.CANCELLED]]

    # Метод получения популярных блюд
    def get_popular_items(self, limit=5):
        sorted_items = sorted(self._menu_items,
                              key=lambda x: x.get_popularity_count(),
                              reverse=True)
        return sorted_items[:limit]

    # Метод отображения полного меню
    def display_full_menu(self):
        if not self._menu_items:
            print("\nMenu is empty")
            return

        print(f"\n{'=' * 60}")
        print(f"{self._restaurant_name} - Menu".center(60))
        print(f"{'=' * 60}")

        for category in MenuCategory:
            items = self.get_menu_by_category(category)
            if items:
                print(f"\n--- {category.get_display_name()} ---")
                for item in items:
                    item.display_short()

    # Метод отображения всех столов
    def display_all_tables(self):
        if not self._tables:
            print("\nNo tables in restaurant")
            return

        print(f"\n=== {self._restaurant_name} - Tables ===")
        for table in self._tables:
            table.display_short()
        print(f"\nTotal tables: {len(self._tables)}")

    # Метод отображения активных заказов
    def display_active_orders(self):
        orders = self.get_active_orders()

        if not orders:
            print("\nNo active orders")
            return

        print("\n=== Active Orders ===")
        for order in orders:
            order.display_short()
        print(f"\nTotal active orders: {len(orders)}")

    # Метод отображения статистики ресторана
    def display_statistics(self):
        total_tables = len(self._tables)
        occupied_tables = len(self.get_occupied_tables())
        available_tables = len(self.get_available_tables())
        total_menu_items = len(self._menu_items)
        available_menu_items = len(self.get_available_menu_items())
        total_orders = len(self._orders)
        active_orders = len(self.get_active_orders())
        completed_orders = sum(1 for o in self._orders if o.get_status() == OrderStatus.COMPLETED)

        print(f"\n=== {self._restaurant_name} Statistics ===")
        if self._address:
            print(f"Location: {self._address}")

        print(f"\nTables:")
        print(f"  Total: {total_tables}")
        print(f"  Occupied: {occupied_tables}")
        print(f"  Available: {available_tables}")

        if total_tables > 0:
            occupancy_rate = (occupied_tables / total_tables) * 100
            print(f"  Occupancy Rate: {occupancy_rate:.1f}%")

        print(f"\nMenu:")
        print(f"  Total Items: {total_menu_items}")
        print(f"  Available Items: {available_menu_items}")

        print(f"\nOrders:")
        print(f"  Total: {total_orders}")
        print(f"  Active: {active_orders}")
        print(f"  Completed: {completed_orders}")

        print(f"\nRevenue:")
        print(f"  Today's Revenue: ${float(self._daily_revenue):.2f}")

        if completed_orders > 0:
            avg_order = float(self._daily_revenue) / completed_orders
            print(f"  Average Order Value: ${avg_order:.2f}")

        # Популярные блюда
        popular = self.get_popular_items(3)
        if popular and popular[0].get_popularity_count() > 0:
            print(f"\nTop 3 Popular Items:")
            for i, item in enumerate(popular, 1):
                print(f"  {i}. {item.get_name()} - Ordered {item.get_popularity_count()} times")


# Класс пользовательского интерфейса
class RestaurantUI:
    def __init__(self, restaurant_name, address=""):
        self._restaurant = Restaurant(restaurant_name, address)
        self._initialize_sample_data()

    # Инициализация примерных данных
    def _initialize_sample_data(self):
        # Добавление позиций меню
        appetizers = [
            MenuItem("Caesar Salad", 12.99, MenuCategory.SALAD, "Fresh romaine with caesar dressing"),
            MenuItem("Garlic Bread", 6.99, MenuCategory.APPETIZER, "Toasted bread with garlic butter"),
            MenuItem("Chicken Wings", 14.99, MenuCategory.APPETIZER, "Spicy buffalo wings")
        ]

        main_courses = [
            MenuItem("Grilled Salmon", 28.99, MenuCategory.MAIN_COURSE, "Atlantic salmon with vegetables", 25),
            MenuItem("Beef Steak", 34.99, MenuCategory.MAIN_COURSE, "Prime ribeye steak", 30),
            MenuItem("Pasta Carbonara", 18.99, MenuCategory.MAIN_COURSE, "Classic Italian pasta", 20)
        ]

        desserts = [
            MenuItem("Chocolate Cake", 8.99, MenuCategory.DESSERT, "Rich chocolate layer cake"),
            MenuItem("Tiramisu", 9.99, MenuCategory.DESSERT, "Traditional Italian dessert")
        ]

        beverages = [
            MenuItem("Coca-Cola", 3.99, MenuCategory.BEVERAGE, "Soft drink"),
            MenuItem("Fresh Orange Juice", 5.99, MenuCategory.BEVERAGE, "Freshly squeezed"),
            MenuItem("Coffee", 4.99, MenuCategory.BEVERAGE, "Espresso or Americano")
        ]

        for item in appetizers + main_courses + desserts + beverages:
            self._restaurant.add_menu_item(item)

        # Добавление столов
        for i in range(1, 11):
            capacity = 2 if i <= 4 else (4 if i <= 8 else 6)
            location = "Window" if i % 3 == 0 else "Main Hall"
            self._restaurant.add_table(Table(i, capacity, location))

    def run(self):
        print("╔════════════════════════════════════════╗")
        print("║  Restaurant Management System          ║")
        print("╚════════════════════════════════════════╝\n")

        while True:
            try:
                self._display_main_menu()
                choice = int(input())

                if choice == 20:
                    print("\nThank you for using Restaurant Management System!")
                    break

                self._handle_menu_choice(choice)

            except Exception:
                print("\nError: Invalid input. Please try again.")

    # Отображение главного меню
    def _display_main_menu(self):
        print("\n=== Main Menu ===")
        print("1. View full menu")
        print("2. Add menu item")
        print("3. Update menu item availability")
        print("4. View all tables")
        print("5. View available tables")
        print("6. Seat guests (occupy table)")
        print("7. Reserve table")
        print("8. Create order")
        print("9. Add item to order")
        print("10. View order details")
        print("11. Update order status")
        print("12. View active orders")
        print("13. Calculate bill")
        print("14. Close table (complete payment)")
        print("15. Release table")
        print("16. View popular items")
        print("17. Search menu by category")
        print("18. View table status")
        print("19. View statistics")
        print("20. Exit")
        print("Enter choice (1-20): ", end='')

    # Обработка выбора меню
    def _handle_menu_choice(self, choice):
        actions = {
            1: self._restaurant.display_full_menu,
            2: self._add_menu_item,
            3: self._update_availability,
            4: self._restaurant.display_all_tables,
            5: self._view_available_tables,
            6: self._seat_guests,
            7: self._reserve_table,
            8: self._create_order,
            9: self._add_item_to_order,
            10: self._view_order_details,
            11: self._update_order_status,
            12: self._restaurant.display_active_orders,
            13: self._calculate_bill,
            14: self._close_table,
            15: self._release_table,
            16: self._view_popular_items,
            17: self._search_by_category,
            18: self._view_table_status,
            19: self._restaurant.display_statistics
        }
        if choice in actions:
            actions[choice]()
        else:
            print("Invalid choice. Please try again.")

    def _add_menu_item(self):
        name = input("\nEnter item name: ")
        price = float(input("Enter price: $"))

        print("\nSelect category:")
        for i, cat in enumerate(MenuCategory, 1):
            print(f"{i}. {cat.get_display_name()}")
        cat_choice = int(input("Enter choice: "))
        category = list(MenuCategory)[cat_choice - 1]

        description = input("Enter description (optional): ")
        prep_time = int(input("Enter preparation time in minutes (default 15): ") or "15")

        item = MenuItem(name, price, category, description, prep_time)
        self._restaurant.add_menu_item(item)

    def _update_availability(self):
        item_id = input("\nEnter menu item ID: ")
        menu_item = self._restaurant.find_menu_item(item_id)

        if not menu_item:
            print("Error: Menu item not found")
            return

        available = input(f"Set available? (current: {menu_item.is_available()}) (y/n): ").lower().startswith('y')
        menu_item.set_available(available)
        print(f"\n✓ {menu_item.get_name()} is now {'available' if available else 'unavailable'}")

    def _view_available_tables(self):
        min_capacity = int(input("\nEnter minimum capacity needed: "))
        tables = self._restaurant.get_available_tables(min_capacity)

        if not tables:
            print(f"\nNo available tables with capacity >= {min_capacity}")
            return

        print(f"\n=== Available Tables (Capacity >= {min_capacity}) ===")
        for table in tables:
            table.display_short()

    def _seat_guests(self):
        table_number = int(input("\nEnter table number: "))
        table = self._restaurant.find_table(table_number)

        if not table:
            print("Error: Table not found")
            return

        party_size = int(input("Enter party size: "))
        table.occupy(party_size)

    def _reserve_table(self):
        table_number = int(input("\nEnter table number: "))
        table = self._restaurant.find_table(table_number)

        if not table:
            print("Error: Table not found")
            return

        name = input("Enter reservation name: ")
        table.reserve(name)

    def _create_order(self):
        table_number = int(input("\nEnter table number: "))
        waiter_name = input("Enter waiter name (optional): ")
        self._restaurant.place_order(table_number, waiter_name)

    def _add_item_to_order(self):
        order_number = input("\nEnter order number: ")
        item_id = input("Enter menu item ID: ")
        quantity = int(input("Enter quantity: "))
        instructions = input("Enter special instructions (optional): ")

        self._restaurant.add_item_to_order(order_number, item_id, quantity, instructions)

    def _view_order_details(self):
        order_number = input("\nEnter order number: ")
        order = self._restaurant.find_order(order_number)

        if order:
            order.display_info()
        else:
            print("Error: Order not found")

    def _update_order_status(self):
        order_number = input("\nEnter order number: ")
        order = self._restaurant.find_order(order_number)

        if not order:
            print("Error: Order not found")
            return

        print(f"\nCurrent status: {order.get_status().name}")
        print("\nSelect new status:")
        for i, status in enumerate(OrderStatus, 1):
            print(f"{i}. {status.name}")

        status_choice = int(input("Enter choice: "))
        new_status = list(OrderStatus)[status_choice - 1]

        order.set_status(new_status)
        print(f"\n✓ Order status updated to {new_status.name}")

    def _calculate_bill(self):
        order_number = input("\nEnter order number: ")
        self._restaurant.calculate_bill(order_number)

    def _close_table(self):
        table_number = int(input("\nEnter table number: "))

        print("\nSelect payment method:")
        for i, method in enumerate(PaymentMethod, 1):
            print(f"{i}. {method.name}")

        payment_choice = int(input("Enter choice: "))
        payment_method = list(PaymentMethod)[payment_choice - 1]

        tip = float(input("Enter tip amount: $"))

        self._restaurant.close_table(table_number, payment_method, tip)

    def _release_table(self):
        table_number = int(input("\nEnter table number: "))
        table = self._restaurant.find_table(table_number)

        if table:
            if table.get_status() == TableStatus.CLEANING:
                table.finish_cleaning()
            else:
                table.release()
        else:
            print("Error: Table not found")

    def _view_popular_items(self):
        limit = int(input("\nEnter number of top items to show: "))
        popular = self._restaurant.get_popular_items(limit)

        if not popular or popular[0].get_popularity_count() == 0:
            print("\nNo order data available yet")
            return

        print(f"\n=== Top {limit} Popular Items ===")
        for i, item in enumerate(popular, 1):
            print(f"{i}. {item.get_name()} - Ordered {item.get_popularity_count()} times (${item.get_price():.2f})")

    def _search_by_category(self):
        print("\nSelect category:")
        for i, cat in enumerate(MenuCategory, 1):
            print(f"{i}. {cat.get_display_name()}")

        cat_choice = int(input("Enter choice: "))
        category = list(MenuCategory)[cat_choice - 1]

        items = self._restaurant.get_menu_by_category(category)

        if not items:
            print(f"\nNo items in {category.get_display_name()}")
            return

        print(f"\n=== {category.get_display_name()} ===")
        for item in items:
            item.display_short()

    def _view_table_status(self):
        table_number = int(input("\nEnter table number: "))
        table = self._restaurant.find_table(table_number)

        if table:
            table.display_info()
        else:
            print("Error: Table not found")


def main():
    ui = RestaurantUI("La Bella Vista", "123 Main Street, New York")
    ui.run()


if __name__ == "__main__":
    main()