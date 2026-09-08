# CONTACT BOOK SYSTEM (DICTIONARY DATA STRUCTURE)
# Features: Add contact, update phone number, update email, show all contacts, remove, search

import sys
import generators

contacts = {}

def main():
    print('** CONTACT BOOK MANAGEMENT **')
    while True:
        print("\n" + "=" * 50)
        print('1. Add New Contact')
        print('2. Change Phone Number')
        print('3. Change Email Address')
        print('4. Show All Contacts')
        print('5. Remove Contact')
        print('6. Search Contact')
        print('7. Exit')
        print("-" * 50)

        try:
            ch = int(input("Enter your choice (1-7): "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue

        match ch:
            case 1:
                print('-' * 75)
                idd = generators.genphon()
                name = input('Enter contact name: ')
                phone = input('Enter mobile number: ')
                email = input('Enter email ID: ')
                contacts[idd] = [name, phone, email]
                print('Contact Added Successfully!')
                print('Generated Contact ID:', idd)
                print('=' * 75)

            case 2:
                print('-' * 75)
                v = input('Enter Contact ID: ')
                if v in contacts:
                    phone1 = input('Enter new phone number: ')
                    contacts[v][1] = phone1
                    print('Phone number updated successfully.')
                else:
                    print('Contact ID not found.')
                print('=' * 75)

            case 3:
                print('-' * 75)
                v = input('Enter Contact ID: ')
                if v in contacts:
                    mail1 = input('Enter new email ID: ')
                    contacts[v][2] = mail1
                    print('Email address updated successfully.')
                else:
                    print('Contact ID not found.')
                print('=' * 75)

            case 4:
                print('-' * 75)
                if not contacts:
                    print('No contacts saved yet.')
                else:
                    for cid, val in contacts.items():
                        print('Contact ID :', cid)
                        print('Name       :', val[0])
                        print('Phone No   :', val[1])
                        print('Email ID   :', val[2])
                        print('.' * 75)
                print('=' * 75)

            case 5:
                print('-' * 75)
                v = input('Enter Contact ID to remove: ')
                if v in contacts:
                    del contacts[v]
                    print('Contact has been deleted successfully.')
                else:
                    print('Contact ID not found.')
                print('=' * 75)

            case 6:
                print('-' * 75)
                v = input('Enter Contact ID to search: ')
                if v in contacts:
                    val = contacts[v]
                    print('Contact ID :', v)
                    print('Name       :', val[0])
                    print('Phone No   :', val[1])
                    print('Email ID   :', val[2])
                else:
                    print('Contact ID not found.')
                print('=' * 75)

            case 7:
                print('*' * 75)
                print('All contact data has been preserved.')
                print('THANK YOU FOR USING CONTACT BOOK')
                print('*' * 75)
                sys.exit(0)

if __name__ == '__main__':
    main()
