import pandas as pd
d1={'ROLLNO':[],'NAME':[],'COURSE':[],'FEES':[]}
#ADD A RECORD:

ROLLNO=int(input('ENTER YOUR ROLL NO'))
NAME=input('ENTER YOUR NAME')
COURSE=input('ENTER YOUR course')
FEES=int(input('ENTER YOUR FEES'))
df=pd.DataFrme(d1)
df.loc[len(df)]=[ROLLNO,NAME,COURSE,FEES]
#SEARCH RECORD:
Rno=int(input('ENTER YOUR ROLL NO'))
result=df[df['ROLLNO']==RNO]
if result.empty:
    print('no record found')
else:
    print("result found")
    print(result)
#REMOVE DATA:


#REMOVE FROM LOC:
Rno=int(input('ENTER YOUR ROLL NO'))
result=df.loc[df['ROLLNO']==RNO,['NAME','COURSE']]
if result.empty:
    print('no record found')
else:
    df=df[df['ROLLNO']!=rno]
    print(df)

#SEARCH SPECIFIC DATA:
Rno=int(input('ENTER YOUR ROLL NO'))
result=df[df['ROLLNO']==RNO,['NAME','COURSE']]
if result.empty:
    print('no record found')
else:
    df=df[df['ROLLNO']!=rno]
result=df.loc[:,['NAME','COURSE']]
print(result)
              
           








    




    











             
