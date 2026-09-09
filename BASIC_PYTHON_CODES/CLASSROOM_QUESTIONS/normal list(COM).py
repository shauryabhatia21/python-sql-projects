student = []
while True:
    eno=int(input('enter your enrollment no'))
    name=input('enter student name')
    course=input('enter course name')
    fee=int(input('enter fees is'))
    a1=[eno,name,course,fee]
    student.append(a1)
    x=input("do u want to entermore")
    if x=='no':
        break
for x in student:
    print('Eno is',x[0])
    print('Name is',x[1])
    print('Course is',x[2])
    print('Fee is',x[3])
    print('='*50)
   

