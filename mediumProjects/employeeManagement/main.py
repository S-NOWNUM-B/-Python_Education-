from abc import ABC, abstractmethod
from enum import Enum
from datetime import date

# Перечисление для департаментов
class Department(Enum):
    IT = 1
    HR = 2
    FINANCE = 3
    MARKETING = 4
    OPERATIONS = 5

# Перечисление для статуса сотрудника
class EmployeeStatus(Enum):
    ACTIVE = 1
    ON_LEAVE = 2
    TERMINATED = 3

# Абстрактный класс сотрудника
class Employee(ABC):
    _employee_counter = 1000

    def __init__(self, name, base_salary, department):
        self._id = Employee._employee_counter
        Employee._employee_counter += 1
        self._name = name
        self._base_salary = base_salary
        self._department = department
        self._hire_date = date.today()
        self._status = EmployeeStatus.ACTIVE

    # Геттеры
    def get_id(self):
        return self._id
    def get_name(self):
        return self._name
    def get_base_salary(self):
        return self._base_salary
    def get_department(self):
        return self._department
    def get_hire_date(self):
        return self._hire_date
    def get_status(self):
        return self._status

    # Сеттеры
    def set_base_salary(self, base_salary):
        self._base_salary = base_salary
    def set_department(self, department):
        self._department = department
    def set_status(self, status):
        self._status = status

    # Абстрактный метод расчета зарплаты (полиморфизм)
    @abstractmethod
    def calculate_salary(self):
        pass

    # Абстрактный метод получения должности
    @abstractmethod
    def get_position(self):
        pass

    # Метод отображения информации о сотруднике
    def display_info(self):
        print("\n=== Employee Information ===")
        print(f"ID: {self._id}")
        print(f"Name: {self._name}")
        print(f"Position: {self.get_position()}")
        print(f"Department: {self._department.name}")
        print(f"Base Salary: ${self._base_salary:.2f}")
        print(f"Total Salary: ${self.calculate_salary():.2f}")
        print(f"Hire Date: {self._hire_date}")
        print(f"Status: {self._status.name}")
        print("---")

    # Метод краткого отображения
    def display_short(self):
        status_symbol = "✓" if self._status == EmployeeStatus.ACTIVE else "✗"
        print(f"[{status_symbol}] ID: {self._id} | {self._name} | {self.get_position()} | ${self.calculate_salary():.2f}")

# Класс менеджера
class Manager(Employee):
    def __init__(self, name, base_salary, department, bonus, team_size):
        super().__init__(name, base_salary, department)
        self._bonus = bonus
        self._team_size = team_size

    # Геттеры
    def get_bonus(self):
        return self._bonus
    def get_team_size(self):
        return self._team_size

    # Сеттеры
    def set_bonus(self, bonus):
        self._bonus = bonus
    def set_team_size(self, team_size):
        self._team_size = team_size

    # Переопределение метода расчета зарплаты (полиморфизм)
    def calculate_salary(self):
        # Базовая зарплата + бонус + премия за размер команды
        team_bonus = self._team_size * 100  # $100 за каждого члена команды
        return self._base_salary + self._bonus + team_bonus

    # Переопределение метода получения должности
    def get_position(self):
        return "Manager"

    # Переопределение метода отображения информации
    def display_info(self):
        super().display_info()
        print(f"Bonus: ${self._bonus:.2f}")
        print(f"Team Size: {self._team_size}")
        print(f"Team Bonus: ${self._team_size * 100:.2f}")

# Класс разработчика
class Developer(Employee):
    def __init__(self, name, base_salary, department, programming_language, project_count):
        super().__init__(name, base_salary, department)
        self._programming_language = programming_language
        self._project_count = project_count
        self._project_bonus = 500.0  # $500 за проект

    # Геттеры
    def get_programming_language(self):
        return self._programming_language
    def get_project_count(self):
        return self._project_count

    # Сеттеры
    def set_programming_language(self, programming_language):
        self._programming_language = programming_language
    def set_project_count(self, project_count):
        self._project_count = project_count

    # Переопределение метода расчета зарплаты (полиморфизм)
    def calculate_salary(self):
        # Базовая зарплата + бонус за проекты
        return self._base_salary + (self._project_count * self._project_bonus)

    # Переопределение метода получения должности
    def get_position(self):
        return f"Developer ({self._programming_language})"

    # Переопределение метода отображения информации
    def display_info(self):
        super().display_info()
        print(f"Programming Language: {self._programming_language}")
        print(f"Completed Projects: {self._project_count}")
        print(f"Project Bonus: ${self._project_count * self._project_bonus:.2f}")

