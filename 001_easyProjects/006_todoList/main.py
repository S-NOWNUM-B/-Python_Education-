from enum import Enum
from datetime import datetime, date
import sys

# Перечисление для приоритета задачи
class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

# Класс задачи
class Task:
    _task_counter = 1

    def __init__(self, title, description, priority, deadline):
        self._id = Task._task_counter
        Task._task_counter += 1
        self._title = title
        self._description = description
        self._is_completed = False
        self._priority = priority
        self._deadline = deadline
        self._created_at = date.today()

    # Геттеры и сеттеры
    def get_id(self):
        return self._id
    def get_title(self):
        return self._title
    def set_title(self, title):
        self._title = title
    def get_description(self):
        return self._description
    def set_description(self, description):
        self._description = description
    def is_completed(self):
        return self._is_completed
    def mark_as_completed(self):
        self._is_completed = True
    def mark_as_incomplete(self):
        self._is_completed = False
    def get_priority(self):
        return self._priority
    def set_priority(self, priority):
        self._priority = priority
    def get_deadline(self):
        return self._deadline
    def set_deadline(self, deadline):
        self._deadline = deadline
    def get_created_at(self):
        return self._created_at

    # Отображение задачи (детально)
    def display(self):
        status = "[✓] COMPLETED" if self._is_completed else "[ ] PENDING"
        priority_str = self._priority.name
        print(f"ID: {self._id} | {status}")
        print(f"Title: {self._title}")
        print(f"Description: {self._description}")
        print(f"Priority: {priority_str}")
        print(f"Deadline: {self._deadline if self._deadline else 'No deadline'}")
        print(f"Created: {self._created_at}")
        print("---")

    # Краткий вывод задачи
    def display_short(self):
        status = "[✓]" if self._is_completed else "[ ]"
        dot = "●" * self._priority.value
        deadline_str = f"Due: {self._deadline}" if self._deadline else "No deadline"
        print(f"{status} ID: {self._id} | {self._title} | Priority: {dot} | {deadline_str}")

# Класс списка задач
class TodoList:
    def __init__(self):
        self._tasks = []

    def add_task(self, task):
        self._tasks.append(task)
        print("\nTask added successfully!")
        print("Task ID:", task.get_id())

    def remove_task(self, task_id):
        for i, task in enumerate(self._tasks):
            if task.get_id() == task_id:
                print("\nTask removed:", task.get_title())
                self._tasks.pop(i)
                return True
        print(f"\nError: Task with ID {task_id} not found")
        return False

    def mark_as_completed(self, task_id):
        task = self._find_task_by_id(task_id)
        if task:
            task.mark_as_completed()
            print("\nTask marked as completed:", task.get_title())
            return True
        print(f"\nError: Task with ID {task_id} not found")
        return False

    def mark_as_incomplete(self, task_id):
        task = self._find_task_by_id(task_id)
        if task:
            task.mark_as_incomplete()
            print("\nTask marked as incomplete:", task.get_title())
            return True
        print(f"\nError: Task with ID {task_id} not found")
        return False

    def edit_task(self, task_id, title, description, priority, deadline):
        task = self._find_task_by_id(task_id)
        if task:
            task.set_title(title)
            task.set_description(description)
            task.set_priority(priority)
            task.set_deadline(deadline)
            print("\nTask updated successfully!")
            return True
        print(f"\nError: Task with ID {task_id} not found")
        return False

    def show_all_tasks(self):
        if not self._tasks:
            print("\nNo tasks in the list")
            return
        print("\n=== All Tasks ===")
        for task in self._tasks:
            task.display_short()
        print("\nTotal tasks:", len(self._tasks))

    def show_tasks_by_status(self, completed):
        filtered = [task for task in self._tasks if task.is_completed() == completed]
        if not filtered:
            print(f"\nNo {'completed' if completed else 'pending'} tasks")
            return
        print(f"\n=== {'Completed' if completed else 'Pending'} Tasks ===")
        for task in filtered:
            task.display_short()
        print("\nTotal:", len(filtered))

    def show_tasks_by_priority(self, priority):
        filtered = [task for task in self._tasks if task.get_priority() == priority]
        if not filtered:
            print(f"\nNo tasks with {priority.name} priority")
            return
        print(f"\n=== {priority.name} Priority Tasks ===")
        for task in filtered:
            task.display_short()
        print("\nTotal:", len(filtered))

    def show_task_details(self, task_id):
        task = self._find_task_by_id(task_id)
        if task:
            print("\n=== Task Details ===")
            task.display()
        else:
            print(f"\nError: Task with ID {task_id} not found")

    def show_statistics(self):
        total = len(self._tasks)
        completed = sum(1 for task in self._tasks if task.is_completed())
        pending = total - completed
        high_priority = sum(1 for task in self._tasks if task.get_priority() == Priority.HIGH)
        print("\n=== Statistics ===")
        print("Total tasks:", total)
        print("Completed:", completed)
        print("Pending:", pending)
        print("High priority tasks:", high_priority)
        if total:
            print(f"Completion rate: {completed/total*100:.1f}%")

    # Вспомогательные методы
    def _find_task_by_id(self, task_id):
        for task in self._tasks:
            if task.get_id() == task_id:
                return task
        return None

