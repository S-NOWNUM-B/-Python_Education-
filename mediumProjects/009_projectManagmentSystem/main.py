from enum import Enum
from datetime import datetime, date, timedelta
from decimal import Decimal


# Перечисление приоритетов задач
class Priority(Enum):
    LOW = ("Низкий", 1)
    MEDIUM = ("Средний", 2)
    HIGH = ("Высокий", 3)
    CRITICAL = ("Критический", 4)

    def __init__(self, display_name, value):
        self._display_name = display_name
        self._priority_value = value

    def get_display_name(self):
        return self._display_name

    def get_priority_value(self):
        return self._priority_value


# Перечисление статусов задач
class Status(Enum):
    TODO = "К выполнению"
    IN_PROGRESS = "В работе"
    REVIEW = "На проверке"
    DONE = "Завершено"
    CANCELLED = "Отменено"
    BLOCKED = "Заблокировано"

    def __init__(self, display_name):
        self._display_name = display_name

    def get_display_name(self):
        return self._display_name


# Перечисление ролей в команде
class Role(Enum):
    DEVELOPER = "Разработчик"
    DESIGNER = "Дизайнер"
    TESTER = "Тестировщик"
    PROJECT_MANAGER = "Менеджер проекта"
    TEAM_LEAD = "Тимлид"
    ANALYST = "Аналитик"

    def __init__(self, display_name):
        self._display_name = display_name

    def get_display_name(self):
        return self._display_name


# Перечисление типов задач
class TaskType(Enum):
    FEATURE = "Функционал"
    BUG = "Ошибка"
    IMPROVEMENT = "Улучшение"
    DOCUMENTATION = "Документация"
    TESTING = "Тестирование"
    RESEARCH = "Исследование"

    def __init__(self, display_name):
        self._display_name = display_name

    def get_display_name(self):
        return self._display_name


