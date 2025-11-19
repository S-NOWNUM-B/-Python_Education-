from enum import Enum


# Перечисление для статуса успеваемости
class AcademicStatus(Enum):
    EXCELLENT = 1  # Отлично (90-100)
    GOOD = 2  # Хорошо (75-89)
    SATISFACTORY = 3  # Удовлетворительно (60-74)
    UNSATISFACTORY = 4  # Неудовлетворительно (0-59)


# Класс для хранения информации о предмете и оценке
class Grade:
    def __init__(self, subject, score):
        self._subject = subject
        self._score = score

    def get_subject(self):
        return self._subject

    def get_score(self):
        return self._score

    def set_score(self, score):
        self._score = score


# Класс студента
class Student:
    _student_counter = 1000

    def __init__(self, name, major, year):
        self._id = Student._student_counter
        Student._student_counter += 1
        self._name = name
        self._major = major
        self._year = year
        self._grades = []

    # Геттеры
    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_major(self):
        return self._major

    def get_year(self):
        return self._year

    def get_grades(self):
        return self._grades

    # Сеттеры
    def set_name(self, name):
        self._name = name

    def set_major(self, major):
        self._major = major

    def set_year(self, year):
        self._year = year

    # Добавление оценки
    def add_grade(self, subject, score):
        if score < 0 or score > 100:
            print("Error: Grade must be between 0 and 100")
            return
        # Проверка на существующий предмет
        for grade in self._grades:
            if grade.get_subject().lower() == subject.lower():
                print(f"Warning: Grade for {subject} already exists")
                print("Use update_grade to modify it")
                return
        self._grades.append(Grade(subject, score))
        print("\nGrade added successfully!")
        print(f"Subject: {subject} | Score: {score}")

    # Обновление оценки
    def update_grade(self, subject, new_score):
        if new_score < 0 or new_score > 100:
            print("Error: Grade must be between 0 and 100")
            return False
        for grade in self._grades:
            if grade.get_subject().lower() == subject.lower():
                old_score = grade.get_score()
                grade.set_score(new_score)
                print("\nGrade updated successfully!")
                print(f"Subject: {subject}")
                print(f"Old score: {old_score} → New score: {new_score}")
                return True
        print("Error: Subject not found")
        return False

    # Удаление оценки
    def remove_grade(self, subject):
        for i, grade in enumerate(self._grades):
            if grade.get_subject().lower() == subject.lower():
                removed = self._grades.pop(i)
                print(f"\nGrade removed: {removed.get_subject()} ({removed.get_score()})")
                return True
        print("Error: Subject not found")
        return False

    # Вычисление среднего балла
    def calculate_average(self):
        if not self._grades:
            return 0.0
        return sum(g.get_score() for g in self._grades) / len(self._grades)

    # Получение статуса успеваемости
    def get_status(self):
        avg = self.calculate_average()
        if avg >= 90:
            return AcademicStatus.EXCELLENT
        elif avg >= 75:
            return AcademicStatus.GOOD
        elif avg >= 60:
            return AcademicStatus.SATISFACTORY
        else:
            return AcademicStatus.UNSATISFACTORY

    # Текстовый статус
    def get_status_text(self):
        status_map = {
            AcademicStatus.EXCELLENT: "Отлично (Excellent)",
            AcademicStatus.GOOD: "Хорошо (Good)",
            AcademicStatus.SATISFACTORY: "Удовлетворительно (Satisfactory)",
            AcademicStatus.UNSATISFACTORY: "Неудовлетворительно (Unsatisfactory)"
        }
        return status_map[self.get_status()]

    # Наивысшая оценка
    def get_highest_grade(self):
        if not self._grades:
            return None
        return max(self._grades, key=lambda g: g.get_score())

    # Низшая оценка
    def get_lowest_grade(self):
        if not self._grades:
            return None
        return min(self._grades, key=lambda g: g.get_score())

    # Отображение информации о студенте
    def display(self):
        print("\n=== Student Information ===")
        print(f"ID: {self._id}")
        print(f"Name: {self._name}")
        print(f"Major: {self._major}")
        print(f"Year: {self._year}")
        print(f"Total subjects: {len(self._grades)}")

        if self._grades:
            print("\nGrades:")
            for grade in self._grades:
                print(f"  • {grade.get_subject()}: {grade.get_score():.2f}")
            print(f"\nAverage: {self.calculate_average():.2f}")
            print(f"Status: {self.get_status_text()}")

            highest = self.get_highest_grade()
            lowest = self.get_lowest_grade()
            if highest:
                print(f"Highest: {highest.get_subject()} ({highest.get_score():.2f})")
            if lowest:
                print(f"Lowest: {lowest.get_subject()} ({lowest.get_score():.2f})")
        else:
            print("\nNo grades recorded yet")
        print("---")

    # Краткое отображение студента
    def display_short(self):
        status_symbols = {
            AcademicStatus.EXCELLENT: "★★★",
            AcademicStatus.GOOD: "★★",
            AcademicStatus.SATISFACTORY: "★",
            AcademicStatus.UNSATISFACTORY: "✗"
        }
        symbol = status_symbols[self.get_status()]
        print(f"ID: {self._id} | {self._name} | Year {self._year} | Avg: {self.calculate_average():.2f} {symbol}")