# Класс пользовательского интерфейса
class TodoUI:
    def __init__(self):
        self._todo_list = TodoList()
        self._date_format = "%Y-%m-%d"

    def run(self):
        print("=== Todo List Manager ===\n")
        while True:
            try:
                self._display_menu()
                choice = int(input())
                if choice == 11:
                    print("\nGoodbye! Keep being productive!")
                    break
                self._handle_choice(choice)
            except Exception:
                print("\nError: Invalid input. Please try again.")

    def _display_menu(self):
        print("\n=== Main Menu ===")
        print("1. Add new task")
        print("2. Remove task")
        print("3. Mark task as completed")
        print("4. Mark task as incomplete")
        print("5. Edit task")
        print("6. View all tasks")
        print("7. View completed tasks")
        print("8. View pending tasks")
        print("9. View task details")
        print("10. View statistics")
        print("11. Exit")
        print("Enter choice (1-11): ", end='')

    def _handle_choice(self, choice):
        if choice == 1:
            self._add_new_task()
        elif choice == 2:
            self._remove_task()
        elif choice == 3:
            self._mark_task(True)
        elif choice == 4:
            self._mark_task(False)
        elif choice == 5:
            self._edit_task()
        elif choice == 6:
            self._todo_list.show_all_tasks()
        elif choice == 7:
            self._todo_list.show_tasks_by_status(True)
        elif choice == 8:
            self._todo_list.show_tasks_by_status(False)
        elif choice == 9:
            self._view_task_details()
        elif choice == 10:
            self._todo_list.show_statistics()
        else:
            print("Invalid choice. Please try again.")

    def _add_new_task(self):
        title = input("\nEnter task title: ")
        description = input("Enter task description: ")

        print("Select priority:")
        for val in Priority:
            print(f"{val.value}. {val.name}")
        priority_choice = int(input("Enter choice (1-3): "))
        priority = Priority(priority_choice) if priority_choice in [1,2,3] else Priority.MEDIUM

        deadline_str = input("Enter deadline (yyyy-mm-dd) or press Enter to skip: ").strip()
        deadline = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, self._date_format).date()
            except ValueError:
                print("Invalid date format. No deadline set.")

        task = Task(title, description, priority, deadline)
        self._todo_list.add_task(task)

    def _remove_task(self):
        task_id = int(input("\nEnter task ID to remove: "))
        self._todo_list.remove_task(task_id)

    def _mark_task(self, completed):
        task_id = int(input(f"\nEnter task ID to mark as {'completed' if completed else 'incomplete'}: "))
        if completed:
            self._todo_list.mark_as_completed(task_id)
        else:
            self._todo_list.mark_as_incomplete(task_id)

    def _edit_task(self):
        task_id = int(input("\nEnter task ID to edit: "))
        title = input("Enter new title: ")
        description = input("Enter new description: ")

        print("Select new priority:")
        for val in Priority:
            print(f"{val.value}. {val.name}")
        priority_choice = int(input("Enter choice (1-3): "))
        priority = Priority(priority_choice) if priority_choice in [1,2,3] else Priority.MEDIUM

        deadline_str = input("Enter new deadline (yyyy-mm-dd) or press Enter to skip: ").strip()
        deadline = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, self._date_format).date()
            except ValueError:
                print("Invalid date format. No deadline set.")

        self._todo_list.edit_task(task_id, title, description, priority, deadline)

    def _view_task_details(self):
        task_id = int(input("\nEnter task ID to view details: "))
        self._todo_list.show_task_details(task_id)

def main():
    ui = TodoUI()
    ui.run()

if __name__ == "__main__":
    main()