# Класс задачи
class Task:
    _task_counter = 1

    def __init__(self, title, description, priority=Priority.MEDIUM,
                 task_type=TaskType.FEATURE, estimated_hours=0):
        self._task_id = f"TASK-{Task._task_counter}"
        Task._task_counter += 1
        self._title = title
        self._description = description
        self._priority = priority
        self._status = Status.TODO
        self._task_type = task_type
        self._assignee = None
        self._created_date = datetime.now()
        self._updated_date = datetime.now()
        self._due_date = None
        self._estimated_hours = estimated_hours
        self._actual_hours = 0
        self._tags = []
        self._comments = []
        self._subtasks = []

    # Геттеры
    def get_task_id(self):
        return self._task_id

    def get_title(self):
        return self._title

    def get_description(self):
        return self._description

    def get_priority(self):
        return self._priority

    def get_status(self):
        return self._status

    def get_task_type(self):
        return self._task_type

    def get_assignee(self):
        return self._assignee

    def get_created_date(self):
        return self._created_date

    def get_updated_date(self):
        return self._updated_date

    def get_due_date(self):
        return self._due_date

    def get_estimated_hours(self):
        return self._estimated_hours

    def get_actual_hours(self):
        return self._actual_hours

    def get_tags(self):
        return self._tags

    def get_comments(self):
        return self._comments

    def get_subtasks(self):
        return self._subtasks

    # Сеттеры
    def set_title(self, title):
        self._title = title
        self._update_timestamp()

    def set_description(self, description):
        self._description = description
        self._update_timestamp()

    def set_priority(self, priority):
        old_priority = self._priority
        self._priority = priority
        self._update_timestamp()
        print(f"\n✓ Приоритет изменен: {old_priority.get_display_name()} → {priority.get_display_name()}")

    def set_status(self, status):
        old_status = self._status
        self._status = status
        self._update_timestamp()
        print(f"\n✓ Статус изменен: {old_status.get_display_name()} → {status.get_display_name()}")

    def set_assignee(self, assignee):
        self._assignee = assignee
        self._update_timestamp()

    def set_due_date(self, due_date):
        self._due_date = due_date
        self._update_timestamp()

    def set_actual_hours(self, hours):
        self._actual_hours = hours
        self._update_timestamp()

    # Метод обновления временной метки
    def _update_timestamp(self):
        self._updated_date = datetime.now()

    # Метод добавления тега
    def add_tag(self, tag):
        if tag not in self._tags:
            self._tags.append(tag)
            print(f"\n✓ Тег добавлен: {tag}")

    # Метод добавления комментария
    def add_comment(self, author, text):
        comment = {
            'author': author,
            'text': text,
            'timestamp': datetime.now()
        }
        self._comments.append(comment)
        print(f"\n✓ Комментарий добавлен")

    # Метод добавления подзадачи
    def add_subtask(self, subtask):
        self._subtasks.append(subtask)
        print(f"\n✓ Подзадача добавлена: {subtask.get_title()}")

    # Метод проверки просрочки
    def is_overdue(self):
        if self._due_date and self._status not in [Status.DONE, Status.CANCELLED]:
            return datetime.now().date() > self._due_date
        return False

    # Метод расчета прогресса подзадач
    def calculate_subtask_progress(self):
        if not self._subtasks:
            return 100 if self._status == Status.DONE else 0

        completed = sum(1 for st in self._subtasks if st.get_status() == Status.DONE)
        return (completed / len(self._subtasks)) * 100

    # Метод проверки, назначена ли задача
    def is_assigned(self):
        return self._assignee is not None

    # Метод отображения информации о задаче
    def display_info(self):
        print("\n=== Информация о задаче ===")
        print(f"ID: {self._task_id}")
        print(f"Название: {self._title}")
        print(f"Описание: {self._description}")
        print(f"Тип: {self._task_type.get_display_name()}")
        print(f"Приоритет: {self._priority.get_display_name()}")
        print(f"Статус: {self._status.get_display_name()}")

        if self._assignee:
            print(f"Исполнитель: {self._assignee.get_name()} ({self._assignee.get_role().get_display_name()})")
        else:
            print("Исполнитель: Не назначен")

        print(f"Создана: {self._created_date.strftime('%Y-%m-%d %H:%M')}")
        print(f"Обновлена: {self._updated_date.strftime('%Y-%m-%d %H:%M')}")

        if self._due_date:
            print(f"Срок: {self._due_date}")
            if self.is_overdue():
                days_overdue = (datetime.now().date() - self._due_date).days
                print(f"⚠️  ПРОСРОЧЕНО на {days_overdue} дней!")

        print(f"Оценка: {self._estimated_hours}ч | Фактически: {self._actual_hours}ч")

        if self._tags:
            print(f"Теги: {', '.join(self._tags)}")

        if self._subtasks:
            progress = self.calculate_subtask_progress()
            print(f"Подзадач: {len(self._subtasks)} (Прогресс: {progress:.0f}%)")

        if self._comments:
            print(f"Комментариев: {len(self._comments)}")

        print("---")

    # Метод краткого отображения задачи
    def display_short(self):
        priority_symbols = {
            Priority.LOW: "⬇️",
            Priority.MEDIUM: "➡️",
            Priority.HIGH: "⬆️",
            Priority.CRITICAL: "🔥"
        }

        status_symbols = {
            Status.TODO: "📋",
            Status.IN_PROGRESS: "🔄",
            Status.REVIEW: "👀",
            Status.DONE: "✅",
            Status.CANCELLED: "❌",
            Status.BLOCKED: "🚫"
        }

        priority_symbol = priority_symbols.get(self._priority, "?")
        status_symbol = status_symbols.get(self._status, "?")

        assignee_name = self._assignee.get_name() if self._assignee else "Не назначен"
        overdue = " [ПРОСРОЧЕНО]" if self.is_overdue() else ""

        print(f"{priority_symbol} {status_symbol} {self._task_id} | {self._title:35} | "
              f"{assignee_name:20} | {self._status.get_display_name():15}{overdue}")


