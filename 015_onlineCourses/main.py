from enum import Enum
from datetime import date


# Перечисление уровней сложности курса
class CourseLevel(Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4


# Перечисление статусов курса
class CourseStatus(Enum):
    ACTIVE = 1
    FULL = 2
    COMPLETED = 3
    CANCELLED = 4


# Перечисление статусов студента на курсе
class EnrollmentStatus(Enum):
    ENROLLED = 1
    COMPLETED = 2
    DROPPED = 3
    FAILED = 4


# Класс записи на курс
class Enrollment:
    def __init__(self, student, course):
        self._student = student
        self._course = course
        self._enrollment_date = date.today()
        self._completion_date = None
        self._status = EnrollmentStatus.ENROLLED
        self._grade = None
        self._progress = 0.0

    # Геттеры
    def get_student(self):
        return self._student

    def get_course(self):
        return self._course

    def get_enrollment_date(self):
        return self._enrollment_date

    def get_completion_date(self):
        return self._completion_date

    def get_status(self):
        return self._status

    def get_grade(self):
        return self._grade

    def get_progress(self):
        return self._progress

    # Сеттеры
    def set_status(self, status):
        self._status = status

    def set_grade(self, grade):
        self._grade = grade

    def set_progress(self, progress):
        self._progress = min(100.0, max(0.0, progress))

    # Метод завершения курса
    def complete(self, grade):
        self._status = EnrollmentStatus.COMPLETED
        self._completion_date = date.today()
        self._grade = grade
        self._progress = 100.0

    # Метод отображения информации
    def display_info(self):
        print(f"\nStudent: {self._student.get_name()}")
        print(f"Course: {self._course.get_title()}")
        print(f"Enrollment Date: {self._enrollment_date}")
        print(f"Status: {self._status.name}")
        print(f"Progress: {self._progress:.1f}%")
        if self._grade is not None:
            print(f"Grade: {self._grade}")
        if self._completion_date:
            print(f"Completion Date: {self._completion_date}")


# Класс курса
class Course:
    _course_counter = 1000

    def __init__(self, title, instructor, max_students, level, duration_weeks, price):
        self._course_id = Course._course_counter
        Course._course_counter += 1
        self._title = title
        self._instructor = instructor
        self._max_students = max_students
        self._enrolled_students = []
        self._level = level
        self._duration_weeks = duration_weeks
        self._price = price
        self._status = CourseStatus.ACTIVE
        self._description = ""
        self._start_date = None

    # Геттеры
    def get_course_id(self):
        return self._course_id

    def get_title(self):
        return self._title

    def get_instructor(self):
        return self._instructor

    def get_max_students(self):
        return self._max_students

    def get_enrolled_students(self):
        return self._enrolled_students

    def get_level(self):
        return self._level

    def get_duration_weeks(self):
        return self._duration_weeks

    def get_price(self):
        return self._price

    def get_status(self):
        return self._status

    def get_description(self):
        return self._description

    def get_start_date(self):
        return self._start_date

    # Сеттеры
    def set_description(self, description):
        self._description = description

    def set_start_date(self, start_date):
        self._start_date = start_date

    def set_status(self, status):
        self._status = status

    # Метод проверки заполненности курса
    def is_full(self):
        return len(self._enrolled_students) >= self._max_students

    # Метод получения количества записанных студентов
    def get_enrollment_count(self):
        return len(self._enrolled_students)

    # Метод получения количества свободных мест
    def get_available_seats(self):
        return self._max_students - len(self._enrolled_students)

    # Метод добавления студента
    def add_student(self, student):
        if student not in self._enrolled_students:
            self._enrolled_students.append(student)
            if self.is_full():
                self._status = CourseStatus.FULL

    # Метод удаления студента
    def remove_student(self, student):
        if student in self._enrolled_students:
            self._enrolled_students.remove(student)
            if self._status == CourseStatus.FULL and not self.is_full():
                self._status = CourseStatus.ACTIVE

    # Метод получения списка студентов (roster)
    def get_course_roster(self):
        return self._enrolled_students.copy()

    # Метод отображения информации о курсе
    def display_info(self):
        print("\n=== Course Information ===")
        print(f"Course ID: {self._course_id}")
        print(f"Title: {self._title}")
        print(f"Instructor: {self._instructor}")
        print(f"Level: {self._level.name}")
        print(f"Duration: {self._duration_weeks} weeks")
        print(f"Price: ${self._price:.2f}")
        print(f"Status: {self._status.name}")
        print(f"Enrolled: {self.get_enrollment_count()}/{self._max_students} students")
        print(f"Available Seats: {self.get_available_seats()}")
        if self._description:
            print(f"Description: {self._description}")
        if self._start_date:
            print(f"Start Date: {self._start_date}")
        print("---")

    # Метод краткого отображения курса
    def display_short(self):
        status_symbol = "✓" if self._status == CourseStatus.ACTIVE else (
            "✗" if self._status == CourseStatus.FULL else "◉")
        print(f"[{status_symbol}] Course #{self._course_id} | {self._title} | {self._instructor} | "
              f"{self._level.name} | {self.get_enrollment_count()}/{self._max_students} students | ${self._price:.2f}")


# Класс студента
class Student:
    _student_counter = 1

    def __init__(self, name, email, phone):
        self._student_id = Student._student_counter
        Student._student_counter += 1
        self._name = name
        self._email = email
        self._phone = phone
        self._enrolled_courses = []
        self._completed_courses = []
        self._registration_date = date.today()

    # Геттеры
    def get_student_id(self):
        return self._student_id

    def get_name(self):
        return self._name

    def get_email(self):
        return self._email

    def get_phone(self):
        return self._phone

    def get_enrolled_courses(self):
        return self._enrolled_courses

    def get_completed_courses(self):
        return self._completed_courses

    def get_registration_date(self):
        return self._registration_date

    # Метод добавления курса
    def add_course(self, course):
        if course not in self._enrolled_courses:
            self._enrolled_courses.append(course)

    # Метод удаления курса
    def remove_course(self, course):
        if course in self._enrolled_courses:
            self._enrolled_courses.remove(course)

    # Метод завершения курса
    def complete_course(self, course):
        if course in self._enrolled_courses:
            self._enrolled_courses.remove(course)
            if course not in self._completed_courses:
                self._completed_courses.append(course)

    # Метод получения количества активных курсов
    def get_active_course_count(self):
        return len(self._enrolled_courses)

    # Метод получения количества завершенных курсов
    def get_completed_course_count(self):
        return len(self._completed_courses)

    # Метод проверки, записан ли студент на курс
    def is_enrolled_in(self, course):
        return course in self._enrolled_courses

    # Метод отображения информации о студенте
    def display_info(self):
        print("\n=== Student Information ===")
        print(f"Student ID: {self._student_id}")
        print(f"Name: {self._name}")
        print(f"Email: {self._email}")
        print(f"Phone: {self._phone}")
        print(f"Registration Date: {self._registration_date}")
        print(f"Active Courses: {self.get_active_course_count()}")
        print(f"Completed Courses: {self.get_completed_course_count()}")
        print("---")

    # Метод краткого отображения студента
    def display_short(self):
        print(f"Student #{self._student_id} | {self._name} | {self._email} | "
              f"Active: {self.get_active_course_count()} | Completed: {self.get_completed_course_count()}")


# Класс платформы
class Platform:
    def __init__(self, platform_name):
        self._platform_name = platform_name
        self._courses = []
        self._students = []
        self._enrollments = []

    # Метод добавления курса
    def add_course(self, course):
        self._courses.append(course)
        print("\n✓ Course added successfully!")
        print(f"Course ID: {course.get_course_id()}")
        print(f"Title: {course.get_title()}")

    # Метод добавления студента
    def add_student(self, student):
        self._students.append(student)
        print("\n✓ Student registered successfully!")
        print(f"Student ID: {student.get_student_id()}")
        print(f"Name: {student.get_name()}")
        return student

    # Метод записи студента на курс
    def enroll_student(self, student, course):
        # Проверка существования студента и курса
        if student not in self._students:
            print("Error: Student not registered in the platform")
            return False

        if course not in self._courses:
            print("Error: Course not found in the platform")
            return False

        # Проверка, не записан ли уже студент на этот курс
        if student.is_enrolled_in(course):
            print("Error: Student is already enrolled in this course")
            return False

        # Проверка заполненности курса
        if course.is_full():
            print("Error: Course is full")
            print(f"Maximum students: {course.get_max_students()}")
            return False

        # Проверка статуса курса
        if course.get_status() not in [CourseStatus.ACTIVE, CourseStatus.FULL]:
            print(f"Error: Course is not available for enrollment (Status: {course.get_status().name})")
            return False

        # Создание записи на курс (двусторонняя связь)
        enrollment = Enrollment(student, course)
        self._enrollments.append(enrollment)

        student.add_course(course)
        course.add_student(student)

        print("\n✓ Student enrolled successfully!")
        print(f"Student: {student.get_name()}")
        print(f"Course: {course.get_title()}")
        print(f"Enrollment Date: {enrollment.get_enrollment_date()}")
        print(f"Price: ${course.get_price():.2f}")

        return True

    # Метод отчисления студента с курса
    def drop_course(self, student, course):
        # Проверка, записан ли студент на курс
        if not student.is_enrolled_in(course):
            print("Error: Student is not enrolled in this course")
            return False

        # Поиск записи
        enrollment = self._find_enrollment(student, course)
        if enrollment:
            enrollment.set_status(EnrollmentStatus.DROPPED)

        # Удаление двусторонней связи
        student.remove_course(course)
        course.remove_student(student)

        print("\n✓ Student dropped from course successfully!")
        print(f"Student: {student.get_name()}")
        print(f"Course: {course.get_title()}")

        return True

    # Метод завершения курса студентом
    def complete_course(self, student, course, grade):
        # Проверка, записан ли студент на курс
        if not student.is_enrolled_in(course):
            print("Error: Student is not enrolled in this course")
            return False

        # Поиск записи
        enrollment = self._find_enrollment(student, course)
        if enrollment:
            enrollment.complete(grade)

        # Обновление данных студента
        student.complete_course(course)

        print("\n✓ Course completed successfully!")
        print(f"Student: {student.get_name()}")
        print(f"Course: {course.get_title()}")
        print(f"Grade: {grade}")

        return True

    # Метод получения курсов студента
    def get_student_courses(self, student):
        return student.get_enrolled_courses()

    # Метод получения завершенных курсов студента
    def get_student_completed_courses(self, student):
        return student.get_completed_courses()

    # Метод получения всех записей студента
    def get_student_enrollments(self, student):
        return [e for e in self._enrollments if e.get_student() == student]

    # Метод получения списка студентов курса (roster)
    def get_course_roster(self, course):
        return course.get_course_roster()

    # Метод поиска курса по ID
    def find_course_by_id(self, course_id):
        for course in self._courses:
            if course.get_course_id() == course_id:
                return course
        return None

    # Метод поиска студента по ID
    def find_student_by_id(self, student_id):
        for student in self._students:
            if student.get_student_id() == student_id:
                return student
        return None

    # Метод поиска записи
    def _find_enrollment(self, student, course):
        for enrollment in self._enrollments:
            if (enrollment.get_student() == student and
                    enrollment.get_course() == course and
                    enrollment.get_status() == EnrollmentStatus.ENROLLED):
                return enrollment
        return None

    # Метод поиска курсов по уровню
    def get_courses_by_level(self, level):
        return [c for c in self._courses if c.get_level() == level]

    # Метод поиска доступных курсов
    def get_available_courses(self):
        return [c for c in self._courses if c.get_status() == CourseStatus.ACTIVE and not c.is_full()]

    # Метод поиска курсов по инструктору
    def get_courses_by_instructor(self, instructor_name):
        term = instructor_name.lower()
        return [c for c in self._courses if term in c.get_instructor().lower()]

    # Метод отображения всех курсов
    def display_all_courses(self):
        if not self._courses:
            print("\nNo courses available")
            return

        print(f"\n=== {self._platform_name} - All Courses ===")
        for course in self._courses:
            course.display_short()
        print(f"\nTotal courses: {len(self._courses)}")

    # Метод отображения всех студентов
    def display_all_students(self):
        if not self._students:
            print("\nNo students registered")
            return

        print(f"\n=== {self._platform_name} - All Students ===")
        for student in self._students:
            student.display_short()
        print(f"\nTotal students: {len(self._students)}")

    # Метод отображения студентов курса
    def display_course_students(self, course):
        students = self.get_course_roster(course)

        if not students:
            print("\nNo students enrolled in this course")
            return

        print(f"\n=== Students in {course.get_title()} ===")
        for student in students:
            student.display_short()
        print(f"\nTotal enrolled: {len(students)}")

    # Метод отображения курсов студента
    def display_student_courses(self, student):
        courses = self.get_student_courses(student)

        if not courses:
            print(f"\n{student.get_name()} is not enrolled in any courses")
            return

        print(f"\n=== {student.get_name()}'s Active Courses ===")
        for course in courses:
            course.display_short()
        print(f"\nTotal active courses: {len(courses)}")

    # Метод отображения статистики платформы
    def display_statistics(self):
        total_courses = len(self._courses)
        active_courses = sum(1 for c in self._courses if c.get_status() == CourseStatus.ACTIVE)
        full_courses = sum(1 for c in self._courses if c.get_status() == CourseStatus.FULL)
        total_students = len(self._students)
        total_enrollments = len([e for e in self._enrollments if e.get_status() == EnrollmentStatus.ENROLLED])
        completed_enrollments = len([e for e in self._enrollments if e.get_status() == EnrollmentStatus.COMPLETED])

        # Подсчет по уровням
        beginner_courses = len(self.get_courses_by_level(CourseLevel.BEGINNER))
        intermediate_courses = len(self.get_courses_by_level(CourseLevel.INTERMEDIATE))
        advanced_courses = len(self.get_courses_by_level(CourseLevel.ADVANCED))

        # Расчет общей выручки
        total_revenue = sum(e.get_course().get_price() for e in self._enrollments
                            if e.get_status() in [EnrollmentStatus.ENROLLED, EnrollmentStatus.COMPLETED])

        print(f"\n=== {self._platform_name} Statistics ===")
        print(f"Total Courses: {total_courses}")
        print(f"  Active: {active_courses}")
        print(f"  Full: {full_courses}")

        print("\nCourse Levels:")
        print(f"  Beginner: {beginner_courses}")
        print(f"  Intermediate: {intermediate_courses}")
        print(f"  Advanced: {advanced_courses}")

        print(f"\nTotal Students: {total_students}")
        print(f"Active Enrollments: {total_enrollments}")
        print(f"Completed Enrollments: {completed_enrollments}")

        print(f"\nTotal Revenue: ${total_revenue:.2f}")

        if total_enrollments > 0:
            avg_courses_per_student = total_enrollments / total_students
            print(f"Average Courses per Student: {avg_courses_per_student:.2f}")


# Класс пользовательского интерфейса
class PlatformUI:
    def __init__(self, platform_name):
        self._platform = Platform(platform_name)
        self._initialize_sample_data()

    # Инициализация примерных данных
    def _initialize_sample_data(self):
        # Добавление курсов
        course1 = Course("Python Programming", "Dr. Smith", 30, CourseLevel.BEGINNER, 8, 299.99)
        course1.set_description("Learn Python from scratch")
        self._platform.add_course(course1)

        course2 = Course("Advanced Java", "Prof. Johnson", 25, CourseLevel.ADVANCED, 12, 499.99)
        course2.set_description("Master advanced Java concepts")
        self._platform.add_course(course2)

        course3 = Course("Web Development", "Sarah Williams", 40, CourseLevel.INTERMEDIATE, 10, 399.99)
        course3.set_description("Full-stack web development")
        self._platform.add_course(course3)

        # Добавление студентов
        student1 = Student("John Doe", "john@email.com", "123-456-7890")
        self._platform.add_student(student1)

        student2 = Student("Jane Smith", "jane@email.com", "098-765-4321")
        self._platform.add_student(student2)

    def run(self):
        print("╔════════════════════════════════════════╗")
        print("║  Online Learning Platform              ║")
        print("╚════════════════════════════════════════╝\n")

        while True:
            try:
                self._display_main_menu()
                choice = int(input())

                if choice == 15:
                    print("\nThank you for using the platform!")
                    break

                self._handle_menu_choice(choice)

            except Exception:
                print("\nError: Invalid input. Please try again.")

    # Отображение главного меню
    def _display_main_menu(self):
        print("\n=== Main Menu ===")
        print("1. View all courses")
        print("2. View available courses")
        print("3. View course details")
        print("4. Add new course")
        print("5. Register new student")
        print("6. View all students")
        print("7. View student details")
        print("8. Enroll student in course")
        print("9. Drop student from course")
        print("10. Complete course")
        print("11. View student's courses")
        print("12. View course roster")
        print("13. Search courses by instructor")
        print("14. View statistics")
        print("15. Exit")
        print("Enter choice (1-15): ", end='')

    # Обработка выбора меню
    def _handle_menu_choice(self, choice):
        actions = {
            1: self._platform.display_all_courses,
            2: self._view_available_courses,
            3: self._view_course_details,
            4: self._add_new_course,
            5: self._register_student,
            6: self._platform.display_all_students,
            7: self._view_student_details,
            8: self._enroll_student,
            9: self._drop_course,
            10: self._complete_course,
            11: self._view_student_courses,
            12: self._view_course_roster,
            13: self._search_by_instructor,
            14: self._platform.display_statistics
        }
        if choice in actions:
            actions[choice]()
        else:
            print("Invalid choice. Please try again.")

    def _view_available_courses(self):
        courses = self._platform.get_available_courses()
        if not courses:
            print("\nNo available courses")
            return
        print("\n=== Available Courses ===")
        for course in courses:
            course.display_short()
        print(f"\nAvailable courses: {len(courses)}")

    def _view_course_details(self):
        course_id = int(input("\nEnter course ID: "))
        course = self._platform.find_course_by_id(course_id)
        if course:
            course.display_info()
        else:
            print("Error: Course not found")

    def _add_new_course(self):
        title = input("\nEnter course title: ")
        instructor = input("Enter instructor name: ")
        max_students = int(input("Enter maximum students: "))

        print("\nSelect course level:")
        for i, level in enumerate(CourseLevel, 1):
            print(f"{i}. {level.name}")
        level_choice = int(input("Enter choice: "))
        level = list(CourseLevel)[level_choice - 1]

        duration = int(input("Enter duration (weeks): "))
        price = float(input("Enter price: $"))

        course = Course(title, instructor, max_students, level, duration, price)
        description = input("Enter course description (optional): ")
        if description:
            course.set_description(description)

        self._platform.add_course(course)

    def _register_student(self):
        name = input("\nEnter student name: ")
        email = input("Enter email: ")
        phone = input("Enter phone: ")

        student = Student(name, email, phone)
        self._platform.add_student(student)

    def _view_student_details(self):
        student_id = int(input("\nEnter student ID: "))
        student = self._platform.find_student_by_id(student_id)
        if student:
            student.display_info()
        else:
            print("Error: Student not found")

    def _enroll_student(self):
        student_id = int(input("\nEnter student ID: "))
        student = self._platform.find_student_by_id(student_id)
        if not student:
            print("Error: Student not found")
            return

        course_id = int(input("Enter course ID: "))
        course = self._platform.find_course_by_id(course_id)
        if not course:
            print("Error: Course not found")
            return

        self._platform.enroll_student(student, course)

    def _drop_course(self):
        student_id = int(input("\nEnter student ID: "))
        student = self._platform.find_student_by_id(student_id)
        if not student:
            print("Error: Student not found")
            return

        course_id = int(input("Enter course ID: "))
        course = self._platform.find_course_by_id(course_id)
        if not course:
            print("Error: Course not found")
            return

        self._platform.drop_course(student, course)

    def _complete_course(self):
        student_id = int(input("\nEnter student ID: "))
        student = self._platform.find_student_by_id(student_id)
        if not student:
            print("Error: Student not found")
            return

        course_id = int(input("Enter course ID: "))
        course = self._platform.find_course_by_id(course_id)
        if not course:
            print("Error: Course not found")
            return

        grade = input("Enter grade (A/B/C/D/F): ").upper()
        self._platform.complete_course(student, course, grade)

    def _view_student_courses(self):
        student_id = int(input("\nEnter student ID: "))
        student = self._platform.find_student_by_id(student_id)
        if student:
            self._platform.display_student_courses(student)
        else:
            print("Error: Student not found")

    def _view_course_roster(self):
        course_id = int(input("\nEnter course ID: "))
        course = self._platform.find_course_by_id(course_id)
        if course:
            self._platform.display_course_students(course)
        else:
            print("Error: Course not found")

    def _search_by_instructor(self):
        instructor = input("\nEnter instructor name: ")
        courses = self._platform.get_courses_by_instructor(instructor)
        if not courses:
            print("\nNo courses found")
            return
        print(f"\n=== Courses by {instructor} ===")
        for course in courses:
            course.display_short()
        print(f"\nFound: {len(courses)} course(s)")

def main():
    ui = PlatformUI("CodeAcademy Pro")
    ui.run()

if __name__ == "__main__":
    main()