# Класс дизайнера
class Designer(Employee):
    def __init__(self, name, base_salary, department, specialization, design_count):
        super().__init__(name, base_salary, department)
        self._specialization = specialization
        self._design_count = design_count
        self._design_bonus = 300.0  # $300 за дизайн

    # Геттеры
    def get_specialization(self):
        return self._specialization
    def get_design_count(self):
        return self._design_count

    # Сеттеры
    def set_specialization(self, specialization):
        self._specialization = specialization
    def set_design_count(self, design_count):
        self._design_count = design_count

    # Переопределение метода расчета зарплаты (полиморфизм)
    def calculate_salary(self):
        # Базовая зарплата + бонус за дизайны + премия за креативность
        creativity_bonus = self._base_salary * 0.15  # 15% от базовой зарплаты
        return self._base_salary + (self._design_count * self._design_bonus) + creativity_bonus

    # Переопределение метода получения должности
    def get_position(self):
        return f"Designer ({self._specialization})"

    # Переопределение метода отображения информации
    def display_info(self):
        super().display_info()
        print(f"Specialization: {self._specialization}")
        print(f"Completed Designs: {self._design_count}")
        print(f"Design Bonus: ${self._design_count * self._design_bonus:.2f}")
        print(f"Creativity Bonus: ${self._base_salary * 0.15:.2f}")

