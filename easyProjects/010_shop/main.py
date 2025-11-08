from enum import Enum

# Перечисление категорий товаров
class Category(Enum):
    ELECTRONICS = 1
    CLOTHING = 2
    FOOD = 3
    BOOKS = 4
    SPORTS = 5

# Класс товара
class Product:
    _product_counter = 1

    def __init__(self, name, price, quantity, category, description):
        self._id = Product._product_counter
        Product._product_counter += 1
        self._name = name
        self._price = price
        self._quantity = quantity
        self._category = category
        self._description = description

    # Геттеры
    def get_id(self):
        return self._id
    def get_name(self):
        return self._name
    def get_price(self):
        return self._price
    def get_quantity(self):
        return self._quantity
    def get_category(self):
        return self._category
    def get_description(self):
        return self._description

    # Сеттеры
    def set_price(self, price):
        self._price = price
    def set_quantity(self, quantity):
        self._quantity = quantity

    # Уменьшение количества товара
    def decrease_quantity(self, amount):
        if amount > self._quantity:
            return False
        self._quantity -= amount
        return True

    # Увеличение количества товара
    def increase_quantity(self, amount):
        self._quantity += amount

    # Проверка доступности
    def is_available(self, requested_amount):
        return self._quantity >= requested_amount

    # Отображение информации о товаре
    def display(self):
        print("\n=== Product Details ===")
        print(f"ID: {self._id}")
        print(f"Name: {self._name}")
        print(f"Price: ${self._price:.2f}")
        print(f"Available: {self._quantity} units")
        print(f"Category: {self._category.name}")
        print(f"Description: {self._description}")
        print("---")

    # Краткое отображение товара
    def display_short(self):
        availability = "✓" if self._quantity > 0 else "✗"
        print(f"[{availability}] ID: {self._id} | {self._name} | ${self._price:.2f} | Stock: {self._quantity}")

# Класс элемента корзины
class CartItem:
    def __init__(self, product, quantity):
        self._product = product
        self._quantity = quantity

    # Геттеры
    def get_product(self):
        return self._product
    def get_quantity(self):
        return self._quantity

    # Изменение количества
    def set_quantity(self, quantity):
        self._quantity = quantity

    # Увеличение количества
    def increase_quantity(self, amount):
        self._quantity += amount

    # Уменьшение количества
    def decrease_quantity(self, amount):
        if amount >= self._quantity:
            return False
        self._quantity -= amount
        return True

    # Расчет стоимости позиции
    def get_subtotal(self):
        return self._product.get_price() * self._quantity

    # Отображение элемента корзины
    def display(self):
        print(f"  {self._product.get_name()} (x{self._quantity}) - ${self._product.get_price():.2f} each = ${self.get_subtotal():.2f}")

# Класс корзины покупок
class ShoppingCart:
    TAX_RATE = 0.10  # 10% налог

    def __init__(self):
        self._items = []

    # Добавление товара в корзину
    def add_to_cart(self, product, quantity):
        if quantity <= 0:
            print("Error: Quantity must be positive")
            return False

        if not product.is_available(quantity):
            print("Error: Not enough stock available")
            print(f"Available: {product.get_quantity()} units")
            return False

        # Проверка, есть ли уже этот товар в корзине
        for item in self._items:
            if item.get_product().get_id() == product.get_id():
                new_quantity = item.get_quantity() + quantity
                if not product.is_available(new_quantity):
                    print("Error: Not enough stock for this amount")
                    return False
                item.increase_quantity(quantity)
                print("\nUpdated quantity in cart!")
                print(f"{product.get_name()} - New quantity: {item.get_quantity()}")
                return True

        # Добавляем новый товар в корзину
        self._items.append(CartItem(product, quantity))
        print("\nProduct added to cart!")
        print(f"{product.get_name()} (x{quantity})")
        return True

    # Удаление товара из корзины
    def remove_from_cart(self, product_id):
        for i, item in enumerate(self._items):
            if item.get_product().get_id() == product_id:
                removed = self._items.pop(i)
                print(f"\nRemoved from cart: {removed.get_product().get_name()}")
                return True
        print("\nError: Product not found in cart")
        return False

    # Изменение количества товара в корзине
    def update_quantity(self, product_id, new_quantity):
        if new_quantity <= 0:
            return self.remove_from_cart(product_id)

        for item in self._items:
            if item.get_product().get_id() == product_id:
                if not item.get_product().is_available(new_quantity):
                    print("Error: Not enough stock available")
                    return False
                item.set_quantity(new_quantity)
                print("\nQuantity updated!")
                return True

        print("Error: Product not found in cart")
        return False

    # Очистка корзины
    def clear(self):
        self._items.clear()
        print("\nCart cleared!")

    # Проверка пустоты корзины
    def is_empty(self):
        return len(self._items) == 0

    # Получение количества товаров
    def get_total_items(self):
        return sum(item.get_quantity() for item in self._items)

    # Расчет промежуточной суммы
    def calculate_subtotal(self):
        return sum(item.get_subtotal() for item in self._items)

    # Расчет налога
    def calculate_tax(self):
        return self.calculate_subtotal() * self.TAX_RATE

    # Расчет итоговой суммы
    def calculate_total(self):
        return self.calculate_subtotal() + self.calculate_tax()

    # Отображение содержимого корзины
    def display(self):
        if self.is_empty():
            print("\nYour cart is empty")
            return

        print("\n=== Shopping Cart ===")
        for item in self._items:
            item.display()

        print("\n--- Summary ---")
        print(f"Subtotal: ${self.calculate_subtotal():.2f}")
        print(f"Tax ({self.TAX_RATE * 100:.0f}%): ${self.calculate_tax():.2f}")
        print(f"Total: ${self.calculate_total():.2f}")
        print(f"\nTotal items: {self.get_total_items()}")

    # Получение списка товаров
    def get_items(self):
        return self._items

