# CSV STUDENT RECORD MANAGER
# Persistent file storage using Python's standard csv module (student_records.csv)

import csv
import os
import sys

CSV_FILE = "student_records.csv"

def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Enroll', 'StudentName', 'Course', 'Fee'])

def add_student():
    eno = input('Enter student enrollment number: ')
    name = input('Enter student name: ')
    course = input('Enter course name: ')
    fee = input('Enter fees: ')
    with open(CSV_FILE, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([eno, name, course, fee])
    print("Student added successfully to CSV!")
    print('=' * 75)

def display_all():
    if not os.path.exists(CSV_FILE):
        print("No CSV file found.")
        return
    with open(CSV_FILE, "r", encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        print('-' * 75)
        print(f"{'Enrollment':<15} {'Name':<20} {'Course':<20} {'Fee':<10}")
        print('-' * 75)
        count = 0
        for row in reader:
            if row:
                count += 1
                print(f"{row[0]:<15} {row[1]:<20} {row[2]:<20} {row[3]:<10}")
        print('-' * 75)
        print(f"Total students on file: {count}")
    print('=' * 75)

def search_student():
    eno = input('Enter enrollment number to search: ')
    with open(CSV_FILE, "r", encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if row and row[0] == eno:
                print('-' * 75)
                print(f"Record Found:")
                print(f"Enrollment : {row[0]}")
                print(f"Name       : {row[1]}")
                print(f"Course     : {row[2]}")
                print(f"Fee        : {row[3]}")
                print('=' * 75)
                return
    print("Enrollment number does not exist.")
    print('=' * 75)

def delete_student():
    eno = input('Enter enrollment number to delete: ')
    records = []
    found = False
    with open(CSV_FILE, "r", encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if row:
                if row[0] == eno:
                    found = True
                else:
                    records.append(row)
    if found:
        with open(CSV_FILE, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if header:
                writer.writerow(header)
            writer.writerows(records)
        print("Record deleted successfully from CSV.")
    else:
        print("Record not found.")
    print('=' * 75)

def main():
    init_csv()
    while True:
        print("\n" + "=" * 50)
        print('         *** CSV STUDENT MANAGER ***')
        print("=" * 50)
        print('1. Add a student')
        print('2. Display all students')
        print('3. Search student')
        print('4. Delete student')
        print('5. Exit')
        print('-' * 50)

        try:
            ch = int(input('Enter your choice (1-5): '))
        except ValueError:
            print("Invalid choice!")
            continue

        match ch:
            case 1:
                add_student()
            case 2:
                display_all()
            case 3:
                search_student()
            case 4:
                delete_student()
            case 5:
                print("All changes saved. Goodbye!")
                sys.exit(0)

if __name__ == '__main__':
    main()
