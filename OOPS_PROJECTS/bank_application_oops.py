# OBJECT ORIENTED BANKING APPLICATION (OOP)
# Implements Bankacc class with auto-generated account numbers, deposit, withdrawal, enquiry, and customer records

import sys
import random

class Bankacc:
    def __init__(self, name, acctype, balance):
        self.accno = self.genAcno()
        self.name = name
        self.acctype = acctype
        self.balance = balance

    def genAcno(self):
        a = random.randint(0, 9)
        b = random.randint(0, 9)
        c = random.randint(0, 9)
        d = random.randint(0, 9)
        return 'SBI' + str(a) + str(b) + str(c) + str(d)

    def show(self):
        print('Account No   :', self.accno)
        print('Name         :', self.name)
        print('Account Type :', self.acctype)
        print('Balance      :', self.balance)
        print('=' * 50)

    def deposit(self, a):
        self.balance = self.balance + a
        print('Amount deposited successfully.')
        print('Current Balance is:', self.balance)

    def withdraw(self, a):
        if a <= self.balance:
            self.balance = self.balance - a
            print('Amount withdrawn successfully.')
            print('Current Balance is:', self.balance)
        else:
            print('Error: Insufficient balance in account!')

    def Getaccno(self):
        return self.accno

    def Getbalance(self):
        return self.balance


customer = []

def main():
    while True:
        print("\n" + "=" * 50)
        print("         *** SBI BANK MANAGEMENT (OOP) ***")
        print("=" * 50)
        print('1. Open Account')
        print('2. Deposit Money')
        print('3. Withdraw Money')
        print('4. Enquire Account')
        print('5. Display All Accounts')
        print('6. Exit')
        print('-' * 50)
        
        try:
            choice = int(input('Enter your choice (1-6): '))
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue

        if choice == 1:
            name = input('Enter customer name: ')
            acctype = input('Enter account type (savings/current): ')
            balance = int(input('Enter opening balance: '))
            cus1 = Bankacc(name, acctype, balance)
            customer.append(cus1)
            print('-' * 50)
            print('Account Created Successfully!')
            print('Your Account Number is:', cus1.Getaccno())
            print('Customer Name:', name)
            print('Account Type:', acctype)
            print('Opening Balance:', balance)
            print('=' * 50)

        elif choice == 2:
            acno = input('Enter account number: ')
            found = False
            for x in customer:
                if x.Getaccno() == acno:
                    a = int(input('Enter amount to deposit: '))
                    x.deposit(a)
                    found = True
                    break
            if not found:
                print('Error: No account found with account number:', acno)

        elif choice == 3:
            acno = input('Enter account number: ')
            found = False
            for x in customer:
                if x.Getaccno() == acno:
                    a = int(input('Enter amount to withdraw: '))
                    x.withdraw(a)
                    found = True
                    break
            if not found:
                print('Error: No account found with account number:', acno)

        elif choice == 4:
            acno = input('Enter account number to enquire: ')
            found = False
            for x in customer:
                if x.Getaccno() == acno:
                    print('-' * 50)
                    x.show()
                    found = True
                    break
            if not found:
                print('Error: No account found with account number:', acno)

        elif choice == 5:
            if not customer:
                print("No accounts registered yet.")
            else:
                print('-' * 50)
                print(f"Total Accounts: {len(customer)}")
                print('-' * 50)
                for x in customer:
                    x.show()

        elif choice == 6:
            print('Thank you for banking with us! Have a great day.')
            sys.exit(0)
        else:
            print("Invalid choice! Please select between 1 and 6.")

if __name__ == '__main__':
    main()
