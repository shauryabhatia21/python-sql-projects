# Student Management System (Python & MySQL)

A complete Student Admission & Management application featuring both a Tkinter Graphical User Interface (GUI) and an interactive command-line CRUD menu.

## Features
- **Tkinter GUI Form (`student_gui.py`)**: Clean registration form with input fields for Enrollment Number, Name, Course, and Fees.
- **Console CRUD Operations (`student_console_menu.py`)**: Add, delete, search, update, and display all records.
- **MySQL Database**: Stores and persists all student records in MySQL.

## Database Setup
Run `schema.sql` in your MySQL command line client:
```sql
source schema.sql;
```

## Configuration
Set your MySQL root password:
- Edit `DB_PASSWORD = 'YOUR_PASSWORD'` in the scripts, OR
- Set an environment variable: `$env:DB_PASSWORD="your_password"`

## Running
- **GUI Application**: `python student_gui.py`
- **CLI Application**: `python student_console_menu.py`
