import sys
import issuemain
import librarymain
import membermain

while True:
    print('***[LIBRARY MAIN MENUE]****')
    print('1.OPEN MEMBERS TAB')
    print('2.OPEN BOOKS TAB')
    print('3.OPEN BOOK ISSUE TAB ')
    print('4.EXIT')
    print('-'*75)
    try:
        ch=int(input('ENTER YOUR CHOISE:'))
    except ValueError:
        print('Please enter a valid number')
        continue
    match ch:
        case 1:
            print('-'*75)
            membermain.genmember()
            print('-'*75)
        case 2:
            print('-'*75)
            librarymain.genlibrary()
            print('-'*75)
        case 3:
            print('-'*75)
            issuemain.genissue1()
            print('-'*75)
        case 4:
            print('*'*75)
            print('YOUR DATA HAS BEEN STORED')
            print('*'*75)
            sys.exit()
