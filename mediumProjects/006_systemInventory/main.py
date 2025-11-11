from enum import Enum
from datetime import datetime, date
from decimal import Decimal


# Перечисление категорий товаров
class Category(Enum):
    ELECTRONICS = "Electronics"
    CLOTHING = "Clothing"
    FOOD = "Food"
    BOOKS = "Books"
    FURNITURE = "Furniture"
    TOYS = "Toys"
    SPORTS = "Sports"
    BEAUTY = "Beauty"
    AUTOMOTIVE = "Automotive"
    OTHER = "Other"

    def __init__(self, display_name):
        self._display_name = display_name

    def get_display_name(self):
        return self._display_name


# Перечисление статусов заказа поставки
class OrderStatus(Enum):
    PENDING = 1
    APPROVED = 2
    SHIPPED = 3
    DELIVERED = 4
    CANCELLED = 5


# Перечисление приоритета товаров
class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


# Класс товара
class Product:
    _product_counter = 1000

    def __init__(self, name, category, quantity, price, supplier="", min_stock_level=10):
        self._product_id = f"PRD{Product._product_counter}"
        Product._product_counter += 1
        self._name = name
        self._category = category
        self._quantity = quantity
        self._price = Decimal(str(price))
        self._supplier = supplier
        self._min_stock_level = min_stock_level
        self._creation_date = date.today()
        self._last_updated = datetime.now()
        self._reorder_point = min_stock_level * 2
        self._description = ""

    # Геттеры
    def get_product_id(self):
        return self._product_id

    def get_name(self):
        return self._name

    def get_category(self):
        return self._category

    def get_quantity(self):
        return self._quantity

    def get_price(self):
        return float(self._price)

    def get_supplier(self):
        return self._supplier

    def get_min_stock_level(self):
        return self._min_stock_level

    def get_reorder_point(self):
        return self._reorder_point

    def get_description(self):
        return self._description

    def get_creation_date(self):
        return self._creation_date

    def get_last_updated(self):
        return self._last_updated

    # Сеттеры
    def set_name(self, name):
        self._name = name
        self._update_timestamp()

    def set_price(self, price):
        self._price = Decimal(str(price))
        self._update_timestamp()

    def set_supplier(self, supplier):
        self._supplier = supplier
        self._update_timestamp()

    def set_min_stock_level(self, level):
        self._min_stock_level = level
        self._reorder_point = level * 2
        self._update_timestamp()

    def set_description(self, description):
        self._description = description
        self._update_timestamp()

    # Метод обновления временной метки
    def _update_timestamp(self):
        self._last_updated = datetime.now()

    # Метод добавления товара на склад
    def add_stock(self, quantity):
        if quantity <= 0:
            print("Error: Quantity must be positive")
            return False

        self._quantity += quantity
        self._update_timestamp()
        print(f"\n✓ Stock added: {quantity} units")
        print(f"New quantity: {self._quantity}")
        return True

    # Метод удаления товара со склада
    def remove_stock(self, quantity):
        if quantity <= 0:
            print("Error: Quantity must be positive")
            return False

        if quantity > self._quantity:
            print(f"Error: Insufficient stock (Available: {self._quantity})")
            return False

        self._quantity -= quantity
        self._update_timestamp()
        print(f"\n✓ Stock removed: {quantity} units")
        print(f"Remaining quantity: {self._quantity}")

        # Предупреждение о низком запасе
        if self.is_low_stock():
            print(f"⚠️  WARNING: Stock is below minimum level ({self._min_stock_level})")

        return True

    # Метод проверки низкого запаса
    def is_low_stock(self):
        return self._quantity <= self._min_stock_level

    # Метод проверки необходимости переоформления заказа
    def needs_reorder(self):
        return self._quantity <= self._reorder_point

    # Метод получения приоритета пополнения
    def get_reorder_priority(self):
        if self._quantity == 0:
            return Priority.CRITICAL
        elif self._quantity <= self._min_stock_level:
            return Priority.HIGH
        elif self._quantity <= self._reorder_point:
            return Priority.MEDIUM
        else:
            return Priority.LOW

    # Метод расчета стоимости товаров на складе
    def calculate_stock_value(self):
        return float(self._price * Decimal(str(self._quantity)))

    # Метод отображения информации о товаре
    def display_info(self):
        print("\n=== Product Information ===")
        print(f"Product ID: {self._product_id}")
        print(f"Name: {self._name}")
        print(f"Category: {self._category.get_display_name()}")
        print(f"Quantity: {self._quantity}")
        print(f"Price: ${self._price:.2f}")
        print(f"Stock Value: ${self.calculate_stock_value():.2f}")
        print(f"Supplier: {self._supplier if self._supplier else 'N/A'}")
        print(f"Minimum Stock Level: {self._min_stock_level}")
        print(f"Reorder Point: {self._reorder_point}")
        print(f"Priority: {self.get_reorder_priority().name}")

        if self._description:
            print(f"Description: {self._description}")

        print(f"Created: {self._creation_date}")
        print(f"Last Updated: {self._last_updated.strftime('%Y-%m-%d %H:%M:%S')}")

        if self.is_low_stock():
            print("⚠️  Status: LOW STOCK")
        elif self.needs_reorder():
            print("⚠️  Status: REORDER NEEDED")
        else:
            print("✓ Status: OK")

        print("---")

    # Метод краткого отображения товара
    def display_short(self):
        status = "✓" if not self.is_low_stock() else "⚠️"
        print(f"[{status}] {self._product_id} | {self._name:30} | {self._category.name:12} | "
              f"Qty: {self._quantity:>5} | ${self._price:>8.2f} | Value: ${self.calculate_stock_value():>10.2f}")


