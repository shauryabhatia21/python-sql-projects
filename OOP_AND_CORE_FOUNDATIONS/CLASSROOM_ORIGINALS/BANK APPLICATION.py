"""
Interactive Bank Account Management System (Object-Oriented Programming)
Author: Shaurya Bhatia (Bennett University)
--------------------------------------------------------------------------------
Demonstrates:
- Encapsulation of account state (accno, name, acctype, balance) inside Bankacc class
- Dynamic account number generator with 'SBI' prefix
- Real-time balance operations: deposit, withdrawal validation, enquiry
- In-memory customer repository management with CLI menu loop
"""

import sys
import random


class Bankacc:
    """Class representing a customer's bank account."""
    def __init__(self, name, acctype, balance):
        self.accno = self.genAcno()
        self.name = name
        self.acctype = acctype
        self.balance = balance

    def genAcno(self):
        """Generates an SBI account identifier with 4 randomized digits."""
        a = random.randint(0, 9)
        b = random.randint(0, 9)
        c = random.randint(0, 9)
        d = random.randint(0, 9)
        accno = 'SBI' + str(a) + str(b) + str(c) + str(d)
        return accno

    def show(self):
        """Displays full account details."""
        print('Account No   :', self.accno)
        print('Customer Name:', self.name)
        print('Account Type :', self.acctype)
        print('Balance (INR):', self.balance)
        print('=' * 50)

    def deposit(self, a):
        """Deposits funds into the account."""
        if a <= 0:
            print("Deposit amount must be positive.")
            return
        self.balance = self.balance + a
        print(f"Amount deposited successfully. Current balance: INR {self.balance}")
        print('=' * 50)

    def withdraw(self, a):
        """Withdraws funds after validating sufficient balance."""
        if a <= 0:
            print("Withdrawal amount must be positive.")
            return
        if a <= self.balance:
            self.balance = self.balance - a
            print(f"Amount withdrawn successfully. Current balance: INR {self.balance}")
        else:
            print("Transaction Rejected: Insufficient balance.")
        print('=' * 50)

    def Getaccno(self):
        return self.accno

    def Getbalance(self):
        return self.balance


def main():
    # Pre-populate sample account
    customer = [Bankacc('Shaurya Bhatia', 'Savings', 25000)]
    
    while True:
        print("\n" + "=" * 50)
        print("          STATE BANK OF INDIA - OOP PORTAL          ")
        print("=" * 50)
        print('1. Open Account')
        print('2. Deposit Money')
        print('3. Withdraw Money')
        print('4. Enquire Account')
        print('5. Display All Accounts')
        print('6. Exit')
        print("=" * 50)

        try:
            choice = int(input('Enter choice (1-6): '))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue

        if choice == 1:
            name = input('Enter customer name: ')
            acctype = input('Enter account type (Savings/Current): ')
            try:
                balance = int(input('Enter initial opening balance: '))
            except ValueError:
                print("Invalid balance amount. Account creation aborted.")
                continue
            
            new_acc = Bankacc(name, acctype, balance)
            customer.append(new_acc)
            print("\n--- Account Created Successfully ---")
            new_acc.show()

        elif choice == 2:
            acno = input('Enter account number: ').strip().upper()
            found = False
            for acc in customer:
                if acc.Getaccno() == acno:
                    found = True
                    try:
                        amount = int(input('Enter amount to deposit: '))
                        acc.deposit(amount)
                    except ValueError:
                        print("Invalid amount.")
                    break
            if not found:
                print(f"Error: Account '{acno}' not found.")

        elif choice == 3:
            acno = input('Enter account number: ').strip().upper()
            found = False
            for acc in customer:
                if acc.Getaccno() == acno:
                    found = True
                    try:
                        amount = int(input('Enter amount to withdraw: '))
                        acc.withdraw(amount)
                    except ValueError:
                        print("Invalid amount.")
                    break
            if not found:
                print(f"Error: Account '{acno}' not found.")

        elif choice == 4:
            acno = input('Enter account number to enquire: ').strip().upper()
            found = False
            for acc in customer:
                if acc.Getaccno() == acno:
                    found = True
                    print("\n--- Account Details ---")
                    acc.show()
                    break
            if not found:
                print(f"Error: Account '{acno}' not found.")

        elif choice == 5:
            if not customer:
                print("No accounts exist currently.")
            else:
                print(f"\n--- Total Accounts Registered: {len(customer)} ---")
                for acc in customer:
                    acc.show()

        elif choice == 6:
            print("Thank you for banking with State Bank of India. Goodbye!")
            sys.exit(0)

        else:
            print("Invalid choice. Please select an option between 1 and 6.")


if __name__ == "__main__":
    main()
