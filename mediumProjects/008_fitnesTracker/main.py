from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime, date, timedelta
from decimal import Decimal


# Перечисление типов тренировок
class WorkoutType(Enum):
    RUNNING = "Бег"
    CYCLING = "Велосипед"
    SWIMMING = "Плавание"
    STRENGTH = "Силовая"
    YOGA = "Йога"
    WALKING = "Ходьба"

    def __init__(self, display_name):
        self._display_name = display_name

    def get_display_name(self):
        return self._display_name


# Перечисление интенсивности тренировок
class Intensity(Enum):
    LOW = ("Низкая", 1.0)
    MEDIUM = ("Средняя", 1.3)
    HIGH = ("Высокая", 1.6)
    EXTREME = ("Экстремальная", 2.0)

    def __init__(self, display_name, multiplier):
        self._display_name = display_name
        self._multiplier = multiplier

    def get_display_name(self):
        return self._display_name

    def get_multiplier(self):
        return self._multiplier


# Перечисление статусов цели
class GoalStatus(Enum):
    ACTIVE = "Активная"
    COMPLETED = "Завершена"
    FAILED = "Провалена"
    PAUSED = "На паузе"

    def __init__(self, display_name):
        self._display_name = display_name

    def get_display_name(self):
        return self._display_name


# Перечисление типов целей
class GoalType(Enum):
    CALORIES = "Калории"
    DISTANCE = "Дистанция"
    WORKOUTS = "Тренировки"
    WEIGHT_LOSS = "Потеря веса"

    def __init__(self, display_name):
        self._display_name = display_name

    def get_display_name(self):
        return self._display_name


# Абстрактный класс тренировки
class Workout(ABC):
    _workout_counter = 1

    def __init__(self, duration_minutes, intensity=Intensity.MEDIUM, notes=""):
        self._workout_id = f"WRK{Workout._workout_counter}"
        Workout._workout_counter += 1
        self._date = datetime.now()
        self._duration_minutes = duration_minutes
        self._intensity = intensity
        self._notes = notes
        self._calories_burned = 0
        self._calculate_calories()

    # Геттеры
    def get_workout_id(self):
        return self._workout_id

    def get_date(self):
        return self._date

    def get_duration_minutes(self):
        return self._duration_minutes

    def get_intensity(self):
        return self._intensity

    def get_notes(self):
        return self._notes

    def get_calories_burned(self):
        return self._calories_burned

    # Сеттеры
    def set_notes(self, notes):
        self._notes = notes

    # Абстрактные методы
    @abstractmethod
    def get_workout_type(self):
        pass

    @abstractmethod
    def get_base_calories_per_minute(self):
        pass

    @abstractmethod
    def get_specific_details(self):
        pass

    # Метод расчета калорий
    def _calculate_calories(self):
        base_calories = self.get_base_calories_per_minute() * self._duration_minutes
        intensity_multiplier = self._intensity.get_multiplier()
        self._calories_burned = int(base_calories * intensity_multiplier)

    # Метод отображения информации о тренировке
    def display_info(self):
        print("\n=== Информация о тренировке ===")
        print(f"ID тренировки: {self._workout_id}")
        print(f"Тип: {self.get_workout_type().get_display_name()}")
        print(f"Дата: {self._date.strftime('%Y-%m-%d %H:%M')}")
        print(f"Продолжительность: {self._duration_minutes} минут")
        print(f"Интенсивность: {self._intensity.get_display_name()}")
        print(f"Сожжено калорий: {self._calories_burned}")

        specific = self.get_specific_details()
        if specific:
            print(specific)

        if self._notes:
            print(f"Заметки: {self._notes}")

        print("---")

    # Метод краткого отображения тренировки
    def display_short(self):
        print(f"[{self._workout_id}] {self._date.strftime('%Y-%m-%d')} | "
              f"{self.get_workout_type().get_display_name():12} | "
              f"{self._duration_minutes:>3} мин | {self._calories_burned:>4} ккал | "
              f"{self._intensity.get_display_name()}")


