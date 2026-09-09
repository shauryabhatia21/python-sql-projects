a1=[11,22,33,44,55]
print('1.add element at the end')
print('2.add at no at specified position')
print('3.remove from bigning')
print('4.display all the element')
print('5.serch the element')
print('6.remove all the element')
print(a1)
ch=int(input('enter your number'))
match ch:
    case 1:
        n=int(input('enter your number'))
        a1.append(n)
        print('your result is',a1)
    case 2:
        n=int(input('enter your number'))
        a=int(input('enter your number position'))
        print('your result is',a1)
    case 3:
        a1.pop(0)
        print('remove first digit',a1)
    case 4:
        print('print all element',a1)
    case 5:
        n=int(input('enter your number'))
        print(a1[n-1])
    case 6:
        a=a1.clear()
        print(a)

        
        
        
