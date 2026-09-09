#MAIN MENUE:
import pandas as pd
import sys
d1={'RNO':[],'NAME':[],'COURSE':[],'FEES':[]}
df=pd.DataFrame(d1)
while True:
    print('1.ADD STUDENT')
    print('2.REMOVE STUDENT')
    print('3.search student')
    print('4.search student by a given double critrieao')
    print('5.display all record by specific coloum')
    print('6.display all records from specific index to given index')
    print('7.display all records from specific index to given index and ')
    print('8.deleate the ecord by drop method')
    print('9.modify course of a particular coloum')
    print('10.modify course of many student')
    print('11.to add a new coloum fees')
    print("12.to add a new coloum fees with a spefic value")
    print("13.to add a new coloum fees with a different value")
    print('14to add a new coloum fees and set the value of particular colomn')
    print('15.display all')
    print('16.exit')
    ch=int(input('enter your choise'))
    match ch:
        case 1:
            RNO=int(input('ENTER YOUR ROLL NO'))
            NAME=input('ENTER YOUR NAME')
            COURSE=input('ENTER YOUR course')
            FEES=int(input('ENTER YOUR FEES'))
            df=pd.DataFrame(d1)
            df.loc[len(df)]=[RNO,NAME,COURSE,FEES]
            print('-'*75)
            print(df)
            print('-'*75)
        case 2:
            RNO=int(input('ENTER YOUR ROLL NO'))
            result=df.loc[df['RNO']==RNO]
            if result.empty:
                print('no record found')
            else:
                df=df[df[RNO]!=rno]
                result=df.loc[:,['NAME','COURSE']]
                print(result)
        case 3:
            RNO=int(input('ENTER YOUR ROLL NO'))
            result=df[df['RNO']==RNO]
            if result.empty:
                print('no record found')
            else:
                print("result found")
                print(result)
        case 4:
            Rno=int(input('ENTER YOUR ROLL NO'))
            result=df[df['ROLLNO']==RNO,['NAME','COURSE']]
            if result.empty:
                print('no record found')
            else:
                df=df[df[RNO]!=rno]
            result=df.loc[:,['NAME','COURSE']]
            print('-'*75)
            print(result)
            print('-'*75)
        case 5:
            Rno=int(input('ENTER YOUR ROLL NO'))
            result=df.loc[df[:['ROLLNO']==RNO,['NAME','COURSE']]]
            if result.empty:
                print('no record found')
            else:
               df=df[df[RNO]!=rno]
               print('-'*75)
               print('record remove')
               print('-'*75)

        case 15:
            pass
          
          
          
