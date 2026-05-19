# Imports
import json
import os
import time

DATA_FILE = "students.json"
STUDENTS = []   # Global in-memory list


# -----------------------------
# Data loading / saving
# -----------------------------

def create_data_file_if_missing():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as file:
            json.dump([], file)


def load_once():
    """Load students only once at program start."""
    global STUDENTS
    with open(DATA_FILE, "r") as file:
        STUDENTS = json.load(file)


def save():
    """Save global STUDENTS list to file."""
    with open(DATA_FILE, "w") as file:
        json.dump(STUDENTS, file, indent=4)


# -----------------------------
# Login
# -----------------------------

def login():
    username = "admin"
    password = "password"

    while True:
        given_username = input("Enter username: ")
        given_password = input("Enter password: ")

        if given_username == username and given_password == password:
            print("Login successful.")
            break
        else:
            print("Incorrect username or password. Please try again.")


# -----------------------------
# Student operations
# -----------------------------

def add_student():
    global STUDENTS

    student_number = input("Enter student number: ")
    name = input("Enter student name: ")
    contact = input("Enter student contact information: ")

    # Check duplicates
    if any(s["student_number"] == student_number for s in STUDENTS):
        print("Student number already exists.")
        return

    new_student = {
        "student_number": student_number,
        "name": name,
        "contact": contact,
        "grades": []
    }

    STUDENTS.append(new_student)
    save()
    print("Student added.")


def add_grade():
    global STUDENTS

    student_number = input("Enter student number: ")
    course = input("Enter course name: ")
    grade = input("Enter grade: ")

    for student in STUDENTS:
        if student["student_number"] == student_number:
            student["grades"].append({"course": course, "grade": grade})
            save()
            print("Grade added.")
            return

    print("Student not found.")


def search_student():
    student_number = input("Enter student number to search for: ")

    start_time = time.perf_counter()

    found_student = next((s for s in STUDENTS if s["student_number"] == student_number), None)

    end_time = time.perf_counter()

    if found_student:
        print("Student found:")
        print(f"Student Number: {found_student['student_number']}")
        print(f"Name: {found_student['name']}")
        print(f"Contact: {found_student['contact']}")
        print(f"Grades: {found_student['grades']}")
    else:
        print("Student not found.")

    print(f"Search took {end_time - start_time:.6f} seconds.")


def display_all_students():
    if not STUDENTS:
        print("No students found.")
        return

    print("All students:")

    sorted_students = sorted(STUDENTS, key=lambda s: s["name"])

    for student in sorted_students:
        print(f"Student Number: {student['student_number']}")
        print(f"Name: {student['name']}")
        print(f"Contact: {student['contact']}")
        print(f"Grades: {student['grades']}")
        print()


def count_total_grades():
    total = sum(len(s["grades"]) for s in STUDENTS)
    print(f"Total number of grades: {total}")


def display_course_summary():
    course_counts = {}

    for student in STUDENTS:
        for grade in student["grades"]:
            course = grade["course"]
            course_counts[course] = course_counts.get(course, 0) + 1

    print("Course summary:")
    for course, count in course_counts.items():
        print(f"{course}: {count} grade(s)")


def save_backup():
    with open("students_backup.json", "w") as file:
        json.dump(STUDENTS, file, indent=4)
    print("Backup saved.")


# -----------------------------
# Main program
# -----------------------------

def main():
    create_data_file_if_missing()
    load_once()
    login()

    while True:
        print("\nSelect an action:")
        print("1. Add a student")
        print("2. Add grade")
        print("3. Search for student")
        print("4. Display all students")
        print("5. Count total grades")
        print("6. Display course summary")
        print("7. Save backup")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            add_grade()
        elif choice == "3":
            search_student()
        elif choice == "4":
            display_all_students()
        elif choice == "5":
            count_total_grades()
        elif choice == "6":
            display_course_summary()
        elif choice == "7":
            save_backup()
        elif choice == "8":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
