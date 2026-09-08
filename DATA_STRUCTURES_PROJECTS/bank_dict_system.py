# KOTAK MAHINDRA BANK MANAGEMENT SYSTEM (DICTIONARY DATA STRUCTURE)
# Features: Add account, Deposit, Withdraw, Search, Close account, Display all, Inter-account money transfer

import sys
import generators

customer = {}

def main():
    print('** WELCOME TO KOTAK MAHINDRA BANK **')
    while True:
        print("\n" + "=" * 50)
        print('1. [Add Account]')
        print('2. [Deposit Money]')
        print('3. [Withdraw Money]')
        print('4. [Search Account]')
        print('5. [Close Account]')
        print('6. [Display All Accounts]')
        print('7. [Transfer Money]')
        print('8. [Exit]')
        print("-" * 50)

        try:
            ch = int(input('* ENTER YOUR CHOICE * : '))
        except ValueError:
            print("Invalid input! Please enter an integer.")
            continue

        match ch:
            case 1:
                print('-' * 75)
                name = input('Enter Customer Name: ')
                print('1. SAVING ACCOUNT')
                print('2. CURRENT ACCOUNT')
                op = int(input('Enter Your Choice (1 or 2): '))
                match op:
                    case 1:
                        typ = 'SAVING ACCOUNT'
                        bal = 15000
                    case 2:
                        typ = 'CURRENT ACCOUNT'
                        bal = 30000
                    case _:
                        typ = 'SAVING ACCOUNT'
                        bal = 10000
                acc = generators.genAcno()
                print('Account Type:', typ)
                print('Your Generated Account Number:', acc)
                customer[acc] = [name, typ, bal]
                print('Data Successfully Uploaded!')
                print('=' * 75)

            case 2:
                print('-' * 75)
                v = input('Enter Account Number: ')
                if v in customer:
                    amount = int(input('Enter Amount You Want To Deposit: '))
                    customer[v][2] += amount
                    print('-' * 75)
                    print('Updated Balance is:', customer[v][2])
                    print('Account Balance Updated Successfully!')
                    print('=' * 75)
                else:
                    print('Record Not Found')
                    print('-' * 75)

            case 3:
                print('-' * 75)
                v = input('Enter Account Number: ')
                if v in customer:
                    amount = int(input('Enter Amount You Want To Withdraw: '))
                    if amount <= customer[v][2]:
                        customer[v][2] -= amount
                        print('-' * 75)
                        print('Updated Balance is:', customer[v][2])
                        print('Account Balance Updated Successfully!')
                    else:
                        print('Error: Insufficient balance!')
                    print('=' * 75)
                else:
                    print('Record Not Found')
                    print('-' * 75)

            case 4:
                print('-' * 75)
                v = input('Enter Account Number: ')
                if v in customer:
                    print('Customer Name   :', customer[v][0])
                    print('Account Type    :', customer[v][1])
                    print('Account Balance :', customer[v][2])
                    print('All Information Displayed')
                    print('=' * 75)
                else:
                    print('Record Not Found')
                    print('-' * 75)

            case 5:
                print('-' * 75)
                v = input('Enter Account Number: ')
                if v in customer:
                    del customer[v]
                    print('Bank Account Has Been Closed Successfully.')
                    print('=' * 75)
                else:
                    print('Record Not Found')
                    print('-' * 75)

            case 6:
                print('-' * 75)
                if not customer:
                    print('No customer accounts on record.')
                else:
                    for acc, details in customer.items():
                        print('Account Number :', acc)
                        print('Customer Name  :', details[0])
                        print('Account Type   :', details[1])
                        print('Balance        :', details[2])
                        print('-' * 75)
                    print('All customer information Printed')
                print('=' * 75)

            case 7:
                print('-' * 75)
                v = input("Enter Sender's Account Number: ")
                if v in customer:
                    amo = int(input('Enter Transfer Amount: '))
                    if amo <= customer[v][2]:
                        r = input("Enter Receiver's Account Number: ")
                        if r in customer:
                            customer[v][2] -= amo
                            customer[r][2] += amo
                            print('-' * 75)
                            print('Amount Transferred Successfully!')
                            print("Sender's Updated Balance is:", customer[v][2])
                            print('=' * 75)
                        else:
                            print("Receiver's Record Not Found")
                            print('-' * 75)
                    else:
                        print('Error: Insufficient balance!')
                        print('-' * 75)
                else:
                    print("Sender's Record Not Found")
                    print('-' * 75)

            case 8:
                print('*' * 75)
                print('The Data Has Been Stored')
                print('THANK YOU FOR BANKING WITH US')
                print('*' * 75)
                sys.exit(0)

if __name__ == '__main__':
    main()