# Класс члена команды
class TeamMember:
    def __init__(self, name, role, email=""):
        self._member_id = f"MEM-{id(self)}"
        self._name = name
        self._role = role
        self._email = email
        self._assigned_tasks = []
        self._join_date = date.today()
        self._is_active = True

    # Геттеры
    def get_member_id(self):
        return self._member_id

    def get_name(self):
        return self._name

    def get_role(self):
        return self._role

    def get_email(self):
        return self._email

    def get_assigned_tasks(self):
        return self._assigned_tasks

    def get_join_date(self):
        return self._join_date

    def is_active(self):
        return self._is_active

    # Сеттеры
    def set_role(self, role):
        old_role = self._role
        self._role = role
        print(f"\n✓ Роль изменена: {old_role.get_display_name()} → {role.get_display_name()}")

    def set_active(self, active):
        self._is_active = active

    # Метод назначения задачи
    def assign_task(self, task):
        if task not in self._assigned_tasks:
            self._assigned_tasks.append(task)
            task.set_assignee(self)

    # Метод снятия задачи
    def unassign_task(self, task):
        if task in self._assigned_tasks:
            self._assigned_tasks.remove(task)
            task.set_assignee(None)

    # Метод получения активных задач
    def get_active_tasks(self):
        return [t for t in self._assigned_tasks
                if t.get_status() not in [Status.DONE, Status.CANCELLED]]

    # Метод получения завершенных задач
    def get_completed_tasks(self):
        return [t for t in self._assigned_tasks if t.get_status() == Status.DONE]

    # Метод расчета рабочей нагрузки (часы)
    def calculate_workload(self):
        active_tasks = self.get_active_tasks()
        total_hours = sum(t.get_estimated_hours() for t in active_tasks)
        return total_hours

    # Метод получения задач по приоритету
    def get_tasks_by_priority(self, priority):
        return [t for t in self._assigned_tasks if t.get_priority() == priority]

    # Метод получения просроченных задач
    def get_overdue_tasks(self):
        return [t for t in self._assigned_tasks if t.is_overdue()]

    # Метод отображения информации о члене команды
    def display_info(self):
        print("\n=== Информация о члене команды ===")
        print(f"ID: {self._member_id}")
        print(f"Имя: {self._name}")
        print(f"Роль: {self._role.get_display_name()}")
        print(f"Email: {self._email if self._email else 'Не указан'}")
        print(f"Дата присоединения: {self._join_date}")
        print(f"Статус: {'Активен' if self._is_active else 'Неактивен'}")
        print(f"Назначено задач: {len(self._assigned_tasks)}")
        print(f"Активных задач: {len(self.get_active_tasks())}")
        print(f"Завершено задач: {len(self.get_completed_tasks())}")
        print(f"Рабочая нагрузка: {self.calculate_workload()}ч")

        overdue = self.get_overdue_tasks()
        if overdue:
            print(f"⚠️  Просроченных задач: {len(overdue)}")

        print("---")

    # Метод краткого отображения члена команды
    def display_short(self):
        status = "✓" if self._is_active else "✗"
        active_tasks = len(self.get_active_tasks())
        workload = self.calculate_workload()

        print(f"[{status}] {self._name:20} | {self._role.get_display_name():20} | "
              f"Задач: {active_tasks:>2} | Нагрузка: {workload:>3}ч")


