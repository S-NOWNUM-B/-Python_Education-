from datetime import date, timedelta

class Book:
    _book_counter = 1

    def __init__(self, title, author, isbn, genre, publication_year):
        self._id = Book._book_counter
        Book._book_counter += 1
        self._title = title
        self._author = author
        self._isbn = isbn
        self._genre = genre
        self._publication_year = publication_year
        self._is_available = True
        self._borrower = None
        self._borrow_date = None
        self._return_date = None

    # Геттеры
    def get_id(self):
        return self._id
    def get_title(self):
        return self._title
    def get_author(self):
        return self._author
    def get_isbn(self):
        return self._isbn
    def is_available(self):
        return self._is_available
    def get_borrower(self):
        return self._borrower
    def get_borrow_date(self):
        return self._borrow_date
    def get_return_date(self):
        return self._return_date
    def get_genre(self):
        return self._genre
    def get_publication_year(self):
        return self._publication_year

    # Выдача книги
    def borrow_book(self, borrower_name):
        if not self._is_available:
            print("Error: Book is already borrowed")
            return False
        self._is_available = False
        self._borrower = borrower_name
        self._borrow_date = date.today()
        self._return_date = self._borrow_date + timedelta(weeks=2)
        print("\nBook borrowed successfully!")
        print("Borrower:", borrower_name)
        print("Return date:", self._return_date)
        return True

    # Возврат книги
    def return_book(self):
        if self._is_available:
            print("Error: Book was not borrowed")
            return False
        self._is_available = True
        previous_borrower = self._borrower
        self._borrower = None
        self._borrow_date = None
        self._return_date = None
        print("\nBook returned successfully!")
        print("Previous borrower:", previous_borrower)
        return True

    def display(self):
        status = "[AVAILABLE]" if self._is_available else "[BORROWED]"
        print("\n" + status)
        print("ID:", self._id)
        print("Title:", self._title)
        print("Author:", self._author)
        print("ISBN:", self._isbn)
        print("Genre:", self._genre)
        print("Publication Year:", self._publication_year)
        if not self._is_available:
            print("Borrowed by:", self._borrower)
            print("Borrow date:", self._borrow_date)
            print("Return date:", self._return_date)
            if date.today() > self._return_date:
                print("⚠️  OVERDUE!")
        print("---")

    def display_short(self):
        status = "[✓]" if self._is_available else "[✗]"
        print(f"{status} ID: {self._id} | \"{self._title}\" by {self._author} | ISBN: {self._isbn}")

class Library:
    def __init__(self, library_name):
        self._books = []
        self._library_name = library_name

    def add_book(self, book):
        for existing in self._books:
            if existing.get_isbn() == book.get_isbn():
                print(f"\nError: Book with ISBN {book.get_isbn()} already exists")
                return
        self._books.append(book)
        print("\nBook added successfully!")
        print("Book ID:", book.get_id())
        print("Title:", book.get_title())

    def remove_book(self, book_id):
        for i, book in enumerate(self._books):
            if book.get_id() == book_id:
                print(f"\nBook removed: \"{book.get_title()}\"")
                self._books.pop(i)
                return True
        print(f"\nError: Book with ID {book_id} not found")
        return False

    def search_by_title(self, title):
        term = title.lower()
        return [b for b in self._books if term in b.get_title().lower()]

    def search_by_author(self, author):
        term = author.lower()
        return [b for b in self._books if term in b.get_author().lower()]

    def search_by_isbn(self, isbn):
        for b in self._books:
            if b.get_isbn() == isbn:
                return b
        return None

    def search_by_genre(self, genre):
        term = genre.lower()
        return [b for b in self._books if term in b.get_genre().lower()]

    def find_book_by_id(self, book_id):
        for b in self._books:
            if b.get_id() == book_id:
                return b
        return None

    def show_all_books(self):
        if not self._books:
            print("\nNo books in the library")
            return
        print(f"\n=== {self._library_name} - All Books ===")
        for b in self._books:
            b.display_short()
        print("\nTotal books:", len(self._books))

    def show_available_books(self):
        available = [b for b in self._books if b.is_available()]
        if not available:
            print("\nNo available books")
            return
        print("\n=== Available Books ===")
        for b in available:
            b.display_short()
        print("\nTotal available:", len(available))

    def show_borrowed_books(self):
        borrowed = [b for b in self._books if not b.is_available()]
        if not borrowed:
            print("\nNo borrowed books")
            return
        print("\n=== Borrowed Books ===")
        for b in borrowed:
            b.display_short()
            print(f"    Borrower: {b.get_borrower()} | Return: {b.get_return_date()}")
        print("\nTotal borrowed:", len(borrowed))

    def show_overdue_books(self):
        today = date.today()
        overdue = [b for b in self._books if not b.is_available() and today > b.get_return_date()]
        if not overdue:
            print("\nNo overdue books")
            return
        print("\n=== Overdue Books ===")
        for b in overdue:
            b.display_short()
            print(f"    Borrower: {b.get_borrower()} | Due: {b.get_return_date()}")
        print("\nTotal overdue:", len(overdue))

    def show_statistics(self):
        total = len(self._books)
        available = sum(1 for b in self._books if b.is_available())
        borrowed = total - available
        print(f"\n=== {self._library_name} Statistics ===")
        print("Total books:", total)
        print("Available:", available)
        print("Borrowed:", borrowed)
        if total:
            print(f"Availability rate: {available / total * 100:.1f}%")

