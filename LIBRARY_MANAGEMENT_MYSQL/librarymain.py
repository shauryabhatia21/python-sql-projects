import mysql.connector as m1
import bookid
from db_config import get_connection

def genlibrary():
    con = get_connection()
    while True:
        print('[****BOOKS MENUE****]')
        print('1.ADD BOOK')
        print('2.DELETE BOOK')
        print('3.CHANGE BOOK')
        print('4.DISPLAY ALL BOOK RECORDS')
        print('5.SEARCH BOOK')
        print('6.RETURN TO MAIN MENUE')
        print('-'*75)
        try:
            ch=int(input('ENTER YOUR CHOISE:'))
        except ValueError:
            print('Please enter a valid number')
            continue
        print('-'*75)
        match ch:
            case 1:
                id=bookid.genbook()
                book=input('ENTER YOUR BOOK NAME:')
                avability=int(input('ENTER NO OF BOOK AVALABLE:'))
                print('your book id is:',id)
                qry="insert into books values('{}','{}',{})".format(id,book,avability)
                cursor=con.cursor()
                cursor.execute(qry)
                if cursor.rowcount>0:
                    print("record added")
                    print('-'*75)
                else:
                    print("record not added")
                    print('-'*75)
                con.commit()
            case 2:
                mem=input('ENTER BOOK ID:')
                qry="delete from books where id='{}'".format(mem)
                cursor=con.cursor()
                cursor.execute(qry)
                if cursor.rowcount>0:
                    print("record deleted")
                    print('-'*75)
                else:
                    print("record not found")
                    print('-'*75)
                con.commit()
            case 3:
                mem=input('ENTER BOOK ID:')
                books=input('ENTER NEW BOOK:')
                qry="update books set bookname='{}' where id='{}'".format(books,mem)
                cursor=con.cursor()
                cursor.execute(qry)
                if cursor.rowcount>0:
                    print("record updated")
                    print('-'*75)
                else:
                    print("record not updated")
                    print('-'*75)
                con.commit()
            case 4:
                qry="select * from books"
                cursor=con.cursor()
                cursor.execute(qry)
                rows=cursor.fetchall()
                for i in rows:
                    print('-'*75)
                    print('BOOK ID:',i[0])
                    print('BOOK NAME:',i[1])
                    print('AVALABILITY:',i[2])
                    print('-'*75)
            case 5:
                mem=input('ENTER BOOK ID:')
                qry="select * from books where id='{}'".format(mem)
                cursor=con.cursor()
                cursor.execute(qry)
                rows=cursor.fetchall()
                for i in rows:
                    print('-'*75)
                    print('BOOK ID:',i[0])
                    print('BOOK NAME:',i[1])
                    print('AVALABILITY:',i[2])
                    print('-'*75)
            case 6:
                con.commit()
                con.close()
                return
