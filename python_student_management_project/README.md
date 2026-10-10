# Python Student Management System

A beginner-friendly Python project that stores student records in an SQLite database.

## Features
- Add a student
- View all students
- Search by name, course, or email
- Update student details
- Delete a student
- Validate age and email
- Prevent duplicate email addresses
- Automatically creates `students.db` on first run

## Requirements
- Python 3.9 or newer
- No third-party packages required

## Run the project

1. Extract the ZIP file.
2. Open a terminal/command prompt in the extracted folder.
3. Run:

   ```bash
   python main.py
   ```

   On some Windows systems, use `py main.py`.

4. Choose an option from the menu.

## Database
The application creates `students.db` in the same folder when first launched. To reset the sample database, close the program and delete `students.db`; it will be recreated next time.

## Suggested test
1. Add a student with a unique email.
2. View all students.
3. Search for that student's name.
4. Update the student's course.
5. Delete the student and verify the list.

## Project structure
```text
python_student_management_project/
├── main.py
├── README.md
└── requirements.txt
```