# Класс бега
class Running(Workout):
    def __init__(self, duration_minutes, distance_km, intensity=Intensity.MEDIUM, notes=""):
        self._distance_km = distance_km
        super().__init__(duration_minutes, intensity, notes)
        self._average_pace = self._calculate_pace()

    def get_distance_km(self):
        return self._distance_km

    def get_average_pace(self):
        return self._average_pace

    def get_workout_type(self):
        return WorkoutType.RUNNING

    def get_base_calories_per_minute(self):
        return 10.0  # базовые калории в минуту

    def _calculate_pace(self):
        # Минут на километр
        if self._distance_km > 0:
            return self._duration_minutes / self._distance_km
        return 0

    def get_specific_details(self):
        return (f"Дистанция: {self._distance_km:.2f} км | "
                f"Средний темп: {self._average_pace:.2f} мин/км")


# Класс велосипеда
class Cycling(Workout):
    def __init__(self, duration_minutes, distance_km, terrain="Ровная дорога",
                 intensity=Intensity.MEDIUM, notes=""):
        self._distance_km = distance_km
        self._terrain = terrain
        super().__init__(duration_minutes, intensity, notes)
        self._average_speed = self._calculate_speed()

    def get_distance_km(self):
        return self._distance_km

    def get_terrain(self):
        return self._terrain

    def get_average_speed(self):
        return self._average_speed

    def get_workout_type(self):
        return WorkoutType.CYCLING

    def get_base_calories_per_minute(self):
        return 8.0  # базовые калории в минуту

    def _calculate_speed(self):
        # Километров в час
        if self._duration_minutes > 0:
            return (self._distance_km / self._duration_minutes) * 60
        return 0

    def get_specific_details(self):
        return (f"Дистанция: {self._distance_km:.2f} км | "
                f"Средняя скорость: {self._average_speed:.2f} км/ч | "
                f"Местность: {self._terrain}")


# Класс плавания
class Swimming(Workout):
    def __init__(self, duration_minutes, distance_meters, style="Вольный стиль",
                 intensity=Intensity.MEDIUM, notes=""):
        self._distance_meters = distance_meters
        self._style = style
        super().__init__(duration_minutes, intensity, notes)
        self._average_pace = self._calculate_pace()

    def get_distance_meters(self):
        return self._distance_meters

    def get_style(self):
        return self._style

    def get_average_pace(self):
        return self._average_pace

    def get_workout_type(self):
        return WorkoutType.SWIMMING

    def get_base_calories_per_minute(self):
        return 12.0  # базовые калории в минуту

    def _calculate_pace(self):
        # Минут на 100 метров
        if self._distance_meters > 0:
            return (self._duration_minutes / self._distance_meters) * 100
        return 0

    def get_specific_details(self):
        return (f"Дистанция: {self._distance_meters} м | "
                f"Средний темп: {self._average_pace:.2f} мин/100м | "
                f"Стиль: {self._style}")


# Класс силовой тренировки
class StrengthTraining(Workout):
    def __init__(self, duration_minutes, exercises_count, total_weight_kg=0,
                 intensity=Intensity.HIGH, notes=""):
        self._exercises_count = exercises_count
        self._total_weight_kg = total_weight_kg
        super().__init__(duration_minutes, intensity, notes)

    def get_exercises_count(self):
        return self._exercises_count

    def get_total_weight_kg(self):
        return self._total_weight_kg

    def get_workout_type(self):
        return WorkoutType.STRENGTH

    def get_base_calories_per_minute(self):
        return 7.0  # базовые калории в минуту

    def get_specific_details(self):
        return (f"Упражнений: {self._exercises_count} | "
                f"Общий вес: {self._total_weight_kg} кг")


