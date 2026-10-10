import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).with_name("students.db")


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL CHECK(age > 0),
                course TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


def add_student(name, age, course, email):
    with connect() as conn:
        conn.execute(
            "INSERT INTO students (name, age, course, email, created_at) VALUES (?, ?, ?, ?, ?)",
            (name.strip(), int(age), course.strip(), email.strip().lower(),
             datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )


def list_students(search=""):
    with connect() as conn:
        term = f"%{search.strip()}%"
        return conn.execute("""
            SELECT * FROM students
            WHERE name LIKE ? OR course LIKE ? OR email LIKE ?
            ORDER BY id DESC
        """, (term, term, term)).fetchall()


def update_student(student_id, name, age, course, email):
    with connect() as conn:
        cursor = conn.execute("""
            UPDATE students
            SET name = ?, age = ?, course = ?, email = ?
            WHERE id = ?
        """, (name.strip(), int(age), course.strip(), email.strip().lower(), int(student_id)))
        if cursor.rowcount == 0:
            raise ValueError("Student ID not found.")


def delete_student(student_id):
    with connect() as conn:
        cursor = conn.execute("DELETE FROM students WHERE id = ?", (int(student_id),))
        if cursor.rowcount == 0:
            raise ValueError("Student ID not found.")


def read_required(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def read_age(prompt="Age: "):
    while True:
        value = input(prompt).strip()
        try:
            age = int(value)
            if age > 0:
                return age
        except ValueError:
            pass
        print("Enter a whole number greater than 0.")


def read_email(prompt="Email: "):
    while True:
        email = input(prompt).strip().lower()
        if "@" in email and "." in email.split("@")[-1]:
            return email
        print("Enter a valid email address.")


def print_students(rows):
    if not rows:
        print("\nNo students found.")
        return
    print("\n" + "-" * 100)
    print(f"{'ID':<5}{'Name':<24}{'Age':<7}{'Course':<22}{'Email':<32}{'Created':<19}")
    print("-" * 100)
    for row in rows:
        print(f"{row['id']:<5}{row['name'][:22]:<24}{row['age']:<7}"
              f"{row['course'][:20]:<22}{row['email'][:30]:<32}{row['created_at']:<19}")
    print("-" * 100)


def main():
    init_db()
    while True:
        print("""
====================================
     STUDENT MANAGEMENT SYSTEM
====================================
1. Add student
2. View all students
3. Search students
4. Update student
5. Delete student
6. Exit
""")
        choice = input("Choose an option (1-6): ").strip()
        try:
            if choice == "1":
                name = read_required("Name: ")
                age = read_age()
                course = read_required("Course: ")
                email = read_email()
                add_student(name, age, course, email)
                print("Student added successfully.")
            elif choice == "2":
                print_students(list_students())
            elif choice == "3":
                term = read_required("Search by name, course, or email: ")
                print_students(list_students(term))
            elif choice == "4":
                student_id = int(read_required("Student ID to update: "))
                existing = next((s for s in list_students() if s["id"] == student_id), None)
                if not existing:
                    print("Student ID not found.")
                    continue
                print("Enter the new details:")
                name = read_required("Name: ")
                age = read_age()
                course = read_required("Course: ")
                email = read_email()
                update_student(student_id, name, age, course, email)
                print("Student updated successfully.")
            elif choice == "5":
                student_id = int(read_required("Student ID to delete: "))
                confirm = input("Are you sure? (y/n): ").strip().lower()
                if confirm == "y":
                    delete_student(student_id)
                    print("Student deleted successfully.")
                else:
                    print("Delete cancelled.")
            elif choice == "6":
                print("Thank you for using Student Management System!")
                break
            else:
                print("Please choose a number from 1 to 6.")
        except ValueError as exc:
            print(f"Error: {exc}")
        except sqlite3.IntegrityError:
            print("That email already exists. Please use a different email.")
        except sqlite3.Error as exc:
            print(f"Database error: {exc}")


if __name__ == "__main__":
    main()
