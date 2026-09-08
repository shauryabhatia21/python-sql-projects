# STUDENT MANAGEMENT SYSTEM (DICTIONARY DATA STRUCTURE)
# Features: Add student, Rename, Search, Modify details, Display all, Remove student

import sys
import generators

student = {}

def main():
    while True:
        print("\n" + "=" * 50)
        print('          *** STUDENT MAIN MENU ***')
        print("=" * 50)
        print('1. Add a student')
        print('2. Rename student')
        print('3. Search student')
        print('4. Modify student')
        print('5. Display all students')
        print('6. Remove student')
        print('7. Exit')
        print('-' * 50)

        try:
            ch = int(input('Enter your choice (1-7): '))
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue

        print('-' * 75)
        match ch:
            case 1:
                eno = generators.genAcno()
                name = input('Enter student name: ')
                course = input('Enter course name: ')
                fee = int(input('Enter fees: '))
                student[eno] = [name, course, fee]
                print('Your enrollment number is:', eno)
                print("Student added successfully!")
                print('=' * 75)

            case 2:
                y = input('Enter enrollment number to rename: ')
                if y in student:
                    name1 = input('Enter new name: ')
                    student[y][0] = name1
                    print("Record updated successfully!")
                else:
                    print('Enrollment number does not exist')
                print('=' * 75)

            case 3:
                eno = input('Enter your enrollment number to search: ')
                if eno in student:
                    print('Name   :', student[eno][0])
                    print('Course :', student[eno][1])
                    print('Fee    :', student[eno][2])
                else:
                    print('Enrollment number does not exist')
                print('=' * 75)

            case 4:
                eno = input('Enter enrollment number to modify: ')
                if eno in student:
                    name1 = input('Enter new student name: ')
                    course1 = input('Enter new course name: ')
                    fee1 = int(input('Enter new fees: '))
                    student[eno] = [name1, course1, fee1]
                    print('Record updated successfully!')
                else:
                    print('Record not found')
                print('=' * 75)

            case 5:
                if not student:
                    print('No students registered yet.')
                else:
                    for eno, info in student.items():
                        print('Enrollment No :', eno)
                        print('Name          :', info[0])
                        print('Course        :', info[1])
                        print('Fee           :', info[2])
                        print('-' * 75)
                    print('All student records printed.')
                print('=' * 75)

            case 6:
                eno = input('Enter enrollment number to remove: ')
                if eno in student:
                    del student[eno]
                    print('Record removed successfully.')
                else:
                    print('Record not found')
                print('=' * 75)

            case 7:
                print('The data has been stored.')
                print('THANK YOU FOR VISITING')
                sys.exit(0)

if __name__ == '__main__':
    main()
