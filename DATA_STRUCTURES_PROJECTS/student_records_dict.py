# ==============================================================================
# Program: Student Information System using Hash Map (Dictionary + Lists)
# Author: Shaurya Bhatia (Bennett University)
# Description: Demonstrates hash map key lookups where enrollment number serves
#              as primary key mapping to a list of student attributes [Name, Course, Fee].
# ==============================================================================

def student_dict_manager():
    student_db = {}

    print("=" * 60)
    print("      STUDENT RECORDS MANAGER (DICTIONARY WITH LIST VALUES)")
    print("=" * 60)

    while True:
        try:
            eno = int(input("Enter enrollment number: "))
        except ValueError:
            print("Invalid input! Enrollment number must be an integer.")
            continue

        if eno in student_db:
            print(f"Warning: Enrollment number {eno} already exists for {student_db[eno][0]}!")
            overwrite = input("Do you want to update this record? (yes/no): ").strip().lower()
            if overwrite not in ("yes", "y"):
                continue

        name = input("Enter student name: ").strip()
        course = input("Enter course name: ").strip()

        try:
            fee = int(input("Enter fee amount: "))
        except ValueError:
            print("Invalid fee amount! Setting fee to 0.")
            fee = 0

        # Mapping enrollment number (key) to attributes list (value)
        student_db[eno] = [name, course, fee]
        print(f"Record for Enrollment [{eno}] saved successfully!")

        more = input("\nDo you want to enter more students? (yes/no): ").strip().lower()
        if more in ("no", "n"):
            break

    print("\n" + "=" * 60)
    print("                 STUDENT ROSTER DATABASE")
    print("=" * 60)

    if not student_db:
        print("No student records available.")
        return

    total_fees = 0
    for eno, details in student_db.items():
        print(f"Enrollment No : {eno}")
        print(f"Student Name  : {details[0]}")
        print(f"Course        : {details[1]}")
        print(f"Fee Amount    : Rs. {details[2]:,}")
        print("-" * 60)
        total_fees += details[2]

    print(f"Total Enrolled Students : {len(student_db)}")
    print(f"Total Tuition Collected : Rs. {total_fees:,}")
    print("=" * 60)


if __name__ == "__main__":
    student_dict_manager()