# Класс проекта
class Project:
    def __init__(self, project_name, description=""):
        self._project_id = f"PRJ-{id(self)}"
        self._project_name = project_name
        self._description = description
        self._tasks = []
        self._team_members = []
        self._created_date = date.today()
        self._start_date = None
        self._deadline = None
        self._is_active = True

    # Геттеры
    def get_project_id(self):
        return self._project_id

    def get_project_name(self):
        return self._project_name

    def get_description(self):
        return self._description

    def get_tasks(self):
        return self._tasks

    def get_team_members(self):
        return self._team_members

    def get_created_date(self):
        return self._created_date

    def is_active(self):
        return self._is_active

    # Метод добавления задачи
    def add_task(self, task):
        self._tasks.append(task)
        print(f"\n✓ Задача добавлена в проект: {task.get_title()}")
        return task

    # Метод добавления члена команды
    def add_team_member(self, member):
        if member not in self._team_members:
            self._team_members.append(member)
            print(f"\n✓ Член команды добавлен: {member.get_name()}")
            return True
        print(f"Ошибка: {member.get_name()} уже в проекте")
        return False

    # Метод удаления задачи
    def remove_task(self, task_id):
        for i, task in enumerate(self._tasks):
            if task.get_task_id() == task_id:
                removed = self._tasks.pop(i)
                print(f"\n✓ Задача удалена: {removed.get_title()}")
                return True
        print(f"Ошибка: Задача {task_id} не найдена")
        return False

    # Метод поиска задачи по ID
    def find_task(self, task_id):
        for task in self._tasks:
            if task.get_task_id() == task_id:
                return task
        return None

    # Метод поиска члена команды по имени
    def find_member(self, name):
        for member in self._team_members:
            if member.get_name().lower() == name.lower():
                return member
        return None

    # Метод назначения задачи
    def assign_task(self, task_id, member_name):
        task = self.find_task(task_id)
        if not task:
            print(f"Ошибка: Задача {task_id} не найдена")
            return False

        member = self.find_member(member_name)
        if not member:
            print(f"Ошибка: Член команды '{member_name}' не найден")
            return False

        # Снять задачу с предыдущего исполнителя
        if task.get_assignee():
            task.get_assignee().unassign_task(task)

        # Назначить новому исполнителю
        member.assign_task(task)

        print(f"\n✓ Задача '{task.get_title()}' назначена на {member.get_name()}")
        return True

    # Метод обновления статуса задачи
    def update_task_status(self, task_id, new_status):
        task = self.find_task(task_id)
        if task:
            task.set_status(new_status)
            return True
        print(f"Ошибка: Задача {task_id} не найдена")
        return False

    # Метод получения задач по приоритету
    def get_tasks_by_priority(self, priority):
        return [t for t in self._tasks if t.get_priority() == priority]

    # Метод получения задач по статусу
    def get_tasks_by_status(self, status):
        return [t for t in self._tasks if t.get_status() == status]

    # Метод получения задач по исполнителю
    def get_tasks_by_assignee(self, member):
        return [t for t in self._tasks if t.get_assignee() == member]

    # Метод получения неназначенных задач
    def get_unassigned_tasks(self):
        return [t for t in self._tasks if not t.is_assigned()]

    # Метод получения просроченных задач
    def get_overdue_tasks(self):
        return [t for t in self._tasks if t.is_overdue()]

    # Метод получения рабочей нагрузки члена команды
    def get_member_workload(self, member_name):
        member = self.find_member(member_name)
        if member:
            workload = member.calculate_workload()
            print(f"\n=== Рабочая нагрузка: {member.get_name()} ===")
            print(f"Активных задач: {len(member.get_active_tasks())}")
            print(f"Общая нагрузка: {workload} часов")

            active_tasks = member.get_active_tasks()
            if active_tasks:
                print("\nАктивные задачи:")
                for task in active_tasks:
                    task.display_short()

            return workload

        print(f"Ошибка: Член команды '{member_name}' не найден")
        return None

    # Метод сортировки задач по приоритету
    def get_tasks_sorted_by_priority(self):
        return sorted(self._tasks,
                      key=lambda t: t.get_priority().get_priority_value(),
                      reverse=True)

    # Метод сортировки задач по сроку
    def get_tasks_sorted_by_deadline(self):
        tasks_with_deadline = [t for t in self._tasks if t.get_due_date()]
        return sorted(tasks_with_deadline, key=lambda t: t.get_due_date())

    # Метод отображения всех задач
    def display_all_tasks(self):
        if not self._tasks:
            print("\nНет задач в проекте")
            return

        print(f"\n=== Задачи проекта '{self._project_name}' ===")
        for task in self._tasks:
            task.display_short()
        print(f"\nВсего задач: {len(self._tasks)}")

    # Метод отображения всех членов команды
    def display_all_members(self):
        if not self._team_members:
            print("\nНет членов команды")
            return

        print(f"\n=== Команда проекта '{self._project_name}' ===")
        for member in self._team_members:
            member.display_short()
        print(f"\nВсего членов команды: {len(self._team_members)}")

    # Метод отображения задач по приоритетам
    def display_tasks_by_priority(self):
        print(f"\n=== Задачи по приоритетам ===")

        for priority in reversed(list(Priority)):
            tasks = self.get_tasks_by_priority(priority)
            if tasks:
                print(f"\n--- {priority.get_display_name()} ({len(tasks)}) ---")
                for task in tasks:
                    task.display_short()

    # Метод отображения задач по статусам
    def display_tasks_by_status(self):
        print(f"\n=== Задачи по статусам ===")

        for status in Status:
            tasks = self.get_tasks_by_status(status)
            if tasks:
                print(f"\n--- {status.get_display_name()} ({len(tasks)}) ---")
                for task in tasks:
                    task.display_short()

    # Метод отображения статистики проекта
    def display_statistics(self):
        total_tasks = len(self._tasks)
        total_members = len(self._team_members)

        # Статистика по статусам
        status_counts = {}
        for status in Status:
            count = len(self.get_tasks_by_status(status))
            if count > 0:
                status_counts[status] = count

        # Статистика по приоритетам
        priority_counts = {}
        for priority in Priority:
            count = len(self.get_tasks_by_priority(priority))
            if count > 0:
                priority_counts[priority] = count

        unassigned = len(self.get_unassigned_tasks())
        overdue = len(self.get_overdue_tasks())

        # Расчет прогресса
        done_tasks = len(self.get_tasks_by_status(Status.DONE))
        progress = (done_tasks / total_tasks * 100) if total_tasks > 0 else 0

        print(f"\n=== Статистика проекта '{self._project_name}' ===")
        print(f"Всего задач: {total_tasks}")
        print(f"Прогресс: {progress:.1f}% ({done_tasks}/{total_tasks})")
        print(f"Членов команды: {total_members}")

        if status_counts:
            print("\nПо статусам:")
            for status, count in status_counts.items():
                print(f"  {status.get_display_name()}: {count}")

        if priority_counts:
            print("\nПо приоритетам:")
            for priority, count in priority_counts.items():
                print(f"  {priority.get_display_name()}: {count}")

        print(f"\nНе назначено: {unassigned}")
        if overdue > 0:
            print(f"⚠️  Просрочено: {overdue}")

        # Топ загруженных членов команды
        if self._team_members:
            members_by_workload = sorted(self._team_members,
                                         key=lambda m: m.calculate_workload(),
                                         reverse=True)
            print("\nТоп-3 загруженных:")
            for i, member in enumerate(members_by_workload[:3], 1):
                print(f"  {i}. {member.get_name()} - {member.calculate_workload()}ч "
                      f"({len(member.get_active_tasks())} задач)")