# Класс цели
class Goal:
    _goal_counter = 1

    def __init__(self, goal_type, target_value, deadline, description=""):
        self._goal_id = f"GOAL{Goal._goal_counter}"
        Goal._goal_counter += 1
        self._goal_type = goal_type
        self._target_value = target_value
        self._current_value = 0
        self._deadline = deadline
        self._description = description
        self._status = GoalStatus.ACTIVE
        self._created_date = date.today()
        self._completed_date = None

    # Геттеры
    def get_goal_id(self):
        return self._goal_id

    def get_goal_type(self):
        return self._goal_type

    def get_target_value(self):
        return self._target_value

    def get_current_value(self):
        return self._current_value

    def get_deadline(self):
        return self._deadline

    def get_description(self):
        return self._description

    def get_status(self):
        return self._status

    def get_created_date(self):
        return self._created_date

    def get_completed_date(self):
        return self._completed_date

    # Сеттеры
    def set_current_value(self, value):
        self._current_value = value
        self._check_completion()

    def set_status(self, status):
        self._status = status

    # Метод обновления прогресса
    def update_progress(self, value):
        self._current_value += value
        self._check_completion()

    # Метод проверки завершения цели
    def _check_completion(self):
        if self._current_value >= self._target_value:
            self._status = GoalStatus.COMPLETED
            self._completed_date = date.today()
            print(f"\n🎉 Поздравляем! Цель '{self._description}' достигнута!")

    # Метод расчета прогресса в процентах
    def calculate_progress_percentage(self):
        if self._target_value == 0:
            return 0
        return min(100, (self._current_value / self._target_value) * 100)

    # Метод расчета оставшихся дней
    def days_remaining(self):
        if self._deadline:
            delta = self._deadline - date.today()
            return delta.days
        return None

    # Метод проверки просрочки
    def is_overdue(self):
        if self._deadline and self._status == GoalStatus.ACTIVE:
            return date.today() > self._deadline
        return False

    # Метод отображения информации о цели
    def display_info(self):
        print("\n=== Информация о цели ===")
        print(f"ID цели: {self._goal_id}")
        print(f"Тип: {self._goal_type.get_display_name()}")
        print(f"Описание: {self._description}")
        print(f"Цель: {self._target_value}")
        print(f"Текущее значение: {self._current_value}")
        print(f"Прогресс: {self.calculate_progress_percentage():.1f}%")
        print(f"Статус: {self._status.get_display_name()}")
        print(f"Создана: {self._created_date}")

        if self._deadline:
            print(f"Крайний срок: {self._deadline}")
            days = self.days_remaining()
            if days is not None:
                if days > 0:
                    print(f"Осталось дней: {days}")
                elif days == 0:
                    print("Крайний срок сегодня!")
                else:
                    print(f"Просрочено на {abs(days)} дней")

        if self._completed_date:
            print(f"Завершена: {self._completed_date}")

        print("---")

    # Метод краткого отображения цели
    def display_short(self):
        status_symbol = {
            GoalStatus.ACTIVE: "🎯",
            GoalStatus.COMPLETED: "✅",
            GoalStatus.FAILED: "❌",
            GoalStatus.PAUSED: "⏸️"
        }
        symbol = status_symbol.get(self._status, "?")

        progress = self.calculate_progress_percentage()
        bar_length = 20
        filled = int(bar_length * progress / 100)
        bar = "█" * filled + "░" * (bar_length - filled)

        print(f"[{symbol}] {self._goal_id} | {self._goal_type.get_display_name():12} | "
              f"[{bar}] {progress:>5.1f}% | {self._current_value}/{self._target_value}")