# Класс реестра студентов
class StudentRegistry:
    def __init__(self, university_name):
        self._students = []
        self._university_name = university_name

    # Добавление студента
    def add_student(self, student):
        self._students.append(student)
        print("\nStudent registered successfully!")
        print(f"Student ID: {student.get_id()}")
        print(f"Name: {student.get_name()}")

    # Удаление студента
    def remove_student(self, student_id):
        for i, student in enumerate(self._students):
            if student.get_id() == student_id:
                removed = self._students.pop(i)
                print(f"\nStudent removed: {removed.get_name()}")
                return True
        print(f"\nError: Student with ID {student_id} not found")
        return False

    # Поиск студента по ID
    def find_student_by_id(self, student_id):
        for student in self._students:
            if student.get_id() == student_id:
                return student
        return None

    # Поиск студентов по имени
    def search_by_name(self, name):
        term = name.lower()
        return [s for s in self._students if term in s.get_name().lower()]

    # Поиск студентов по специальности
    def search_by_major(self, major):
        term = major.lower()
        return [s for s in self._students if term in s.get_major().lower()]

    # Получение студентов по статусу
    def get_students_by_status(self, status):
        return [s for s in self._students if s.get_status() == status]

    # Отображение всех студентов
    def show_all_students(self):
        if not self._students:
            print("\nNo students registered")
            return
        print(f"\n=== {self._university_name} - All Students ===")
        for student in self._students:
            student.display_short()
        print(f"\nTotal students: {len(self._students)}")

    # Отображение топ студентов
    def show_top_students(self, count):
        if not self._students:
            print("\nNo students registered")
            return
        sorted_students = sorted(self._students, key=lambda s: s.calculate_average(), reverse=True)
        display_count = min(count, len(sorted_students))
        print(f"\n=== Top {display_count} Students ===")
        for i, student in enumerate(sorted_students[:display_count], 1):
            print(f"{i}. {student.get_name()} | Avg: {student.calculate_average():.2f} | {student.get_status_text()}")

    # Общая статистика
    def show_statistics(self):
        if not self._students:
            print("\nNo students to analyze")
            return

        total = len(self._students)
        status_counts = {status: 0 for status in AcademicStatus}
        total_average = 0
        total_grades = 0

        for student in self._students:
            status_counts[student.get_status()] += 1
            total_average += student.calculate_average()
            total_grades += len(student.get_grades())

        overall_avg = total_average / total

        print(f"\n=== {self._university_name} Statistics ===")
        print(f"Total students: {total}")
        print(f"Total grades recorded: {total_grades}")
        print(f"Overall average: {overall_avg:.2f}")
        print("\nPerformance Distribution:")
        print(
            f"  Excellent: {status_counts[AcademicStatus.EXCELLENT]} ({status_counts[AcademicStatus.EXCELLENT] * 100.0 / total:.1f}%)")
        print(
            f"  Good: {status_counts[AcademicStatus.GOOD]} ({status_counts[AcademicStatus.GOOD] * 100.0 / total:.1f}%)")
        print(
            f"  Satisfactory: {status_counts[AcademicStatus.SATISFACTORY]} ({status_counts[AcademicStatus.SATISFACTORY] * 100.0 / total:.1f}%)")
        print(
            f"  Unsatisfactory: {status_counts[AcademicStatus.UNSATISFACTORY]} ({status_counts[AcademicStatus.UNSATISFACTORY] * 100.0 / total:.1f}%)")

    # Анализ по предметам
    def show_subject_analysis(self):
        if not self._students:
            print("\nNo students to analyze")
            return

        subject_scores = {}
        for student in self._students:
            for grade in student.get_grades():
                subject = grade.get_subject()
                if subject not in subject_scores:
                    subject_scores[subject] = []
                subject_scores[subject].append(grade.get_score())

        if not subject_scores:
            print("\nNo grades recorded yet")
            return

        print("\n=== Subject Analysis ===")
        for subject, scores in subject_scores.items():
            avg = sum(scores) / len(scores)
            print(f"{subject}: {avg:.2f} average ({len(scores)} students)")


