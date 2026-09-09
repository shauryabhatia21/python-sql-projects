import phoneidgenerator
import sys
customer={}
print('**contact list***')
print('1.add new contact list')
print('2.change phone number')
print('3.chnage email address')
print('4.show all data')
print('5.remove coustomer')
print('6.search contact list')
print('7.exit')
while True:
    print('-'*75)
    ch=int(input("enter your choise="))
    match ch:
        case 1:
            print('-'*75)
            idd=phoneidgenerator.genphon()
            name=input('enter your name=')
            phone=int(input('enter your mobile no='))
            email=input('enter your mail id=')
            print('your contact id=',idd)
            customer[idd]=[name,phone,email]
        case 2:
            v=input('enter phone id')
            for x in customer:
                if v==x:
                    phone1=input('enter new phone no')
                    customer[x][1]=phone1
                    print('name updated succesfully')
        case 3:
            print('-'*75)
            v=input('enter phone id')
            for x in customer:
                if v==x:
                    mail1=input('enter new mail id')
                    customer[x][2]=mail1
                    print('name updated succesfully')
        case 4:
            print('-'*75)
            for x in customer:
                print('name',customer[x][0])
                print('phone no is',customer[x][1])
                print('email id is',customer[x][2])
                print('.'*75)
                
        case 5:
            print('-'*75)
            v=input('enter phone id')
            for x in customer:
                if v==x:
                    customer.pop(x)
                    print('LIST HASS BEEN  Closed')
                    print('='*75)
                    break
        case 6:
            print('-'*75)
            v=input('enter phone id')
            for x in customer:
                if v==x:
                    print('name',customer[x][0])
                    print('phone no',customer[x][1])
                    print('email id',customer[x][2])
                    print('-'*75)
        case 7:
            print('*'*75)
            print('The Data Has Been Stored')
            print('*'*75)
            sys.exit(0)
            
            
            
        
