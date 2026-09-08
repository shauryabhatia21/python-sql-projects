import mysql.connector as m1
import os
import sys

# Database connection details (replace with your password):
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'YOUR_PASSWORD')
DB_NAME = os.getenv('DB_NAME', 'ots')

def get_connection():
    return m1.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)

while True:
    print('**** BANK MAIN MENU ****')
    print('1. Add Customer')
    print('2. Delete Customer')
    print('3. Change Account Type')
    print('4. Display All Records')
    print('5. Search Customer')
    print('6. Exit')
    print('-'*50)
    try:
        ch=int(input('Enter your choice: '))
    except ValueError:
        print('Please enter a valid number')
        continue

    match ch:
        case 1:
            try:
                con=get_connection()
                acc=int(input('Enter account number: '))
                name=input('Enter customer name: ')
                acc_type=input('Enter account type (Savings/Current): ')
                bal=int(input('Enter opening balance: '))
                qry="insert into customer values({},'{}','{}',{})".format(acc,name,acc_type,bal)
                cursor=con.cursor()
                cursor.execute(qry)
                if cursor.rowcount>0:
                    print("Customer added successfully")
                else:
                    print("Customer not added")
                con.commit()
                con.close()
            except Exception as e:
                print('Error:', e)
            print('-'*50)
        case 2:
            try:
                con=get_connection()
                acc=int(input('Enter account number to delete: '))
                qry="delete from customer where acc={}".format(acc)
                cursor=con.cursor()
                cursor.execute(qry)
                if cursor.rowcount>0:
                    print("Customer record deleted")
                else:
                    print("Customer account not found")
                con.commit()
                con.close()
            except Exception as e:
                print('Error:', e)
            print('-'*50)
        case 3:
            try:
                con=get_connection()
                acc=int(input('Enter account number: '))
                acc_type=input('Enter new account type: ')
                qry="update customer set type='{}' where acc={}".format(acc_type,acc)
                cursor=con.cursor()
                cursor.execute(qry)
                if cursor.rowcount>0:
                    print("Account type updated")
                else:
                    print("Account not found")
                con.commit()
                con.close()
            except Exception as e:
                print('Error:', e)
            print('-'*50)
        case 4:
            try:
                con=get_connection()
                qry="select * from customer"
                cursor=con.cursor()
                cursor.execute(qry)
                rows=cursor.fetchall()
                print('-'*50)
                print("ALL CUSTOMER RECORDS:")
                for i in rows:
                    print(f"ACC NO: {i[0]} | NAME: {i[1]} | TYPE: {i[2]} | BALANCE: ₹{i[3]}")
                con.close()
            except Exception as e:
                print('Error:', e)
            print('-'*50)
        case 5:
            try:
                con=get_connection()
                acc=int(input('Enter account number to search: '))
                qry="select * from customer where acc={}".format(acc)
                cursor=con.cursor()
                cursor.execute(qry)
                rows=cursor.fetchall()
                if not rows:
                    print("No customer found with account number:", acc)
                else:
                    for i in rows:
                        print(f"ACC NO: {i[0]} | NAME: {i[1]} | TYPE: {i[2]} | BALANCE: ₹{i[3]}")
                con.close()
            except Exception as e:
                print('Error:', e)
            print('-'*50)
        case 6:
            print('*'*50)
            print('Thank you for using Bank Portal. Data stored.')
            print('*'*50)
            sys.exit()
