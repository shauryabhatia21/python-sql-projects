student={}
while True:
    eno=int(input('enter your enrollment no'))
    name=input('enter student name')
    course=input('enter course name')
    fee=int(input('enter fees is'))
    student[eno]=[name,course,fee]
    x=input("do u want to entermore")
    if x=='no':
        break
for y in student:
    print('eno',student[y])
    print('name',student[y][0])
    print('course',student[y][1])
    print('fee',student[y][2])
    
    print('='*50)

    
    
