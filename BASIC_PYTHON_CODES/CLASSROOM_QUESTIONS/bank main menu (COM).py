import sys
import accgenerator
customer=[]
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
                case 2:
                    typ=('CURRENT ACCOUNT')
            print(typ)
            bal=int(input('Enter Account Balance'))
            acc=accgenerator.genAcno()
            print('Your Account Number',acc)
            a1=[acc,name,typ,bal]
            customer.append(a1)
            print('Data Succesfully Uploaded')
            print('='*75)
        case 2:
            print('-'*75)
            v=input('Enter Account Number')
            for x in customer:
                if v==x[0]:
                    amount=int(input('Enter Amount You Want To Deposit'))
                    x[3]=x[3]+amount
                    print('-'*75)
                    print('Updated Balance is',x[3])
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
                if v==x[0]:
                    amount=int(input('Enter Amount You Want To Withdraw'))
                    x[3]=x[3]-amount
                    print('-'*75)
                    print('Updated Balance Is',x[3])
                    print('Account Balance Updated Succesfully')
                    print('='*75)
                    break
            else:
                print('Record Not Found')
                print('-'*75)
                
        case 4:
            print('-'*75)
            v=(input('Enter Account Number'))
            for x in customer:
                if v==x[0]:
                    print('Custmer Name',x[1])
                    print('Account Type',x[2])
                    print('Account Balance',x[3])
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
                if v==x[0]:
                    a1.clear()
                    print('Bank Account Hass Been Closed')
                    print('='*75)
                    break
        case 6:
            print('-'*75)
            for x in customer:
                print('Account Number',x[0])
                print('Name Is',x[1])
                print('Account Type Is',x[2])
                print('balance is',x[3])
                print('All customer information Printed')
                print('-'*75)
        case 7:
            print('-'*75)
            v=(input("Enter Sender's Account Number"))
            for x in customer:
                if v==x[0]:
                    amo=int(input('Enter Transfer Amount'))
                    if amo<=x[3]:
                        x[3]=x[3]-amo
                        print('updated amount',x[3])
                        r=(input("Enter Receiver's Account Number"))
                        for y in customer:
                                if r==y[0]:
                                    y[3]=y[3]+amo
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
                         
                    
                              
                
                
                
                    
                    
                    
                
            
            
        