# Класс пользовательского интерфейса
class RegistryUI:
    def __init__(self, university_name):
        self._registry = StudentRegistry(university_name)

    def run(self):
        print("=== Student Grade Management System ===\n")
        while True:
            try:
                self._display_menu()
                choice = int(input())
                if choice == 14:
                    print("\nThank you for using Student Grade Management System!")
                    break
                self._handle_menu(choice)
            except Exception:
                print("\nError: Invalid input. Please try again.")

    def _display_menu(self):
        print("\n=== Main Menu ===")
        print("1. Register new student")
        print("2. Remove student")
        print("3. Add grade")
        print("4. Update grade")
        print("5. Remove grade")
        print("6. View student information")
        print("7. Search students by name")
        print("8. Search students by major")
        print("9. View all students")
        print("10. View top students")
        print("11. View students by status")
        print("12. View statistics")
        print("13. View subject analysis")
        print("14. Exit")
        print("Enter choice (1-14): ", end='')

    def _handle_menu(self, choice):
        actions = {
            1: self._register_student, 2: self._remove_student,
            3: self._add_grade, 4: self._update_grade, 5: self._remove_grade,
            6: self._view_student_info, 7: self._search_by_name,
            8: self._search_by_major, 9: self._registry.show_all_students,
            10: self._view_top_students, 11: self._view_students_by_status,
            12: self._registry.show_statistics, 13: self._registry.show_subject_analysis
        }
        if choice in actions:
            actions[choice]()
        else:
            print("Invalid choice. Please try again.")

    def _register_student(self):
        name = input("\nEnter student name: ")
        major = input("Enter major: ")
        year = int(input("Enter year (1-4): "))
        student = Student(name, major, year)
        self._registry.add_student(student)

    def _remove_student(self):
        student_id = int(input("\nEnter student ID to remove: "))
        self._registry.remove_student(student_id)

    def _add_grade(self):
        student_id = int(input("\nEnter student ID: "))
        student = self._registry.find_student_by_id(student_id)
        if not student:
            print("Error: Student not found")
            return
        subject = input("Enter subject name: ")
        score = float(input("Enter grade (0-100): "))
        student.add_grade(subject, score)

    def _update_grade(self):
        student_id = int(input("\nEnter student ID: "))
        student = self._registry.find_student_by_id(student_id)
        if not student:
            print("Error: Student not found")
            return
        subject = input("Enter subject name: ")
        score = float(input("Enter new grade (0-100): "))
        student.update_grade(subject, score)

    def _remove_grade(self):
        student_id = int(input("\nEnter student ID: "))
        student = self._registry.find_student_by_id(student_id)
        if not student:
            print("Error: Student not found")
            return
        subject = input("Enter subject name: ")
        student.remove_grade(subject)

    def _view_student_info(self):
        student_id = int(input("\nEnter student ID: "))
        student = self._registry.find_student_by_id(student_id)
        if student:
            student.display()
        else:
            print("Error: Student not found")

    def _search_by_name(self):
        name = input("\nEnter name to search: ")
        results = self._registry.search_by_name(name)
        self._display_search_results(results, "Name")

    def _search_by_major(self):
        major = input("\nEnter major to search: ")
        results = self._registry.search_by_major(major)
        self._display_search_results(results, "Major")

    def _view_top_students(self):
        count = int(input("\nEnter number of top students to display: "))
        self._registry.show_top_students(count)

    def _view_students_by_status(self):
        print("\nSelect status:")
        print("1. Excellent")
        print("2. Good")
        print("3. Satisfactory")
        print("4. Unsatisfactory")
        choice = int(input("Enter choice (1-4): "))
        status_map = {1: AcademicStatus.EXCELLENT, 2: AcademicStatus.GOOD,
                      3: AcademicStatus.SATISFACTORY, 4: AcademicStatus.UNSATISFACTORY}
        if choice in status_map:
            results = self._registry.get_students_by_status(status_map[choice])
            self._display_search_results(results, status_map[choice].name)
        else:
            print("Invalid choice")

    def _display_search_results(self, results, search_type):
        if not results:
            print("\nNo students found")
            return
        print(f"\n=== Search Results ({search_type}) ===")
        for student in results:
            student.display_short()
        print(f"\nFound: {len(results)} student(s)")

def main():
    ui = RegistryUI("University of Technology")
    ui.run()

if __name__ == "__main__":
    main()