# Класс пользователя
class User:
    def __init__(self, name, age, weight_kg, height_cm, gender="Мужской"):
        self._name = name
        self._age = age
        self._weight_kg = weight_kg
        self._height_cm = height_cm
        self._gender = gender
        self._workouts = []
        self._goals = []
        self._registration_date = date.today()
        self._weight_history = [(date.today(), weight_kg)]

    # Геттеры
    def get_name(self):
        return self._name

    def get_age(self):
        return self._age

    def get_weight_kg(self):
        return self._weight_kg

    def get_height_cm(self):
        return self._height_cm

    def get_gender(self):
        return self._gender

    def get_workouts(self):
        return self._workouts

    def get_goals(self):
        return self._goals

    def get_registration_date(self):
        return self._registration_date

    # Сеттеры
    def set_weight_kg(self, weight):
        self._weight_kg = weight
        self._weight_history.append((date.today(), weight))

    def set_age(self, age):
        self._age = age

    # Метод добавления тренировки
    def add_workout(self, workout):
        self._workouts.append(workout)

        # Обновление прогресса целей
        self._update_goals_progress(workout)

        print(f"\n✓ Тренировка добавлена: {workout.get_workout_type().get_display_name()}")
        print(f"Сожжено калорий: {workout.get_calories_burned()}")

    # Метод обновления прогресса целей
    def _update_goals_progress(self, workout):
        for goal in self._goals:
            if goal.get_status() != GoalStatus.ACTIVE:
                continue

            if goal.get_goal_type() == GoalType.CALORIES:
                goal.update_progress(workout.get_calories_burned())
            elif goal.get_goal_type() == GoalType.WORKOUTS:
                goal.update_progress(1)
            elif goal.get_goal_type() == GoalType.DISTANCE:
                if hasattr(workout, 'get_distance_km'):
                    goal.update_progress(workout.get_distance_km())

    # Метод добавления цели
    def add_goal(self, goal):
        self._goals.append(goal)
        print(f"\n✓ Цель добавлена: {goal.get_description()}")

    # Метод расчета общих сожженных калорий
    def calculate_total_calories(self, days=None):
        if days:
            cutoff_date = datetime.now() - timedelta(days=days)
            workouts = [w for w in self._workouts if w.get_date() >= cutoff_date]
        else:
            workouts = self._workouts

        return sum(w.get_calories_burned() for w in workouts)

    # Метод расчета общей дистанции
    def calculate_total_distance(self, workout_type=None, days=None):
        if days:
            cutoff_date = datetime.now() - timedelta(days=days)
            workouts = [w for w in self._workouts if w.get_date() >= cutoff_date]
        else:
            workouts = self._workouts

        if workout_type:
            workouts = [w for w in workouts if w.get_workout_type() == workout_type]

        total = 0
        for workout in workouts:
            if hasattr(workout, 'get_distance_km'):
                total += workout.get_distance_km()
            elif hasattr(workout, 'get_distance_meters'):
                total += workout.get_distance_meters() / 1000

        return total

    # Метод расчета ИМТ (индекс массы тела)
    def calculate_bmi(self):
        height_m = self._height_cm / 100
        bmi = self._weight_kg / (height_m ** 2)
        return bmi

    # Метод получения категории ИМТ
    def get_bmi_category(self):
        bmi = self.calculate_bmi()

        if bmi < 18.5:
            return "Недостаточный вес"
        elif 18.5 <= bmi < 25:
            return "Нормальный вес"
        elif 25 <= bmi < 30:
            return "Избыточный вес"
        else:
            return "Ожирение"

    # Метод расчета базового метаболизма (BMR)
    def calculate_bmr(self):
        # Формула Миффлина-Сан Жеора
        if self._gender == "Мужской":
            bmr = 10 * self._weight_kg + 6.25 * self._height_cm - 5 * self._age + 5
        else:
            bmr = 10 * self._weight_kg + 6.25 * self._height_cm - 5 * self._age - 161

        return bmr

    # Метод расчета рекомендуемых калорий
    def calculate_recommended_calories(self, activity_level="Умеренная"):
        bmr = self.calculate_bmr()

        activity_multipliers = {
            "Минимальная": 1.2,
            "Низкая": 1.375,
            "Умеренная": 1.55,
            "Высокая": 1.725,
            "Очень высокая": 1.9
        }

        multiplier = activity_multipliers.get(activity_level, 1.55)
        return bmr * multiplier

    # Метод получения тренировок за период
    def get_workouts_by_period(self, days):
        cutoff_date = datetime.now() - timedelta(days=days)
        return [w for w in self._workouts if w.get_date() >= cutoff_date]

    # Метод получения активных целей
    def get_active_goals(self):
        return [g for g in self._goals if g.get_status() == GoalStatus.ACTIVE]

    # Метод проверки прогресса целей
    def check_goals_progress(self):
        active_goals = self.get_active_goals()

        if not active_goals:
            print("\nУ вас нет активных целей")
            return

        print("\n=== Прогресс целей ===")
        for goal in active_goals:
            goal.display_short()

            # Проверка просрочки
            if goal.is_overdue():
                print("  ⚠️  ПРОСРОЧЕНО!")

    # Метод отображения информации о пользователе
    def display_info(self):
        print("\n=== Профиль пользователя ===")
        print(f"Имя: {self._name}")
        print(f"Возраст: {self._age} лет")
        print(f"Пол: {self._gender}")
        print(f"Вес: {self._weight_kg} кг")
        print(f"Рост: {self._height_cm} см")

        bmi = self.calculate_bmi()
        print(f"\nИМТ: {bmi:.1f} ({self.get_bmi_category()})")
        print(f"Базовый метаболизм: {self.calculate_bmr():.0f} ккал/день")

        print(f"\nДата регистрации: {self._registration_date}")
        print(f"Всего тренировок: {len(self._workouts)}")
        print(f"Активных целей: {len(self.get_active_goals())}")
        print(f"Всего сожжено калорий: {self.calculate_total_calories()} ккал")

        print("---")

    # Метод отображения статистики
    def display_statistics(self, days=30):
        print(f"\n=== Статистика за последние {days} дней ===")

        workouts = self.get_workouts_by_period(days)
        total_workouts = len(workouts)

        if total_workouts == 0:
            print("Нет тренировок за указанный период")
            return

        total_calories = sum(w.get_calories_burned() for w in workouts)
        total_duration = sum(w.get_duration_minutes() for w in workouts)

        print(f"Всего тренировок: {total_workouts}")
        print(f"Общее время: {total_duration} минут ({total_duration / 60:.1f} часов)")
        print(f"Сожжено калорий: {total_calories} ккал")
        print(f"Среднее за тренировку: {total_calories / total_workouts:.0f} ккал")

        # Статистика по типам тренировок
        workout_types = {}
        for workout in workouts:
            w_type = workout.get_workout_type().get_display_name()
            if w_type not in workout_types:
                workout_types[w_type] = {'count': 0, 'calories': 0, 'duration': 0}
            workout_types[w_type]['count'] += 1
            workout_types[w_type]['calories'] += workout.get_calories_burned()
            workout_types[w_type]['duration'] += workout.get_duration_minutes()

        print("\nПо типам тренировок:")
        for w_type, stats in workout_types.items():
            print(f"  {w_type}: {stats['count']} тренировок, "
                  f"{stats['calories']} ккал, {stats['duration']} мин")

        # Общая дистанция
        total_distance = self.calculate_total_distance(days=days)
        if total_distance > 0:
            print(f"\nОбщая дистанция: {total_distance:.2f} км")


