# ==============================================================================
# Program: Student Records Management using Nested Lists
# Author: Shaurya Bhatia (Bennett University)
# Description: Demonstrates data storage, continuous data entry, iteration,
#              and formatting with nested list data structures.
# ==============================================================================

def student_list_manager():
    students = []

    print("=" * 50)
    print("      STUDENT RECORDS MANAGER (NESTED LISTS)")
    print("=" * 50)

    while True:
        try:
            eno = int(input("Enter enrollment number: "))
            name = input("Enter student name: ").strip()
            course = input("Enter course name: ").strip()
            fee = int(input("Enter fee amount: "))
        except ValueError:
            print("Invalid input! Enrollment number and fee must be integers.")
            continue

        record = [eno, name, course, fee]
        students.append(record)
        print(f"Record for '{name}' added successfully!")

        more = input("\nDo you want to enter more students? (yes/no): ").strip().lower()
        if more == "no" or more == "n":
            break

    print("\n" + "=" * 50)
    print("            ALL REGISTERED STUDENTS")
    print("=" * 50)

    if not students:
        print("No student records available.")
        return

    total_fees = 0
    for s in students:
        print(f"Enrollment No : {s[0]}")
        print(f"Student Name  : {s[1]}")
        print(f"Course        : {s[2]}")
        print(f"Fee Amount    : Rs. {s[3]:,}")
        print("-" * 50)
        total_fees += s[3]

    print(f"Total Students Enrolled : {len(students)}")
    print(f"Total Fees Collected    : Rs. {total_fees:,}")
    print("=" * 50)


if __name__ == "__main__":
    student_list_manager()