# Класс заказа поставки
class SupplyOrder:
    _order_counter = 5000

    def __init__(self, product, quantity, supplier=""):
        self._order_id = f"ORD{SupplyOrder._order_counter}"
        SupplyOrder._order_counter += 1
        self._product = product
        self._quantity = quantity
        self._supplier = supplier if supplier else product.get_supplier()
        self._order_date = datetime.now()
        self._expected_delivery = None
        self._actual_delivery = None
        self._status = OrderStatus.PENDING
        self._unit_price = product.get_price()
        self._total_cost = Decimal(str(self._unit_price)) * Decimal(str(quantity))
        self._notes = ""

    # Геттеры
    def get_order_id(self):
        return self._order_id

    def get_product(self):
        return self._product

    def get_quantity(self):
        return self._quantity

    def get_supplier(self):
        return self._supplier

    def get_order_date(self):
        return self._order_date

    def get_expected_delivery(self):
        return self._expected_delivery

    def get_actual_delivery(self):
        return self._actual_delivery

    def get_status(self):
        return self._status

    def get_total_cost(self):
        return float(self._total_cost)

    def get_notes(self):
        return self._notes

    # Сеттеры
    def set_expected_delivery(self, delivery_date):
        self._expected_delivery = delivery_date

    def set_notes(self, notes):
        self._notes = notes

    def set_status(self, status):
        self._status = status

    # Метод одобрения заказа
    def approve(self):
        if self._status != OrderStatus.PENDING:
            print("Error: Order can only be approved if it's pending")
            return False

        self._status = OrderStatus.APPROVED
        print(f"\n✓ Order {self._order_id} approved")
        return True

    # Метод отправки заказа
    def ship(self):
        if self._status != OrderStatus.APPROVED:
            print("Error: Order must be approved before shipping")
            return False

        self._status = OrderStatus.SHIPPED
        print(f"\n✓ Order {self._order_id} shipped")
        return True

    # Метод доставки заказа
    def deliver(self):
        if self._status != OrderStatus.SHIPPED:
            print("Error: Order must be shipped before delivery")
            return False

        self._status = OrderStatus.DELIVERED
        self._actual_delivery = datetime.now()

        # Автоматическое пополнение склада
        self._product.add_stock(self._quantity)

        print(f"\n✓ Order {self._order_id} delivered")
        print(f"Added {self._quantity} units of {self._product.get_name()} to inventory")
        return True

    # Метод отмены заказа
    def cancel(self):
        if self._status in [OrderStatus.DELIVERED, OrderStatus.CANCELLED]:
            print("Error: Cannot cancel delivered or already cancelled order")
            return False

        self._status = OrderStatus.CANCELLED
        print(f"\n✓ Order {self._order_id} cancelled")
        return True

    # Метод проверки просрочки
    def is_overdue(self):
        if self._expected_delivery and self._status not in [OrderStatus.DELIVERED, OrderStatus.CANCELLED]:
            return datetime.now().date() > self._expected_delivery
        return False

    # Метод отображения информации о заказе
    def display_info(self):
        print("\n=== Supply Order Information ===")
        print(f"Order ID: {self._order_id}")
        print(f"Product: {self._product.get_name()} ({self._product.get_product_id()})")
        print(f"Quantity: {self._quantity}")
        print(f"Supplier: {self._supplier}")
        print(f"Unit Price: ${self._unit_price:.2f}")
        print(f"Total Cost: ${self._total_cost:.2f}")
        print(f"Status: {self._status.name}")
        print(f"Order Date: {self._order_date.strftime('%Y-%m-%d %H:%M:%S')}")

        if self._expected_delivery:
            print(f"Expected Delivery: {self._expected_delivery}")
            if self.is_overdue():
                print("⚠️  OVERDUE")

        if self._actual_delivery:
            print(f"Actual Delivery: {self._actual_delivery.strftime('%Y-%m-%d %H:%M:%S')}")

        if self._notes:
            print(f"Notes: {self._notes}")

        print("---")

    # Метод краткого отображения заказа
    def display_short(self):
        status_symbol = {
            OrderStatus.PENDING: "⏳",
            OrderStatus.APPROVED: "✓",
            OrderStatus.SHIPPED: "🚚",
            OrderStatus.DELIVERED: "✔",
            OrderStatus.CANCELLED: "✗"
        }
        symbol = status_symbol.get(self._status, "?")
        overdue = " [OVERDUE]" if self.is_overdue() else ""

        print(f"[{symbol}] {self._order_id} | {self._product.get_name():30} | "
              f"Qty: {self._quantity:>5} | ${self._total_cost:>10.2f} | "
              f"{self._status.name}{overdue}")


