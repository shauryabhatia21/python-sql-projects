from Books_module import booksMenu
from members_module import memberMenu
from issue_module import transactionMenu
import sys

def mainMenu():
    while True:
        print('=================================')
        print('--- LIBRARY MANAGEMENT SYSTEM ---')
        print('=================================')
        print('1. Go to Book Menu')
        print('2. Go to Member Menu')
        print('3. Go to Issue / Return Menu')
        print('4. Exit')
        try:
            ch=int(input('Enter your choice: '))
        except ValueError:
            print('Please enter a valid number')
            continue

        if ch==1:
            booksMenu()
        elif ch==2:
            memberMenu()
        elif ch==3:
            transactionMenu()
        elif ch==4:
            print('Thank you for using Library Management System!')
            sys.exit(0)
        else:
            print('Invalid choice, try again.')

if __name__ == '__main__':
    mainMenu()