# Класс магазина
class Shop:
    def __init__(self, shop_name):
        self._shop_name = shop_name
        self._inventory = []
        self._order_history = []
        self._initialize_inventory()

    # Инициализация начального товарного запаса
    def _initialize_inventory(self):
        # Электроника
        self._inventory.append(Product("Laptop", 999.99, 10, Category.ELECTRONICS,
                                      "High-performance laptop with 16GB RAM"))
        self._inventory.append(Product("Smartphone", 599.99, 15, Category.ELECTRONICS,
                                      "Latest model with 128GB storage"))
        self._inventory.append(Product("Headphones", 79.99, 25, Category.ELECTRONICS,
                                      "Wireless noise-cancelling headphones"))

        # Одежда
        self._inventory.append(Product("T-Shirt", 19.99, 50, Category.CLOTHING,
                                      "Cotton casual t-shirt"))
        self._inventory.append(Product("Jeans", 49.99, 30, Category.CLOTHING,
                                      "Classic blue denim jeans"))

        # Еда
        self._inventory.append(Product("Coffee Beans", 12.99, 100, Category.FOOD,
                                      "Premium arabica coffee beans 1kg"))
        self._inventory.append(Product("Chocolate", 3.99, 200, Category.FOOD,
                                      "Swiss dark chocolate bar"))

        # Книги
        self._inventory.append(Product("Java Programming", 45.99, 20, Category.BOOKS,
                                      "Complete guide to Java programming"))
        self._inventory.append(Product("Design Patterns", 39.99, 15, Category.BOOKS,
                                      "Software design patterns book"))

        # Спорт
        self._inventory.append(Product("Yoga Mat", 29.99, 40, Category.SPORTS,
                                      "Non-slip exercise yoga mat"))

    # Добавление товара в магазин
    def add_product(self, product):
        self._inventory.append(product)
        print("\nProduct added to shop inventory!")
        print(f"Product ID: {product.get_id()}")

    # Поиск товара по ID
    def find_product_by_id(self, product_id):
        for product in self._inventory:
            if product.get_id() == product_id:
                return product
        return None

    # Поиск товаров по названию
    def search_by_name(self, name):
        term = name.lower()
        return [p for p in self._inventory if term in p.get_name().lower()]

    # Поиск товаров по категории
    def search_by_category(self, category):
        return [p for p in self._inventory if p.get_category() == category]

    # Поиск товаров в ценовом диапазоне
    def search_by_price_range(self, min_price, max_price):
        return [p for p in self._inventory if min_price <= p.get_price() <= max_price]

    # Отображение всех товаров
    def display_all_products(self):
        if not self._inventory:
            print("\nNo products available")
            return

        print(f"\n=== {self._shop_name} - All Products ===")
        for product in self._inventory:
            product.display_short()
        print(f"\nTotal products: {len(self._inventory)}")

    # Отображение товаров по категориям
    def display_by_category(self):
        category_map = {}
        for product in self._inventory:
            cat = product.get_category()
            if cat not in category_map:
                category_map[cat] = []
            category_map[cat].append(product)

        print("\n=== Products by Category ===")
        for category in Category:
            if category in category_map:
                print(f"\n--- {category.name} ---")
                for product in category_map[category]:
                    product.display_short()

    # Оформление заказа
    def checkout(self, cart):
        if cart.is_empty():
            print("\nError: Cart is empty")
            return False

        # Проверка доступности всех товаров
        for item in cart.get_items():
            product = item.get_product()
            if not product.is_available(item.get_quantity()):
                print(f"\nError: {product.get_name()} is out of stock")
                return False

        # Уменьшаем количество товаров на складе
        for item in cart.get_items():
            product = item.get_product()
            product.decrease_quantity(item.get_quantity())

        # Сохраняем заказ в историю
        order = f"Order - Total: ${cart.calculate_total():.2f} - Items: {cart.get_total_items()}"
        self._order_history.append(order)

        # Отображаем чек
        self._display_receipt(cart)

        return True

    # Отображение чека
    def _display_receipt(self, cart):
        print("\n╔════════════════════════════════╗")
        print(f"║      {self._shop_name} Receipt      ║")
        print("╚════════════════════════════════╝")

        cart.display()

        print("\n✓ Order completed successfully!")
        print("Thank you for your purchase!")

    # Отображение истории заказов
    def display_order_history(self):
        if not self._order_history:
            print("\nNo orders yet")
            return

        print("\n=== Order History ===")
        for i, order in enumerate(self._order_history, 1):
            print(f"{i}. {order}")
        print(f"\nTotal orders: {len(self._order_history)}")

    # Статистика магазина
    def display_statistics(self):
        total_products = len(self._inventory)
        available_products = sum(1 for p in self._inventory if p.get_quantity() > 0)
        total_stock = sum(p.get_quantity() for p in self._inventory)
        total_value = sum(p.get_price() * p.get_quantity() for p in self._inventory)

        print(f"\n=== {self._shop_name} Statistics ===")
        print(f"Total products: {total_products}")
        print(f"Available products: {available_products}")
        print(f"Total stock units: {total_stock}")
        print(f"Total inventory value: ${total_value:.2f}")
        print(f"Total orders: {len(self._order_history)}")