# Класс склада
class Warehouse:
    def __init__(self, warehouse_name, location=""):
        self._warehouse_name = warehouse_name
        self._location = location
        self._products = []
        self._supply_orders = []

    # Метод добавления товара
    def add_product(self, product):
        # Проверка на дубликаты по названию и категории
        for existing in self._products:
            if (existing.get_name().lower() == product.get_name().lower() and
                    existing.get_category() == product.get_category()):
                print(f"Warning: Similar product already exists: {existing.get_product_id()}")
                response = input("Add anyway? (y/n): ")
                if not response.lower().startswith('y'):
                    return False

        self._products.append(product)
        print(f"\n✓ Product added to warehouse")
        print(f"Product ID: {product.get_product_id()}")
        print(f"Name: {product.get_name()}")
        return True

    # Метод удаления товара
    def remove_product(self, product_id):
        for i, product in enumerate(self._products):
            if product.get_product_id() == product_id:
                removed = self._products.pop(i)
                print(f"\n✓ Product removed: {removed.get_name()}")
                return True

        print(f"Error: Product with ID {product_id} not found")
        return False

    # Метод добавления товара на склад (увеличение количества)
    def add_stock(self, product_id, quantity):
        product = self.find_product_by_id(product_id)
        if product:
            return product.add_stock(quantity)

        print(f"Error: Product with ID {product_id} not found")
        return False

    # Метод удаления товара со склада (уменьшение количества)
    def remove_stock(self, product_id, quantity):
        product = self.find_product_by_id(product_id)
        if product:
            return product.remove_stock(quantity)

        print(f"Error: Product with ID {product_id} not found")
        return False

    # Метод поиска товара по ID
    def find_product_by_id(self, product_id):
        for product in self._products:
            if product.get_product_id() == product_id:
                return product
        return None

    # Метод поиска товаров по названию
    def search_by_name(self, name):
        term = name.lower()
        return [p for p in self._products if term in p.get_name().lower()]

    # Метод поиска товаров по категории
    def search_by_category(self, category):
        return [p for p in self._products if p.get_category() == category]

    # Метод поиска товаров по поставщику
    def search_by_supplier(self, supplier):
        term = supplier.lower()
        return [p for p in self._products if term in p.get_supplier().lower()]

    # Метод получения товаров с низким запасом
    def get_low_stock_items(self):
        return [p for p in self._products if p.is_low_stock()]

    # Метод получения товаров, требующих переоформления заказа
    def get_reorder_items(self):
        return [p for p in self._products if p.needs_reorder()]

    # Метод расчета общей стоимости инвентаря
    def calculate_inventory_value(self):
        return sum(p.calculate_stock_value() for p in self._products)

    # Метод расчета стоимости по категории
    def calculate_value_by_category(self, category):
        products = self.search_by_category(category)
        return sum(p.calculate_stock_value() for p in products)

    # Метод создания заказа поставки
    def create_supply_order(self, product, quantity, supplier=""):
        order = SupplyOrder(product, quantity, supplier)
        self._supply_orders.append(order)

        print(f"\n✓ Supply order created")
        print(f"Order ID: {order.get_order_id()}")
        print(f"Product: {product.get_name()}")
        print(f"Quantity: {quantity}")
        print(f"Total Cost: ${order.get_total_cost():.2f}")

        return order

    # Метод поиска заказа по ID
    def find_order_by_id(self, order_id):
        for order in self._supply_orders:
            if order.get_order_id() == order_id:
                return order
        return None

    # Метод получения активных заказов
    def get_active_orders(self):
        return [o for o in self._supply_orders
                if o.get_status() not in [OrderStatus.DELIVERED, OrderStatus.CANCELLED]]

    # Метод получения просроченных заказов
    def get_overdue_orders(self):
        return [o for o in self._supply_orders if o.is_overdue()]

    # Метод отображения всех товаров
    def display_all_products(self):
        if not self._products:
            print("\nNo products in warehouse")
            return

        print(f"\n=== {self._warehouse_name} - All Products ===")
        for product in self._products:
            product.display_short()
        print(f"\nTotal products: {len(self._products)}")
        print(f"Total inventory value: ${self.calculate_inventory_value():.2f}")

    # Метод отображения товаров по категориям
    def display_by_category(self):
        print(f"\n=== Products by Category ===")

        for category in Category:
            products = self.search_by_category(category)
            if products:
                print(f"\n--- {category.get_display_name()} ---")
                for product in products:
                    product.display_short()
                print(f"Category value: ${self.calculate_value_by_category(category):.2f}")

    # Метод отображения товаров с низким запасом
    def display_low_stock_items(self):
        items = self.get_low_stock_items()

        if not items:
            print("\n✓ No low stock items")
            return

        print("\n⚠️  === Low Stock Items ===")
        for product in items:
            product.display_short()
        print(f"\nTotal low stock items: {len(items)}")

    # Метод отображения товаров для переоформления заказа
    def display_reorder_items(self):
        items = self.get_reorder_items()

        if not items:
            print("\n✓ No items need reordering")
            return

        print("\n⚠️  === Items Needing Reorder ===")
        # Сортировка по приоритету
        items.sort(key=lambda p: p.get_reorder_priority().value, reverse=True)

        for product in items:
            priority = product.get_reorder_priority().name
            print(f"[{priority:8}] ", end="")
            product.display_short()

        print(f"\nTotal items needing reorder: {len(items)}")

    # Метод отображения всех заказов
    def display_all_orders(self):
        if not self._supply_orders:
            print("\nNo supply orders")
            return

        print(f"\n=== All Supply Orders ===")
        for order in self._supply_orders:
            order.display_short()
        print(f"\nTotal orders: {len(self._supply_orders)}")

    # Метод отображения активных заказов
    def display_active_orders(self):
        orders = self.get_active_orders()

        if not orders:
            print("\nNo active orders")
            return

        print("\n=== Active Supply Orders ===")
        for order in orders:
            order.display_short()
        print(f"\nTotal active orders: {len(orders)}")

    # Метод отображения статистики склада
    def display_statistics(self):
        total_products = len(self._products)
        total_quantity = sum(p.get_quantity() for p in self._products)
        total_value = self.calculate_inventory_value()
        low_stock_count = len(self.get_low_stock_items())
        reorder_count = len(self.get_reorder_items())
        active_orders = len(self.get_active_orders())

        # Статистика по категориям
        category_stats = {}
        for category in Category:
            products = self.search_by_category(category)
            if products:
                category_stats[category] = {
                    'count': len(products),
                    'value': self.calculate_value_by_category(category)
                }

        print(f"\n=== {self._warehouse_name} Statistics ===")
        if self._location:
            print(f"Location: {self._location}")

        print(f"\nInventory Overview:")
        print(f"  Total Products: {total_products}")
        print(f"  Total Units: {total_quantity}")
        print(f"  Total Value: ${total_value:.2f}")

        if total_products > 0:
            print(f"  Average Value per Product: ${total_value / total_products:.2f}")

        print(f"\nStock Status:")
        print(f"  Low Stock Items: {low_stock_count}")
        print(f"  Items Needing Reorder: {reorder_count}")

        print(f"\nSupply Orders:")
        print(f"  Active Orders: {active_orders}")
        print(f"  Total Orders: {len(self._supply_orders)}")

        if category_stats:
            print(f"\nCategory Breakdown:")
            for category, stats in sorted(category_stats.items(),
                                          key=lambda x: x[1]['value'], reverse=True):
                print(f"  {category.get_display_name():15} | "
                      f"Products: {stats['count']:>3} | "
                      f"Value: ${stats['value']:>12.2f}")


