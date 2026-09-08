# BINARY FILE BANKING MANAGEMENT (PICKLE MODULE)
# Persistent disk storage of records using pickle serialization (customer.dat)

import pickle
import os
import random
import sys

DATA_FILE = 'customer.dat'

def genAcno():
    return "".join(str(random.randint(0, 9)) for _ in range(8))

def main():
    while True:
        print("\n" + "=" * 50)
        print('       *** PICKLE BANKING MAIN MENU ***')
        print("=" * 50)
        print('1. Add A Customer')
        print('2. Show All Records')
        print('3. Search Customer')
        print('4. Remove Customer')
        print('5. Deposit Amount')
        print('6. Withdraw Amount')
        print('7. Exit')
        print('-' * 50)

        try:
            ch = int(input('Enter your choice (1-7): '))
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue

        match ch:
            case 1:
                eno = genAcno()
                name = input('Enter customer name: ')
                type1 = input('Enter account type (Savings/Current): ')
                bal = int(input('Enter opening balance: '))
                a1 = [eno, name, type1, bal]
                with open(DATA_FILE, 'ab') as f1:
                    pickle.dump(a1, f1)
                print('-' * 50)
                print('Account Created & Saved to Disk Successfully!')
                print('Your Account Number is:', eno)
                print('=' * 75)

            case 2:
                print('-' * 75)
                if not os.path.exists(DATA_FILE):
                    print("No records file found.")
                    continue
                try:
                    count = 0
                    with open(DATA_FILE, 'rb') as f1:
                        while True:
                            try:
                                a1 = pickle.load(f1)
                                count += 1
                                print('Account Number :', a1[0])
                                print('Customer Name  :', a1[1])
                                print('Account Type   :', a1[2])
                                print('Balance        :', a1[3])
                                print('-' * 75)
                            except EOFError:
                                break
                    if count == 0:
                        print("File is empty.")
                    else:
                        print(f"Total Records Displayed: {count}")
                except Exception as e:
                    print("Error reading file:", e)
                print('=' * 75)

            case 3:
                print('-' * 75)
                if not os.path.exists(DATA_FILE):
                    print("No records file found.")
                    continue
                eno = input('Enter account number to search: ')
                found = False
                with open(DATA_FILE, 'rb') as f1:
                    while True:
                        try:
                            a1 = pickle.load(f1)
                            if str(a1[0]) == str(eno):
                                print('Account Number :', a1[0])
                                print('Customer Name  :', a1[1])
                                print('Account Type   :', a1[2])
                                print('Balance        :', a1[3])
                                print('=' * 75)
                                found = True
                                break
                        except EOFError:
                            break
                if not found:
                    print('No record found with account number:', eno)

            case 4:
                print('-' * 75)
                if not os.path.exists(DATA_FILE):
                    print("No records file found.")
                    continue
                eno = input('Enter account number to remove: ')
                found = False
                temp_file = 'temp.dat'
                with open(DATA_FILE, 'rb') as f1, open(temp_file, 'wb') as f2:
                    while True:
                        try:
                            a1 = pickle.load(f1)
                            if str(a1[0]) == str(eno):
                                found = True
                            else:
                                pickle.dump(a1, f2)
                        except EOFError:
                            break
                if found:
                    os.remove(DATA_FILE)
                    os.rename(temp_file, DATA_FILE)
                    print('Customer removed successfully from disk.')
                else:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                    print('No record found to delete.')
                print('=' * 75)

            case 5:
                print('-' * 75)
                if not os.path.exists(DATA_FILE):
                    print("No records file found.")
                    continue
                eno = input('Enter account number: ')
                try:
                    amount1 = int(input('Enter amount to deposit: '))
                except ValueError:
                    print("Invalid amount!")
                    continue
                found = False
                temp_file = 'temp.dat'
                with open(DATA_FILE, 'rb') as f1, open(temp_file, 'wb') as f2:
                    while True:
                        try:
                            a1 = pickle.load(f1)
                            if str(a1[0]) == str(eno):
                                a1[3] = int(a1[3]) + amount1
                                found = True
                                print('Amount Deposited. Updated Balance:', a1[3])
                            pickle.dump(a1, f2)
                        except EOFError:
                            break
                if found:
                    os.remove(DATA_FILE)
                    os.rename(temp_file, DATA_FILE)
                    print('Record updated successfully.')
                else:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                    print('Record not found.')
                print('=' * 75)

            case 6:
                print('-' * 75)
                if not os.path.exists(DATA_FILE):
                    print("No records file found.")
                    continue
                eno = input('Enter account number: ')
                try:
                    amount1 = int(input('Enter amount to withdraw: '))
                except ValueError:
                    print("Invalid amount!")
                    continue
                found = False
                temp_file = 'temp.dat'
                with open(DATA_FILE, 'rb') as f1, open(temp_file, 'wb') as f2:
                    while True:
                        try:
                            a1 = pickle.load(f1)
                            if str(a1[0]) == str(eno):
                                if int(a1[3]) >= amount1:
                                    a1[3] = int(a1[3]) - amount1
                                    print('Amount Withdrawn. Updated Balance:', a1[3])
                                else:
                                    print('Insufficient balance!')
                                found = True
                            pickle.dump(a1, f2)
                        except EOFError:
                            break
                if found:
                    os.remove(DATA_FILE)
                    os.rename(temp_file, DATA_FILE)
                    print('Record updated successfully.')
                else:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                    print('Record not found.')
                print('=' * 75)

            case 7:
                print("Exiting system. All files closed.")
                sys.exit(0)

if __name__ == '__main__':
    main()