class LibraryUI:
    def __init__(self, library_name):
        self._library = Library(library_name)

    def run(self):
        print("=== Library Management System ===")
        print(f"Welcome to {self._library._library_name}!\n")
        while True:
            try:
                self._display_menu()
                choice = int(input())
                if choice == 13:
                    print("\nThank you for using Library Management System!")
                    break
                self._handle_menu(choice)
            except Exception:
                print("\nError: Invalid input. Please try again.")

    def _display_menu(self):
        print("\n=== Main Menu ===")
        print("1. Add new book")
        print("2. Remove book")
        print("3. Borrow book")
        print("4. Return book")
        print("5. Search by title")
        print("6. Search by author")
        print("7. Search by ISBN")
        print("8. Search by genre")
        print("9. View all books")
        print("10. View available books")
        print("11. View borrowed books")
        print("12. View statistics")
        print("13. Exit")
        print("Enter choice (1-13): ", end="")

    def _handle_menu(self, choice):
        if choice == 1:
            self._add_new_book()
        elif choice == 2:
            self._remove_book()
        elif choice == 3:
            self._borrow_book()
        elif choice == 4:
            self._return_book()
        elif choice == 5:
            self._search_by_title()
        elif choice == 6:
            self._search_by_author()
        elif choice == 7:
            self._search_by_isbn()
        elif choice == 8:
            self._search_by_genre()
        elif choice == 9:
            self._library.show_all_books()
        elif choice == 10:
            self._library.show_available_books()
        elif choice == 11:
            self._library.show_borrowed_books()
        elif choice == 12:
            self._library.show_statistics()
        else:
            print("Invalid choice. Please try again.")

    def _add_new_book(self):
        title = input("\nEnter book title: ")
        author = input("Enter author name: ")
        isbn = input("Enter ISBN: ")
        genre = input("Enter genre: ")
        year = int(input("Enter publication year: "))
        book = Book(title, author, isbn, genre, year)
        self._library.add_book(book)

    def _remove_book(self):
        book_id = int(input("\nEnter book ID to remove: "))
        self._library.remove_book(book_id)

    def _borrow_book(self):
        book_id = int(input("\nEnter book ID to borrow: "))
        book = self._library.find_book_by_id(book_id)
        if not book:
            print("Error: Book not found")
            return
        borrower_name = input("Enter borrower name: ")
        book.borrow_book(borrower_name)

    def _return_book(self):
        book_id = int(input("\nEnter book ID to return: "))
        book = self._library.find_book_by_id(book_id)
        if not book:
            print("Error: Book not found")
            return
        book.return_book()

    def _search_by_title(self):
        title = input("\nEnter title to search: ")
        results = self._library.search_by_title(title)
        self._display_search_results(results, "Title")

    def _search_by_author(self):
        author = input("\nEnter author name to search: ")
        results = self._library.search_by_author(author)
        self._display_search_results(results, "Author")

    def _search_by_isbn(self):
        isbn = input("\nEnter ISBN to search: ")
        book = self._library.search_by_isbn(isbn)
        if book:
            print("\n=== Book Found ===")
            book.display()
        else:
            print("\nBook not found")

    def _search_by_genre(self):
        genre = input("\nEnter genre to search: ")
        results = self._library.search_by_genre(genre)
        self._display_search_results(results, "Genre")

    def _display_search_results(self, results, search_type):
        if not results:
            print("\nNo books found")
            return
        print(f"\n=== Search Results ({search_type}) ===")
        for b in results:
            b.display_short()
        print("\nFound:", len(results), "book(s)")

def main():
    ui = LibraryUI("Central Library")
    ui.run()

if __name__ == "__main__":
    main()