# Класс пользовательского интерфейса
class WarehouseUI:
    def __init__(self, warehouse_name, location=""):
        self._warehouse = Warehouse(warehouse_name, location)
        self._initialize_sample_data()

    # Инициализация примерных данных
    def _initialize_sample_data(self):
        # Добавление товаров
        p1 = Product("Laptop Dell XPS", Category.ELECTRONICS, 15, 1299.99, "Dell Inc.", 5)
        p1.set_description("High-performance laptop")
        self._warehouse.add_product(p1)

        p2 = Product("T-Shirt Cotton", Category.CLOTHING, 50, 19.99, "Fashion Co.", 20)
        self._warehouse.add_product(p2)

        p3 = Product("Organic Apples", Category.FOOD, 8, 4.99, "Fresh Farms", 15)
        self._warehouse.add_product(p3)

        p4 = Product("Python Programming Book", Category.BOOKS, 25, 45.99, "Tech Publishers", 10)
        self._warehouse.add_product(p4)

    def run(self):
        print("╔════════════════════════════════════════╗")
        print("║  Warehouse Inventory System            ║")
        print("╚════════════════════════════════════════╝\n")

        while True:
            try:
                self._display_main_menu()
                choice = int(input())

                if choice == 20:
                    print("\nThank you for using Warehouse Inventory System!")
                    break

                self._handle_menu_choice(choice)

            except Exception:
                print("\nError: Invalid input. Please try again.")

    # Отображение главного меню
    def _display_main_menu(self):
        print("\n=== Main Menu ===")
        print("1. Add new product")
        print("2. Remove product")
        print("3. View product details")
        print("4. View all products")
        print("5. View products by category")
        print("6. Add stock")
        print("7. Remove stock")
        print("8. Search by name")
        print("9. Search by category")
        print("10. Search by supplier")
        print("11. View low stock items")
        print("12. View items needing reorder")
        print("13. Create supply order")
        print("14. View all orders")
        print("15. View active orders")
        print("16. Process order (approve/ship/deliver)")
        print("17. Cancel order")
        print("18. Calculate inventory value")
        print("19. View statistics")
        print("20. Exit")
        print("Enter choice (1-20): ", end='')

    # Обработка выбора меню
    def _handle_menu_choice(self, choice):
        actions = {
            1: self._add_product,
            2: self._remove_product,
            3: self._view_product_details,
            4: self._warehouse.display_all_products,
            5: self._warehouse.display_by_category,
            6: self._add_stock,
            7: self._remove_stock,
            8: self._search_by_name,
            9: self._search_by_category,
            10: self._search_by_supplier,
            11: self._warehouse.display_low_stock_items,
            12: self._warehouse.display_reorder_items,
            13: self._create_supply_order,
            14: self._warehouse.display_all_orders,
            15: self._warehouse.display_active_orders,
            16: self._process_order,
            17: self._cancel_order,
            18: self._calculate_inventory_value,
            19: self._warehouse.display_statistics
        }
        if choice in actions:
            actions[choice]()
        else:
            print("Invalid choice. Please try again.")

    def _add_product(self):
        name = input("\nEnter product name: ")

        print("\nSelect category:")
        for i, cat in enumerate(Category, 1):
            print(f"{i}. {cat.get_display_name()}")
        cat_choice = int(input("Enter choice: "))
        category = list(Category)[cat_choice - 1]

        quantity = int(input("Enter initial quantity: "))
        price = float(input("Enter price: $"))
        supplier = input("Enter supplier (optional): ")
        min_stock = int(input("Enter minimum stock level (default 10): ") or "10")

        product = Product(name, category, quantity, price, supplier, min_stock)

        description = input("Enter description (optional): ")
        if description:
            product.set_description(description)

        self._warehouse.add_product(product)

    def _remove_product(self):
        product_id = input("\nEnter product ID: ")
        self._warehouse.remove_product(product_id)

    def _view_product_details(self):
        product_id = input("\nEnter product ID: ")
        product = self._warehouse.find_product_by_id(product_id)
        if product:
            product.display_info()
        else:
            print("Error: Product not found")

    def _add_stock(self):
        product_id = input("\nEnter product ID: ")
        quantity = int(input("Enter quantity to add: "))
        self._warehouse.add_stock(product_id, quantity)

    def _remove_stock(self):
        product_id = input("\nEnter product ID: ")
        quantity = int(input("Enter quantity to remove: "))
        self._warehouse.remove_stock(product_id, quantity)

    def _search_by_name(self):
        name = input("\nEnter product name: ")
        products = self._warehouse.search_by_name(name)

        if not products:
            print("\nNo products found")
            return

        print(f"\n=== Search Results ===")
        for product in products:
            product.display_short()
        print(f"\nFound: {len(products)} product(s)")

    def _search_by_category(self):
        print("\nSelect category:")
        for i, cat in enumerate(Category, 1):
            print(f"{i}. {cat.get_display_name()}")
        cat_choice = int(input("Enter choice: "))
        category = list(Category)[cat_choice - 1]

        products = self._warehouse.search_by_category(category)

        if not products:
            print(f"\nNo products found in {category.get_display_name()}")
            return

        print(f"\n=== {category.get_display_name()} Products ===")
        for product in products:
            product.display_short()
        print(f"\nFound: {len(products)} product(s)")
        print(f"Category value: ${self._warehouse.calculate_value_by_category(category):.2f}")

    def _search_by_supplier(self):
        supplier = input("\nEnter supplier name: ")
        products = self._warehouse.search_by_supplier(supplier)

        if not products:
            print("\nNo products found")
            return

        print(f"\n=== Products from '{supplier}' ===")
        for product in products:
            product.display_short()
        print(f"\nFound: {len(products)} product(s)")

    def _create_supply_order(self):
        product_id = input("\nEnter product ID: ")
        product = self._warehouse.find_product_by_id(product_id)

        if not product:
            print("Error: Product not found")
            return

        quantity = int(input("Enter quantity to order: "))
        supplier = input(f"Enter supplier (default: {product.get_supplier()}): ") or product.get_supplier()

        order = self._warehouse.create_supply_order(product, quantity, supplier)

        delivery_str = input("Enter expected delivery date (YYYY-MM-DD) or press Enter to skip: ")
        if delivery_str.strip():
            try:
                delivery_date = date.fromisoformat(delivery_str)
                order.set_expected_delivery(delivery_date)
            except ValueError:
                print("Invalid date format")

        notes = input("Enter notes (optional): ")
        if notes:
            order.set_notes(notes)

    def _process_order(self):
        order_id = input("\nEnter order ID: ")
        order = self._warehouse.find_order_by_id(order_id)

        if not order:
            print("Error: Order not found")
            return

        print(f"\nCurrent status: {order.get_status().name}")
        print("\nSelect action:")
        print("1. Approve")
        print("2. Ship")
        print("3. Deliver")

        action = int(input("Enter choice (1-3): "))

        if action == 1:
            order.approve()
        elif action == 2:
            order.ship()
        elif action == 3:
            order.deliver()

    def _cancel_order(self):
        order_id = input("\nEnter order ID: ")
        order = self._warehouse.find_order_by_id(order_id)

        if order:
            order.cancel()
        else:
            print("Error: Order not found")

    def _calculate_inventory_value(self):
        total_value = self._warehouse.calculate_inventory_value()
        print(f"\n=== Inventory Value ===")
        print(f"Total Value: ${total_value:.2f}")

        print("\nValue by Category:")
        for category in Category:
            value = self._warehouse.calculate_value_by_category(category)
            if value > 0:
                print(f"  {category.get_display_name():15} | ${value:>12.2f}")


def main():
    ui = WarehouseUI("Central Warehouse", "New York, NY")
    ui.run()


if __name__ == "__main__":
    main()