# Класс плана тренировок
class WorkoutPlan:
    def __init__(self, name, description, duration_weeks):
        self._plan_id = f"PLAN{id(self)}"
        self._name = name
        self._description = description
        self._duration_weeks = duration_weeks
        self._scheduled_workouts = []
        self._created_date = date.today()

    # Геттеры
    def get_plan_id(self):
        return self._plan_id

    def get_name(self):
        return self._name

    def get_description(self):
        return self._description

    def get_duration_weeks(self):
        return self._duration_weeks

    def get_scheduled_workouts(self):
        return self._scheduled_workouts

    # Метод добавления запланированной тренировки
    def add_scheduled_workout(self, workout_type, day_of_week, duration, notes=""):
        scheduled = {
            'type': workout_type,
            'day': day_of_week,
            'duration': duration,
            'notes': notes
        }
        self._scheduled_workouts.append(scheduled)
        print(f"\n✓ Тренировка добавлена в план: {workout_type.get_display_name()} на {day_of_week}")

    # Метод отображения информации о плане
    def display_info(self):
        print("\n=== План тренировок ===")
        print(f"Название: {self._name}")
        print(f"Описание: {self._description}")
        print(f"Длительность: {self._duration_weeks} недель")
        print(f"Создан: {self._created_date}")

        if self._scheduled_workouts:
            print(f"\nЗапланировано тренировок: {len(self._scheduled_workouts)}")
            for i, workout in enumerate(self._scheduled_workouts, 1):
                print(f"{i}. {workout['day']} - {workout['type'].get_display_name()} "
                      f"({workout['duration']} мин)")
                if workout['notes']:
                    print(f"   Заметка: {workout['notes']}")

        print("---")


