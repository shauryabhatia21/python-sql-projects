import sys
import accgenerator
student={}
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
            eno=accgenerator.genAcno()
            name=input('enter student name =')
            course=input('enter course name =')
            fee=int(input('enter fees is ='))
            student[eno]=[name,course,fee]
            print('your enrollment number is',eno)
            print("Student add successfully")
            print('='*75)
            
        case 2:
            y=input('enter enrollment no')
            for z in student:
                if y==z:
                    name1=input('enter new name')
                    student[z][0]=name1
                    print("Record updated")
                    break
            else:
                print('enrollment number not exist')
            print('='*75)
        case 3:
            eno=input('enter your enrollment no =')
            for y in student:
                if eno==y:
                    print('Name is',student[y][0])
                    print('Course is',student[y][1])
                    print('Fee is',student[y][2])
                    break
            else:
                print('enrollment number not exist')
            print('='*75)
        case 4:
            eno=input('enter your enrollment no =')
            for z in student:
                if eno==z:
                    name1=input('enter student name =')
                    course1=input('enter course name =')
                    fee1=int(input('enter fees is ='))
                    student[z][0]=name1
                    student[z][1]=course1
                    student[z][2]=fee1
                    print('record updated')
                    break
            else:
                print('record not found')

        case 5:
            for y in student:
                print('Name is',student[y][0])
                print('Course is',student[y][1])
                print('Fee is',student[y][2])
                print('-'*75)
            print('all student name printed')
            print('='*75)
        case 6:
            eno=input('enter your enrollment number')
            for y in student:
                if eno==y:
                    student.pop(y)
                    print('record updated')
                    break
            else:
                print('record not found')

        case 7:
            print('the data has been stored')
            print('THANK YOU FOR VISIT')
            sys.exit(0)
            
            
    
       