# Класс пользовательского интерфейса
class ProjectManagementUI:
    def __init__(self):
        self._projects = []
        self._current_project = None
        self._initialize_sample_data()

    # Инициализация примерных данных
    def _initialize_sample_data(self):
        # Создание проекта
        project = Project("Веб-приложение", "Разработка веб-приложения для управления задачами")
        self._projects.append(project)
        self._current_project = project

        # Добавление членов команды
        dev1 = TeamMember("Алексей Иванов", Role.DEVELOPER, "alexey@example.com")
        dev2 = TeamMember("Мария Петрова", Role.DEVELOPER, "maria@example.com")
        designer = TeamMember("Ольга Сидорова", Role.DESIGNER, "olga@example.com")
        tester = TeamMember("Иван Смирнов", Role.TESTER, "ivan@example.com")

        project.add_team_member(dev1)
        project.add_team_member(dev2)
        project.add_team_member(designer)
        project.add_team_member(tester)

        # Добавление задач
        task1 = Task("Разработать главную страницу", "Создать дизайн и реализовать главную страницу",
                     Priority.HIGH, TaskType.FEATURE, 16)
        task1.set_due_date(date.today() + timedelta(days=7))
        project.add_task(task1)
        project.assign_task(task1.get_task_id(), dev1.get_name())

        task2 = Task("Исправить баг авторизации", "Пользователь не может войти через Google",
                     Priority.CRITICAL, TaskType.BUG, 4)
        task2.set_due_date(date.today() + timedelta(days=2))
        project.add_task(task2)
        project.assign_task(task2.get_task_id(), dev2.get_name())

        task3 = Task("Создать дизайн профиля", "Дизайн страницы профиля пользователя",
                     Priority.MEDIUM, TaskType.FEATURE, 8)
        project.add_task(task3)
        project.assign_task(task3.get_task_id(), designer.get_name())

    def run(self):
        print("╔════════════════════════════════════════╗")
        print("║  Система управления проектами         ║")
        print("╚════════════════════════════════════════╝\n")

        while True:
            try:
                self._display_main_menu()
                choice = int(input())

                if choice == 25:
                    print("\nУспехов в работе!")
                    break

                self._handle_menu_choice(choice)

            except Exception:
                print("\nОшибка: Неверный ввод. Попробуйте снова.")

    # Отображение главного меню
    def _display_main_menu(self):
        print("\n=== Главное меню ===")
        if self._current_project:
            print(f"Текущий проект: {self._current_project.get_project_name()}")

        print("\n--- Задачи ---")
        print("1. Создать задачу")
        print("2. Просмотреть все задачи")
        print("3. Просмотреть задачи по приоритетам")
        print("4. Просмотреть задачи по статусам")
        print("5. Просмотреть детали задачи")
        print("6. Обновить статус задачи")
        print("7. Изменить приоритет задачи")
        print("8. Назначить задачу")
        print("9. Добавить комментарий к задаче")
        print("10. Просмотреть неназначенные задачи")
        print("11. Просмотреть просроченные задачи")

        print("\n--- Команда ---")
        print("12. Добавить члена команды")
        print("13. Просмотреть всю команду")
        print("14. Просмотреть детали члена команды")
        print("15. Рабочая нагрузка члена команды")
        print("16. Задачи члена команды")

        print("\n--- Проект ---")
        print("17. Создать проект")
        print("18. Переключить проект")
        print("19. Просмотреть статистику проекта")
        print("20. Установить срок задачи")
        print("21. Добавить тег к задаче")
        print("22. Поиск задач по тегу")
        print("23. Задачи отсортированные по приоритету")
        print("24. Задачи отсортированные по сроку")
        print("25. Выход")
        print("Введите выбор (1-25): ", end='')

    # Обработка выбора меню
    def _handle_menu_choice(self, choice):
        if not self._current_project and choice not in [17, 25]:
            print("Ошибка: Проект не выбран. Создайте или выберите проект.")
            return

        actions = {
            1: self._create_task,
            2: self._view_all_tasks,
            3: self._view_tasks_by_priority,
            4: self._view_tasks_by_status,
            5: self._view_task_details,
            6: self._update_task_status,
            7: self._change_task_priority,
            8: self._assign_task,
            9: self._add_comment,
            10: self._view_unassigned_tasks,
            11: self._view_overdue_tasks,
            12: self._add_team_member,
            13: self._view_all_members,
            14: self._view_member_details,
            15: self._view_member_workload,
            16: self._view_member_tasks,
            17: self._create_project,
            18: self._switch_project,
            19: self._view_statistics,
            20: self._set_task_deadline,
            21: self._add_tag_to_task,
            22: self._search_by_tag,
            23: self._view_tasks_sorted_by_priority,
            24: self._view_tasks_sorted_by_deadline
        }

        if choice in actions:
            actions[choice]()
        else:
            print("Неверный выбор. Попробуйте снова.")

    def _create_task(self):
        title = input("\nНазвание задачи: ")
        description = input("Описание: ")

        print("\nВыберите приоритет:")
        for i, priority in enumerate(Priority, 1):
            print(f"{i}. {priority.get_display_name()}")
        priority_choice = int(input("Введите выбор: "))
        priority = list(Priority)[priority_choice - 1]

        print("\nВыберите тип задачи:")
        for i, task_type in enumerate(TaskType, 1):
            print(f"{i}. {task_type.get_display_name()}")
        type_choice = int(input("Введите выбор: "))
        task_type = list(TaskType)[type_choice - 1]

        estimated = int(input("Оценка времени (часы): ") or "0")

        task = Task(title, description, priority, task_type, estimated)
        self._current_project.add_task(task)

    def _view_all_tasks(self):
        self._current_project.display_all_tasks()

    def _view_tasks_by_priority(self):
        self._current_project.display_tasks_by_priority()

    def _view_tasks_by_status(self):
        self._current_project.display_tasks_by_status()

    def _view_task_details(self):
        task_id = input("\nВведите ID задачи: ")
        task = self._current_project.find_task(task_id)
        if task:
            task.display_info()
        else:
            print("Задача не найдена")

    def _update_task_status(self):
        task_id = input("\nВведите ID задачи: ")

        print("\nВыберите новый статус:")
        for i, status in enumerate(Status, 1):
            print(f"{i}. {status.get_display_name()}")

        status_choice = int(input("Введите выбор: "))
        new_status = list(Status)[status_choice - 1]

        self._current_project.update_task_status(task_id, new_status)

    def _change_task_priority(self):
        task_id = input("\nВведите ID задачи: ")
        task = self._current_project.find_task(task_id)

        if not task:
            print("Задача не найдена")
            return

        print("\nВыберите новый приоритет:")
        for i, priority in enumerate(Priority, 1):
            print(f"{i}. {priority.get_display_name()}")

        priority_choice = int(input("Введите выбор: "))
        new_priority = list(Priority)[priority_choice - 1]

        task.set_priority(new_priority)

    def _assign_task(self):
        task_id = input("\nВведите ID задачи: ")
        member_name = input("Введите имя исполнителя: ")

        self._current_project.assign_task(task_id, member_name)

    def _add_comment(self):
        task_id = input("\nВведите ID задачи: ")
        task = self._current_project.find_task(task_id)

        if not task:
            print("Задача не найдена")
            return

        author = input("Автор комментария: ")
        text = input("Текст комментария: ")

        task.add_comment(author, text)

    def _view_unassigned_tasks(self):
        tasks = self._current_project.get_unassigned_tasks()

        if not tasks:
            print("\n✓ Нет неназначенных задач")
            return

        print("\n=== Неназначенные задачи ===")
        for task in tasks:
            task.display_short()
        print(f"\nВсего: {len(tasks)}")

    def _view_overdue_tasks(self):
        tasks = self._current_project.get_overdue_tasks()

        if not tasks:
            print("\n✓ Нет просроченных задач")
            return

        print("\n⚠️  === Просроченные задачи ===")
        for task in tasks:
            task.display_short()
        print(f"\nВсего: {len(tasks)}")

    def _add_team_member(self):
        name = input("\nИмя члена команды: ")

        print("\nВыберите роль:")
        for i, role in enumerate(Role, 1):
            print(f"{i}. {role.get_display_name()}")

        role_choice = int(input("Введите выбор: "))
        role = list(Role)[role_choice - 1]

        email = input("Email (опционально): ")

        member = TeamMember(name, role, email)
        self._current_project.add_team_member(member)

    def _view_all_members(self):
        self._current_project.display_all_members()

    def _view_member_details(self):
        name = input("\nВведите имя члена команды: ")
        member = self._current_project.find_member(name)

        if member:
            member.display_info()
        else:
            print("Член команды не найден")

    def _view_member_workload(self):
        name = input("\nВведите имя члена команды: ")
        self._current_project.get_member_workload(name)

    def _view_member_tasks(self):
        name = input("\nВведите имя члена команды: ")
        member = self._current_project.find_member(name)

        if not member:
            print("Член команды не найден")
            return

        tasks = member.get_assigned_tasks()

        if not tasks:
            print(f"\nУ {name} нет назначенных задач")
            return

        print(f"\n=== Задачи: {name} ===")
        for task in tasks:
            task.display_short()
        print(f"\nВсего задач: {len(tasks)}")

    def _create_project(self):
        name = input("\nНазвание проекта: ")
        description = input("Описание: ")

        project = Project(name, description)
        self._projects.append(project)
        self._current_project = project

    def _switch_project(self):
        if len(self._projects) == 0:
            print("\nНет доступных проектов")
            return

        print("\n=== Доступные проекты ===")
        for i, project in enumerate(self._projects, 1):
            print(f"{i}. {project.get_project_name()}")

        choice = int(input("\nВыберите проект: "))
        if 1 <= choice <= len(self._projects):
            self._current_project = self._projects[choice - 1]
            print(f"\n✓ Переключено на проект: {self._current_project.get_project_name()}")

    def _view_statistics(self):
        self._current_project.display_statistics()

    def _set_task_deadline(self):
        task_id = input("\nВведите ID задачи: ")
        task = self._current_project.find_task(task_id)

        if not task:
            print("Задача не найдена")
            return

        deadline_str = input("Введите срок (ГГГГ-ММ-ДД): ")
        try:
            deadline = date.fromisoformat(deadline_str)
            task.set_due_date(deadline)
            print(f"\n✓ Срок установлен: {deadline}")
        except ValueError:
            print("Ошибка: Неверный формат даты")

    def _add_tag_to_task(self):
        task_id = input("\nВведите ID задачи: ")
        task = self._current_project.find_task(task_id)

        if not task:
            print("Задача не найдена")
            return

        tag = input("Введите тег: ")
        task.add_tag(tag)

    def _search_by_tag(self):
        tag = input("\nВведите тег для поиска: ")
        tasks = [t for t in self._current_project.get_tasks() if tag in t.get_tags()]

        if not tasks:
            print(f"\nЗадачи с тегом '{tag}' не найдены")
            return

        print(f"\n=== Задачи с тегом '{tag}' ===")
        for task in tasks:
            task.display_short()
        print(f"\nНайдено: {len(tasks)}")

    def _view_tasks_sorted_by_priority(self):
        tasks = self._current_project.get_tasks_sorted_by_priority()

        if not tasks:
            print("\nНет задач")
            return

        print("\n=== Задачи по приоритету (от высокого к низкому) ===")
        for task in tasks:
            task.display_short()

    def _view_tasks_sorted_by_deadline(self):
        tasks = self._current_project.get_tasks_sorted_by_deadline()

        if not tasks:
            print("\nНет задач с установленным сроком")
            return

        print("\n=== Задачи по сроку ===")
        for task in tasks:
            task.display_short()


def main():
    ui = ProjectManagementUI()
    ui.run()


if __name__ == "__main__":
    main()