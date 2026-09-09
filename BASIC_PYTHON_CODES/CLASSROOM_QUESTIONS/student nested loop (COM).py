import sys
student=[]
while True:
    print('***main menue***')
    print('1.add a student')
    print('2.rename student')
    print('3.serch student')
    print('4.modify student')
    print('5.display all student')
    print('6 remove student')
    print('7.exit')
    ch=int(input('enter your choise ='))
    print('-'*75)
    match ch:
        case 1:
            eno=int(input('enter your enrollment no ='))
            name=input('enter student name =')
            course=input('enter course name =')
            fee=int(input('enter fees is ='))
            a1=[eno,name,course,fee]
            student.append(a1)
            print("Student add successfully")
            print('='*75)
        case 2:
            y=int(input('enter enrollment no'))
            for z in student:
                if y==z[0]:
                    name1=input('enter new name')
                    z[1]=name1
                    print("Record updated")
                    break

            else:
                print('enrollment number not exist')
            print('='*75)
        case 3:
            eno=int(input('enter your enrollment no ='))
            for x in student:
                if eno==x[0]:
                    print('Eno is',x[0])
                    print('Name is',x[1])
                    print('Course is',x[2])
                    print('Fee is',x[3])
                    break
            else:
                print('enrollment number not exist')
            print('='*75)
        case 4:
            eno=int(input('enter your enrollment no ='))
            for x in student:
                if eno==x[0]:
                    name1=input('enter student name =')
                    course1=input('enter course name =')
                    fee1=int(input('enter fees is ='))
                    x[1]=name1
                    x[2]=course1
                    x[3]=fee1
                    print('record updated')
                    break
            else:
                print('record not found')

        case 5:
            for x in student:
                print('Eno is',x[0])
                print('Name is',x[1])
                print('Course is',x[2])
                print('Fee is',x[3])
            print('all student name printed')
            print('='*75)
        case 6:
            eno=int(input('enter your enrollment number'))
            for x in student:
                if eno==x[0]:
                    student.remove(x)
                    print('record updated')
                    break
            else:
                print('record not found')

        case 7:
            print('the data has been stored')
            print('THANK YOU FOR VISIT')
            sys.exit(0)
            
            
    
       
