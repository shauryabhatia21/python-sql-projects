import sys
import accgenerator
customer={}
print('**WELCOME IN KOTAK MAHINDRA BANK**')
print('1.[add account]')
print('2.[deposite money]')
print('3.[withdraw money]')
print('4.[search account]')
print('5.[close account]')
print('6.[display all data]')
print('7.[transfer money]')
print('8.[exit]')
while True:
    ch=int(input('*ENTER YOUR CHOISE*'))
    match ch:

        case 1:
            print('-'*75)
            name=input('Enter Customer Name')
            print('1.SAVING ACCOUNT')
            print('2.CURRENT ACCOUNT')
            op=int(input('Enter Youre Choise'))
            match op:
                case 1:
                    typ=('SAVING ACCOUNT')
                    bal=15000
                case 2:
                    typ=('CURRENT ACCOUNT')
                    bal=30000
            print(typ)
            acc=accgenerator.genAcno()
            print('Your Account Number',acc)
            customer[acc]=[name,typ,bal]
            print('Data Succesfully Uploaded')
            print('='*75)
        case 2:
            print('-'*75)
            v=input('Enter Account Number')
            for x in customer:
                if v==x:
                    amount=int(input('Enter Amount You Want To Deposit'))
                    customer[x][2]=customer[x][2]+amount
                    print('-'*75)
                    print('Updated Balance is',customer[x][2])
                    print('Account Balance Updated Succesfully')
                    print('='*75)
                    break
            else:
                print('Record Not Found')
                print('-'*75)
                
        case 3:
            print('-'*75)
            v=input('Enter Account Number')
            for x in customer:
                if v==x:
                    amount=int(input('Enter Amount You Want To Withdraw'))
                    if amount<=customer[x][2]:
                        customer[x][2]=customer[x][2]-amount
                        print('-'*75)
                        print('Updated Balance Is',customer[x][2])
                        print('Account Balance Updated Succesfully')
                    else:
                        print('insufficient balance')
                        print('-'*75)
                    
                    print('='*75)
                    break
            else:
                print('Record Not Found')
                print('-'*75)
                
        case 4:
            print('-'*75)
            v=input('Enter Account Number')
            for x in customer:
                if v==x:
                    print('Custmer Name',customer[x][0])
                    print('Account Type',customer[x][1])
                    print('Account Balance',customer[x][2])
                    print('All Information Displayed')
                    print('='*75)
                    break
            else:
                print('Record Not Found')
                print('-'*75)
        case 5:
            print('-'*75)
            v=(input('Enter Account Number'))
            for x in customer:
                if v==x:
                    customer.pop(x)
                    print('Bank Account Hass Been Closed')
                    print('='*75)
                    break
        case 6:
            print('-'*75)
            for x in customer:
                print('Account Number')
                print('Name Is',customer[x][0])
                print('Account Type Is',customer[x][1])
                print('balance is',customer[x][2])
                print('All customer information Printed')
                print('-'*75)
        case 7:
            print('-'*75)
            v=(input("Enter Sender's Account Number"))
            for x in customer:
                if v==x:
                    amo=int(input('Enter Transfer Amount'))
                    if amo<=customer[x][2]:
                        customer[x][2]=customer[x][2]-amo
                        print('updated amount',customer[x][2])
                        r=(input("Enter Receiver's Account Number"))
                        for y in customer:
                                if r==y:
                                    customer[y][2]=customer[y][2]+amo
                                    print("Amount Transfered successfully")
                                    break
                        else:
                            print("receiver's Record Not Found")
                            print('-'*75)
                    else:
                        print('insufficient balance')
                        print('-'*75)
                    break
            else:
                print('Record Not Found')
                print('-'*75)
        case 8:
            print('*'*75)
            print('The Data Has Been Stored')
            print('THANK YOU FOR BANKING WITH US')
            print('*'*75)
            sys.exit(0)
                         
                    
                              
                
                
                
                    
                    
                    
                
            
            
        

