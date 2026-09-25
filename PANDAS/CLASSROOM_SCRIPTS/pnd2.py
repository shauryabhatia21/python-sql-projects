import pandas as pd

d1 = {'ROLLNO': [], 'NAME': [], 'COURSE': [], 'FEES': []}

# ADD A RECORD:
ROLLNO = int(input('ENTER YOUR ROLL NO: '))
NAME = input('ENTER YOUR NAME: ')
COURSE = input('ENTER YOUR course: ')
FEES = int(input('ENTER YOUR FEES: '))
df = pd.DataFrame(d1)
df.loc[len(df)] = [ROLLNO, NAME, COURSE, FEES]
print(df)

# SEARCH RECORD:
Rno = int(input('ENTER YOUR ROLL NO: '))
result = df[df['ROLLNO'] == Rno]
if result.empty:
    print('no record found')
else:
    print("result found")
    print(result)

# REMOVE FROM LOC:
Rno = int(input('ENTER YOUR ROLL NO: '))
result = df.loc[df['ROLLNO'] == Rno, ['NAME', 'COURSE']]
if result.empty:
    print('no record found')
else:
    df = df[df['ROLLNO'] != Rno]
    print(df)

# SEARCH SPECIFIC DATA:
Rno = int(input('ENTER YOUR ROLL NO: '))
result = df.loc[df['ROLLNO'] == Rno, ['NAME', 'COURSE']]
if result.empty:
    print('no record found')
else:
    print("result found")
    print(result)

