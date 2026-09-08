import mysql.connector as m1
import os

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'YOUR_PASSWORD')
DB_NAME = os.getenv('DB_NAME', 'ots')

def get_connection():
    return m1.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)

while True:
    print('**** STUDENT DATABASE MANAGEMENT ****')
    print('1. Add Student Record')
    print('2. Delete Student Record')
    print('3. Search Student')
    print('4. Update Student Record')
    print('5. Display All Records')
    print('6. Exit')
    print('-'*50)
    try:
        ch=int(input('Enter your choice: '))
    except ValueError:
        print('Please enter a valid number')
        continue

    match ch:
        case 1:
            con=get_connection()
            eno=int(input('Enter enrollment number: '))
            name=input('Enter student name: ')
            course=input('Enter course name: ')
            fees=int(input('Enter fees: '))
            qry="insert into student values({},'{}','{}',{})".format(eno,name,course,fees)
            cursor=con.cursor()
            cursor.execute(qry)
            if cursor.rowcount>0:
                print("Record added successfully")
            else:
                print("Record not added")
            con.commit()
            con.close()
            print('-'*50)
        case 2:
            con=get_connection()
            eno=int(input('Enter enrollment number to delete: '))
            qry="delete from student where eno={}".format(eno)
            cursor=con.cursor()
            cursor.execute(qry)
            if cursor.rowcount>0:
                print("Record deleted successfully")
            else:
                print("Record not found")
            con.commit()
            con.close()
            print('-'*50)
        case 3:
            con=get_connection()
            eno=int(input('Enter enrollment number to search: '))
            qry="select * from student where eno={}".format(eno)
            cursor=con.cursor()
            cursor.execute(qry)
            rows=cursor.fetchall()
            if not rows:
                print("Student not found")
            else:
                for row in rows:
                    print(f"ENO: {row[0]}, NAME: {row[1]}, COURSE: {row[2]}, FEES: {row[3]}")
            con.close()
            print('-'*50)
        case 4:
            con=get_connection()
            eno=int(input('Enter enrollment number to update: '))
            name=input('Enter new name: ')
            course=input('Enter new course: ')
            fees=int(input('Enter new fees: '))
            qry="update student set name='{}', course='{}', fees={} where eno={}".format(name,course,fees,eno)
            cursor=con.cursor()
            cursor.execute(qry)
            if cursor.rowcount>0:
                print("Record updated successfully")
            else:
                print("Record not updated")
            con.commit()
            con.close()
            print('-'*50)
        case 5:
            con=get_connection()
            qry="select * from student"
            cursor=con.cursor()
            cursor.execute(qry)
            rows=cursor.fetchall()
            print('-'*50)
            print("ALL STUDENT RECORDS:")
            for row in rows:
                print(f"ENO: {row[0]} | NAME: {row[1]} | COURSE: {row[2]} | FEES: {row[3]}")
            con.close()
            print('-'*50)
        case 6:
            print("Exiting Student Management...")
            break