# Класс пользовательского интерфейса
class ShopUI:
    def __init__(self, shop_name):
        self._shop = Shop(shop_name)
        self._cart = ShoppingCart()

    def run(self):
        print("╔════════════════════════════════╗")
        print("║  Welcome to Online Shop!       ║")
        print("╚════════════════════════════════╝\n")

        while True:
            try:
                self._display_main_menu()
                choice = int(input())

                if choice == 11:
                    print("\nThank you for visiting!")
                    break

                self._handle_menu_choice(choice)

            except Exception:
                print("\nError: Invalid input. Please try again.")

    # Отображение главного меню
    def _display_main_menu(self):
        print("\n=== Main Menu ===")
        print("1. View all products")
        print("2. View products by category")
        print("3. Search product by name")
        print("4. Search by price range")
        print("5. View product details")
        print("6. Add to cart")
        print("7. View cart")
        print("8. Update cart")
        print("9. Remove from cart")
        print("10. Checkout")
        print("11. Exit")
        print("Enter choice (1-11): ", end='')

    # Обработка выбора меню
    def _handle_menu_choice(self, choice):
        actions = {
            1: self._shop.display_all_products,
            2: self._view_by_category,
            3: self._search_by_name,
            4: self._search_by_price_range,
            5: self._view_product_details,
            6: self._add_to_cart,
            7: self._cart.display,
            8: self._update_cart,
            9: self._remove_from_cart,
            10: self._checkout
        }
        if choice in actions:
            actions[choice]()
        else:
            print("Invalid choice. Please try again.")

    def _view_by_category(self):
        self._shop.display_by_category()

    def _search_by_name(self):
        name = input("\nEnter product name to search: ")
        results = self._shop.search_by_name(name)
        self._display_search_results(results)

    def _search_by_price_range(self):
        min_price = float(input("\nEnter minimum price: $"))
        max_price = float(input("Enter maximum price: $"))
        results = self._shop.search_by_price_range(min_price, max_price)
        self._display_search_results(results)

    def _display_search_results(self, results):
        if not results:
            print("\nNo products found")
            return
        print("\n=== Search Results ===")
        for product in results:
            product.display_short()
        print(f"\nFound: {len(results)} product(s)")

    def _view_product_details(self):
        product_id = int(input("\nEnter product ID: "))
        product = self._shop.find_product_by_id(product_id)
        if product:
            product.display()
        else:
            print("Error: Product not found")

    def _add_to_cart(self):
        product_id = int(input("\nEnter product ID: "))
        quantity = int(input("Enter quantity: "))
        product = self._shop.find_product_by_id(product_id)
        if product:
            self._cart.add_to_cart(product, quantity)
        else:
            print("Error: Product not found")

    def _update_cart(self):
        if self._cart.is_empty():
            print("\nYour cart is empty")
            return
        self._cart.display()
        product_id = int(input("\nEnter product ID to update: "))
        quantity = int(input("Enter new quantity (0 to remove): "))
        self._cart.update_quantity(product_id, quantity)

    def _remove_from_cart(self):
        if self._cart.is_empty():
            print("\nYour cart is empty")
            return
        self._cart.display()
        product_id = int(input("\nEnter product ID to remove: "))
        self._cart.remove_from_cart(product_id)

    def _checkout(self):
        if self._cart.is_empty():
            print("\nYour cart is empty")
            return
        self._cart.display()
        answer = input("\nProceed with checkout? (y/n): ").lower()
        if answer in ['y', 'yes']:
            if self._shop.checkout(self._cart):
                self._cart.clear()
        else:
            print("\nCheckout cancelled")

def main():
    ui = ShopUI("TechShop")
    ui.run()

if __name__ == "__main__":
    main()