# Класс фитнес-трекера
class FitnessTracker:
    def __init__(self):
        self._users = []
        self._workout_plans = []

    # Метод добавления пользователя
    def add_user(self, user):
        self._users.append(user)
        print(f"\n✓ Пользователь зарегистрирован: {user.get_name()}")
        return user

    # Метод добавления плана тренировок
    def add_workout_plan(self, plan):
        self._workout_plans.append(plan)
        print(f"\n✓ План тренировок добавлен: {plan.get_name()}")

    # Метод получения статистики системы
    def display_system_statistics(self):
        total_users = len(self._users)
        total_workouts = sum(len(u.get_workouts()) for u in self._users)
        total_calories = sum(u.calculate_total_calories() for u in self._users)

        print("\n=== Статистика системы ===")
        print(f"Всего пользователей: {total_users}")
        print(f"Всего тренировок: {total_workouts}")
        print(f"Всего сожжено калорий: {total_calories} ккал")
        print(f"Доступно планов тренировок: {len(self._workout_plans)}")


# Класс пользовательского интерфейса
class FitnessTrackerUI:
    def __init__(self):
        self._tracker = FitnessTracker()
        self._current_user = None
        self._initialize_sample_data()

    # Инициализация примерных данных
    def _initialize_sample_data(self):
        # Создание примерного пользователя
        user = User("Иван Иванов", 30, 80, 180, "Мужской")
        self._tracker.add_user(user)
        self._current_user = user

        # Добавление примерных тренировок
        user.add_workout(Running(45, 8.5, Intensity.MEDIUM, "Утренняя пробежка"))
        user.add_workout(Cycling(60, 25, "Парк", Intensity.HIGH))

        # Добавление примерной цели
        deadline = date.today() + timedelta(days=30)
        goal = Goal(GoalType.CALORIES, 10000, deadline, "Сжечь 10000 калорий за месяц")
        user.add_goal(goal)

    def run(self):
        print("╔════════════════════════════════════════╗")
        print("║             Фитнес-Трекер              ║")
        print("╚════════════════════════════════════════╝\n")

        while True:
            try:
                self._display_main_menu()
                choice = int(input())

                if choice == 20:
                    print("\nБудьте здоровы!")
                    break

                self._handle_menu_choice(choice)

            except Exception:
                print("\nОшибка: Неверный ввод. Попробуйте снова.")

    # Отображение главного меню
    def _display_main_menu(self):
        print("\n=== Главное меню ===")
        if self._current_user:
            print(f"Текущий пользователь: {self._current_user.get_name()}")

        print("\n1. Просмотреть профиль")
        print("2. Добавить тренировку")
        print("3. Просмотреть все тренировки")
        print("4. Просмотреть статистику")
        print("5. Рассчитать ИМТ")
        print("6. Добавить цель")
        print("7. Просмотреть цели")
        print("8. Проверить прогресс целей")
        print("9. Обновить вес")
        print("10. Рассчитать рекомендуемые калории")
        print("11. Просмотреть тренировки за период")
        print("12. Создать план тренировок")
        print("13. Просмотреть планы тренировок")
        print("14. Добавить тренировку в план")
        print("15. Просмотреть детали тренировки")
        print("16. Просмотреть детали цели")
        print("17. Общая дистанция")
        print("18. Изменить статус цели")
        print("19. Статистика системы")
        print("20. Выход")
        print("Введите выбор (1-20): ", end='')

    # Обработка выбора меню
    def _handle_menu_choice(self, choice):
        if not self._current_user and choice not in [19, 20]:
            print("Ошибка: Пользователь не выбран")
            return

        actions = {
            1: self._view_profile,
            2: self._add_workout,
            3: self._view_all_workouts,
            4: self._view_statistics,
            5: self._calculate_bmi,
            6: self._add_goal,
            7: self._view_goals,
            8: self._check_goals_progress,
            9: self._update_weight,
            10: self._calculate_recommended_calories,
            11: self._view_workouts_period,
            12: self._create_workout_plan,
            13: self._view_workout_plans,
            14: self._add_workout_to_plan,
            15: self._view_workout_details,
            16: self._view_goal_details,
            17: self._view_total_distance,
            18: self._change_goal_status,
            19: self._tracker.display_system_statistics
        }

        if choice in actions:
            actions[choice]()
        else:
            print("Неверный выбор. Попробуйте снова.")

    def _view_profile(self):
        self._current_user.display_info()

    def _add_workout(self):
        print("\nВыберите тип тренировки:")
        print("1. Бег")
        print("2. Велосипед")
        print("3. Плавание")
        print("4. Силовая тренировка")

        workout_type = int(input("Введите выбор (1-4): "))
        duration = int(input("Продолжительность (минуты): "))

        print("\nВыберите интенсивность:")
        for i, intensity in enumerate(Intensity, 1):
            print(f"{i}. {intensity.get_display_name()}")
        intensity_choice = int(input("Введите выбор: "))
        intensity = list(Intensity)[intensity_choice - 1]

        notes = input("Заметки (опционально): ")

        workout = None

        if workout_type == 1:  # Бег
            distance = float(input("Дистанция (км): "))
            workout = Running(duration, distance, intensity, notes)
        elif workout_type == 2:  # Велосипед
            distance = float(input("Дистанция (км): "))
            terrain = input("Местность (опционально): ") or "Ровная дорога"
            workout = Cycling(duration, distance, terrain, intensity, notes)
        elif workout_type == 3:  # Плавание
            distance = int(input("Дистанция (метры): "))
            style = input("Стиль плавания (опционально): ") or "Вольный стиль"
            workout = Swimming(duration, distance, style, intensity, notes)
        elif workout_type == 4:  # Силовая
            exercises = int(input("Количество упражнений: "))
            weight = float(input("Общий вес (кг, опционально): ") or "0")
            workout = StrengthTraining(duration, exercises, weight, intensity, notes)

        if workout:
            self._current_user.add_workout(workout)

    def _view_all_workouts(self):
        workouts = self._current_user.get_workouts()

        if not workouts:
            print("\nНет тренировок")
            return

        print("\n=== Все тренировки ===")
        for workout in reversed(workouts[-20:]):  # Последние 20
            workout.display_short()
        print(f"\nВсего тренировок: {len(workouts)}")

    def _view_statistics(self):
        days = int(input("\nЗа сколько дней показать статистику? "))
        self._current_user.display_statistics(days)

    def _calculate_bmi(self):
        bmi = self._current_user.calculate_bmi()
        category = self._current_user.get_bmi_category()

        print(f"\n=== Индекс Массы Тела (ИМТ) ===")
        print(f"Ваш ИМТ: {bmi:.1f}")
        print(f"Категория: {category}")

        print("\nРекомендации:")
        if bmi < 18.5:
            print("Рекомендуется набрать вес")
        elif 18.5 <= bmi < 25:
            print("У вас нормальный вес")
        elif 25 <= bmi < 30:
            print("Рекомендуется снизить вес")
        else:
            print("Необходимо снизить вес. Проконсультируйтесь с врачом")

    def _add_goal(self):
        print("\nВыберите тип цели:")
        for i, goal_type in enumerate(GoalType, 1):
            print(f"{i}. {goal_type.get_display_name()}")

        type_choice = int(input("Введите выбор: "))
        goal_type = list(GoalType)[type_choice - 1]

        target = float(input(f"Целевое значение ({goal_type.get_display_name()}): "))
        description = input("Описание цели: ")

        deadline_str = input("Крайний срок (ГГГГ-ММ-ДД) или Enter для пропуска: ")
        deadline = date.fromisoformat(deadline_str) if deadline_str.strip() else None

        goal = Goal(goal_type, target, deadline, description)
        self._current_user.add_goal(goal)

    def _view_goals(self):
        goals = self._current_user.get_goals()

        if not goals:
            print("\nНет целей")
            return

        print("\n=== Все цели ===")
        for goal in goals:
            goal.display_short()

    def _check_goals_progress(self):
        self._current_user.check_goals_progress()

    def _update_weight(self):
        new_weight = float(input("\nВведите новый вес (кг): "))
        old_weight = self._current_user.get_weight_kg()
        self._current_user.set_weight_kg(new_weight)

        difference = new_weight - old_weight
        print(f"\n✓ Вес обновлен: {old_weight} кг → {new_weight} кг")

        if difference > 0:
            print(f"Набрано: +{difference:.1f} кг")
        elif difference < 0:
            print(f"Потеряно: {abs(difference):.1f} кг")

    def _calculate_recommended_calories(self):
        print("\nВыберите уровень активности:")
        print("1. Минимальная (сидячий образ жизни)")
        print("2. Низкая (легкие упражнения 1-3 раза в неделю)")
        print("3. Умеренная (умеренные упражнения 3-5 раз в неделю)")
        print("4. Высокая (интенсивные упражнения 6-7 раз в неделю)")
        print("5. Очень высокая (очень интенсивные упражнения, физическая работа)")

        levels = ["Минимальная", "Низкая", "Умеренная", "Высокая", "Очень высокая"]
        choice = int(input("Введите выбор (1-5): "))

        if 1 <= choice <= 5:
            level = levels[choice - 1]
            calories = self._current_user.calculate_recommended_calories(level)
            bmr = self._current_user.calculate_bmr()

            print(f"\n=== Рекомендуемые калории ===")
            print(f"Базовый метаболизм (BMR): {bmr:.0f} ккал/день")
            print(f"Рекомендуемые калории ({level}): {calories:.0f} ккал/день")

    def _view_workouts_period(self):
        days = int(input("\nЗа сколько дней показать тренировки? "))
        workouts = self._current_user.get_workouts_by_period(days)

        if not workouts:
            print(f"\nНет тренировок за последние {days} дней")
            return

        print(f"\n=== Тренировки за последние {days} дней ===")
        for workout in reversed(workouts):
            workout.display_short()
        print(f"\nВсего тренировок: {len(workouts)}")

    def _create_workout_plan(self):
        name = input("\nНазвание плана: ")
        description = input("Описание: ")
        duration = int(input("Длительность (недели): "))

        plan = WorkoutPlan(name, description, duration)
        self._tracker.add_workout_plan(plan)

    def _view_workout_plans(self):
        plans = self._tracker._workout_plans

        if not plans:
            print("\nНет планов тренировок")
            return

        print("\n=== Планы тренировок ===")
        for i, plan in enumerate(plans, 1):
            print(f"{i}. {plan.get_name()} ({plan.get_duration_weeks()} недель)")

    def _add_workout_to_plan(self):
        plans = self._tracker._workout_plans

        if not plans:
            print("\nНет планов тренировок")
            return

        self._view_workout_plans()
        plan_idx = int(input("\nВыберите план: ")) - 1

        if 0 <= plan_idx < len(plans):
            plan = plans[plan_idx]

            print("\nВыберите тип тренировки:")
            for i, w_type in enumerate(WorkoutType, 1):
                print(f"{i}. {w_type.get_display_name()}")

            type_choice = int(input("Введите выбор: "))
            workout_type = list(WorkoutType)[type_choice - 1]

            day = input("День недели: ")
            duration = int(input("Продолжительность (минуты): "))
            notes = input("Заметки (опционально): ")

            plan.add_scheduled_workout(workout_type, day, duration, notes)

    def _view_workout_details(self):
        workouts = self._current_user.get_workouts()

        if not workouts:
            print("\nНет тренировок")
            return

        self._view_all_workouts()
        workout_id = input("\nВведите ID тренировки: ")

        for workout in workouts:
            if workout.get_workout_id() == workout_id:
                workout.display_info()
                return

        print("Тренировка не найдена")

    def _view_goal_details(self):
        goals = self._current_user.get_goals()

        if not goals:
            print("\nНет целей")
            return

        self._view_goals()
        goal_id = input("\nВведите ID цели: ")

        for goal in goals:
            if goal.get_goal_id() == goal_id:
                goal.display_info()
                return

        print("Цель не найдена")

    def _view_total_distance(self):
        days = int(input("\nЗа сколько дней показать дистанцию? "))
        total = self._current_user.calculate_total_distance(days=days)

        print(f"\n=== Общая дистанция за {days} дней ===")
        print(f"Всего: {total:.2f} км")

    def _change_goal_status(self):
        goals = self._current_user.get_goals()

        if not goals:
            print("\nНет целей")
            return

        self._view_goals()
        goal_id = input("\nВведите ID цели: ")

        for goal in goals:
            if goal.get_goal_id() == goal_id:
                print("\nВыберите новый статус:")
                for i, status in enumerate(GoalStatus, 1):
                    print(f"{i}. {status.get_display_name()}")

                status_choice = int(input("Введите выбор: "))
                new_status = list(GoalStatus)[status_choice - 1]

                goal.set_status(new_status)
                print(f"\n✓ Статус цели обновлен на {new_status.get_display_name()}")
                return

        print("Цель не найдена")


def main():
    ui = FitnessTrackerUI()
    ui.run()


if __name__ == "__main__":
    main()