# Класс компании
class Company:
    def __init__(self, company_name):
        self._company_name = company_name
        self._employees = []

    # Метод добавления сотрудника
    def add_employee(self, employee):
        self._employees.append(employee)
        print("\nEmployee added successfully!")
        print(f"Employee ID: {employee.get_id()}")
        print(f"Name: {employee.get_name()}")
        print(f"Position: {employee.get_position()}")

    # Метод удаления сотрудника
    def remove_employee(self, employee_id):
        for i, emp in enumerate(self._employees):
            if emp.get_id() == employee_id:
                removed = self._employees.pop(i)
                print(f"\nEmployee removed: {removed.get_name()}")
                return True
        print(f"\nError: Employee with ID {employee_id} not found")
        return False

    # Метод поиска сотрудника по ID
    def find_employee_by_id(self, employee_id):
        for emp in self._employees:
            if emp.get_id() == employee_id:
                return emp
        return None

    # Метод поиска сотрудников по имени
    def search_by_name(self, name):
        term = name.lower()
        return [e for e in self._employees if term in e.get_name().lower()]

    # Метод поиска сотрудников по департаменту
    def get_employees_by_department(self, department):
        return [e for e in self._employees if e.get_department() == department]

    # Метод получения сотрудников по должности (демонстрация полиморфизма)
    def get_employees_by_type(self, employee_type):
        return [e for e in self._employees if isinstance(e, employee_type)]

    # Метод расчета общего фонда заработной платы (полиморфизм)
    def get_total_payroll(self):
        return sum(e.calculate_salary() for e in self._employees if e.get_status() == EmployeeStatus.ACTIVE)

    # Метод расчета средней зарплаты
    def get_average_salary(self):
        active_count = self.get_active_employee_count()
        return self.get_total_payroll() / active_count if active_count > 0 else 0

    # Метод получения количества активных сотрудников
    def get_active_employee_count(self):
        return sum(1 for e in self._employees if e.get_status() == EmployeeStatus.ACTIVE)

    # Метод отображения всех сотрудников
    def display_all_employees(self):
        if not self._employees:
            print("\nNo employees in the company")
            return

        print(f"\n=== {self._company_name} - All Employees ===")
        for emp in self._employees:
            emp.display_short()
        print(f"\nTotal employees: {len(self._employees)}")

    # Метод отображения сотрудников по типу (демонстрация полиморфизма)
    def display_employees_by_type(self):
        print("\n=== Employees by Type ===")

        managers = self.get_employees_by_type(Manager)
        if managers:
            print("\n--- Managers ---")
            for emp in managers:
                emp.display_short()

        developers = self.get_employees_by_type(Developer)
        if developers:
            print("\n--- Developers ---")
            for emp in developers:
                emp.display_short()

        designers = self.get_employees_by_type(Designer)
        if designers:
            print("\n--- Designers ---")
            for emp in designers:
                emp.display_short()

    # Метод отображения сотрудников по департаменту
    def display_by_department(self):
        print("\n=== Employees by Department ===")

        for dept in Department:
            dept_employees = self.get_employees_by_department(dept)
            if dept_employees:
                print(f"\n--- {dept.name} ---")
                for emp in dept_employees:
                    emp.display_short()

    # Метод отображения статистики компании
    def display_statistics(self):
        total_employees = len(self._employees)
        active_employees = self.get_active_employee_count()
        managers = len(self.get_employees_by_type(Manager))
        developers = len(self.get_employees_by_type(Developer))
        designers = len(self.get_employees_by_type(Designer))

        print(f"\n=== {self._company_name} Statistics ===")
        print(f"Total Employees: {total_employees}")
        print(f"Active Employees: {active_employees}")
        print("\nEmployee Distribution:")
        print(f"  Managers: {managers}")
        print(f"  Developers: {developers}")
        print(f"  Designers: {designers}")

        print(f"\nTotal Payroll: ${self.get_total_payroll():.2f}")
        print(f"Average Salary: ${self.get_average_salary():.2f}")

        # Статистика по департаментам
        print("\nDepartment Distribution:")
        for dept in Department:
            count = len(self.get_employees_by_department(dept))
            if count > 0:
                print(f"  {dept.name}: {count}")

    # Метод получения топ сотрудников по зарплате
    def display_top_earners(self, count):
        if not self._employees:
            print("\nNo employees in the company")
            return

        # Сортировка по зарплате (полиморфный вызов calculate_salary)
        sorted_employees = sorted(self._employees, key=lambda e: e.calculate_salary(), reverse=True)

        display_count = min(count, len(sorted_employees))

        print(f"\n=== Top {display_count} Earners ===")
        for i, emp in enumerate(sorted_employees[:display_count], 1):
            print(f"{i}. {emp.get_name()} ({emp.get_position()}) - ${emp.calculate_salary():.2f}")

# Класс пользовательского интерфейса
class CompanyUI:
    def __init__(self, company_name):
        self._company = Company(company_name)
        self._initialize_sample_data()

    # Инициализация примерных данных
    def _initialize_sample_data(self):
        self._company.add_employee(Manager("John Smith", 80000, Department.IT, 10000, 5))
        self._company.add_employee(Developer("Alice Johnson", 70000, Department.IT, "Java", 8))
        self._company.add_employee(Developer("Bob Wilson", 75000, Department.IT, "Python", 10))
        self._company.add_employee(Designer("Emma Davis", 60000, Department.MARKETING, "UI/UX", 12))
        self._company.add_employee(Manager("Sarah Brown", 85000, Department.HR, 8000, 3))

    def run(self):
        print("╔════════════════════════════════════════╗")
        print("║  Employee Management System            ║")
        print("╚════════════════════════════════════════╝\n")

        while True:
            try:
                self._display_main_menu()
                choice = int(input())

                if choice == 13:
                    print("\nGoodbye!")
                    break

                self._handle_menu_choice(choice)

            except Exception:
                print("\nError: Invalid input. Please try again.")

    # Отображение главного меню
    def _display_main_menu(self):
        print("\n=== Main Menu ===")
        print("1. Add new employee")
        print("2. Remove employee")
        print("3. View employee details")
        print("4. Search employee by name")
        print("5. View all employees")
        print("6. View employees by type")
        print("7. View employees by department")
        print("8. Update employee salary")
        print("9. Update employee status")
        print("10. View total payroll")
        print("11. View top earners")
        print("12. View company statistics")
        print("13. Exit")
        print("Enter choice (1-13): ", end='')

    # Обработка выбора меню
    def _handle_menu_choice(self, choice):
        actions = {
            1: self._add_new_employee, 2: self._remove_employee,
            3: self._view_employee_details, 4: self._search_by_name,
            5: self._company.display_all_employees, 6: self._company.display_employees_by_type,
            7: self._company.display_by_department, 8: self._update_salary,
            9: self._update_status, 10: self._view_total_payroll,
            11: self._view_top_earners, 12: self._company.display_statistics
        }
        if choice in actions:
            actions[choice]()
        else:
            print("Invalid choice. Please try again.")

    # Добавление нового сотрудника
    def _add_new_employee(self):
        print("\nSelect employee type:")
        print("1. Manager")
        print("2. Developer")
        print("3. Designer")
        emp_type = int(input("Enter choice (1-3): "))

        name = input("Enter name: ")
        salary = float(input("Enter base salary: $"))

        print("Select department:")
        for i, dept in enumerate(Department, 1):
            print(f"{i}. {dept.name}")
        dept_choice = int(input("Enter choice: "))
        dept = list(Department)[dept_choice - 1]

        employee = None

        if emp_type == 1:  # Manager
            bonus = float(input("Enter bonus amount: $"))
            team_size = int(input("Enter team size: "))
            employee = Manager(name, salary, dept, bonus, team_size)
        elif emp_type == 2:  # Developer
            language = input("Enter programming language: ")
            projects = int(input("Enter number of completed projects: "))
            employee = Developer(name, salary, dept, language, projects)
        elif emp_type == 3:  # Designer
            specialization = input("Enter specialization: ")
            designs = int(input("Enter number of completed designs: "))
            employee = Designer(name, salary, dept, specialization, designs)

        if employee:
            self._company.add_employee(employee)

    def _remove_employee(self):
        emp_id = int(input("\nEnter employee ID to remove: "))
        self._company.remove_employee(emp_id)

    def _view_employee_details(self):
        emp_id = int(input("\nEnter employee ID: "))
        employee = self._company.find_employee_by_id(emp_id)
        if employee:
            employee.display_info()  # Полиморфный вызов
        else:
            print("Error: Employee not found")

    def _search_by_name(self):
        name = input("\nEnter name to search: ")
        results = self._company.search_by_name(name)

        if not results:
            print("\nNo employees found")
            return

        print("\n=== Search Results ===")
        for emp in results:
            emp.display_short()
        print(f"\nFound: {len(results)} employee(s)")

    def _update_salary(self):
        emp_id = int(input("\nEnter employee ID: "))
        employee = self._company.find_employee_by_id(emp_id)
        if not employee:
            print("Error: Employee not found")
            return

        print(f"Current base salary: ${employee.get_base_salary():.2f}")
        new_salary = float(input("Enter new base salary: $"))
        employee.set_base_salary(new_salary)
        print("\nSalary updated successfully!")
        print(f"New total salary: ${employee.calculate_salary():.2f}")

    def _update_status(self):
        emp_id = int(input("\nEnter employee ID: "))
        employee = self._company.find_employee_by_id(emp_id)
        if not employee:
            print("Error: Employee not found")
            return

        print("\nSelect new status:")
        for i, status in enumerate(EmployeeStatus, 1):
            print(f"{i}. {status.name}")
        status_choice = int(input("Enter choice (1-3): "))

        new_status = list(EmployeeStatus)[status_choice - 1]
        employee.set_status(new_status)
        print("\nStatus updated successfully!")

    def _view_total_payroll(self):
        total = self._company.get_total_payroll()
        print(f"\nTotal Payroll: ${total:.2f}")
        print(f"Average Salary: ${self._company.get_average_salary():.2f}")
        print(f"Active Employees: {self._company.get_active_employee_count()}")

    def _view_top_earners(self):
        count = int(input("\nEnter number of top earners to display: "))
        self._company.display_top_earners(count)

def main():
    ui = CompanyUI("TechCorp International")
    ui.run()

if __name__ == "__main__":
    main()