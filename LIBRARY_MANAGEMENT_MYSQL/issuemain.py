import mysql.connector as m1
import sys
import smtplib
from datetime import datetime, date, timedelta
import issueid
import mytoken
from db_config import get_connection
from email_config import SENDER_EMAIL, SENDER_PASSWORD

def genissue1():
    con = get_connection()
    while True:
        if con.is_connected():
            print('[****ISSUE TAB****]')
            print('1.ISSUE NEW BOOK')
            print('2.RETURN BOOK')
            print('3.SEARCH MEMBER')
            print('4.SHOW ALL DATA')
            print('5.DELETE MEMBER')
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
                    current_date=date.today()
                    mem=input('enter member id:')
                    id=input('enter book id:')
                    qry="select * from library where membership='{}'".format(mem)
                    cursor=con.cursor()
                    cursor.execute(qry)
                    rows=cursor.fetchall()
                    t = 0
                    if not rows:
                        print('you have enter wrong member id')
                    else:
                        for i in rows:
                            if i[0]==mem:
                                qry="select * from books where id='{}'".format(id)
                                cursor=con.cursor()
                                cursor.execute(qry)
                                rows_books=cursor.fetchall()
                                if not rows_books:
                                    print('you have enter wrong book id')
                                else:
                                    for z in rows_books:
                                        if z[0]==id:
                                            t=40
                                        else:
                                            print('you have enter wrong book id')
                            else:
                                print('you have enter wrong member id')
                    if t==40:
                        new=int(input('ENTER DAYS TO BORROW:'))
                        print('BOOKING DATE:',current_date)
                        ten=timedelta(days=new)
                        newdate=current_date+ten
                        print('YOUR DUE DATE WILL BE:',newdate)
                        r=(f'₹{new*10}')
                        m=(f'RS{new*10}')
                        print('YOUR TOTAL COST WILL BE:',r)
                        token=mytoken.gentoken()
                        print('YOUR TOKEN NUMBER:',token)
                        u=30
                    else:
                        u=0
                    if u==30:
                        qry="select * from library where membership='{}'".format(mem)
                        cursor=con.cursor()
                        cursor.execute(qry)
                        rows=cursor.fetchall()
                        ki = ""
                        p = 0
                        for i in rows:
                            ki=i[3]
                            p=10
                        if p==10:
                            receiver_email=ki
                            subject = "THANK YOU FOR BEING CUSTOMER IN OUR LIBRARY"
                            message = f"""YOU BORROW BOOK FROM OUR LIBRARY.
                            - HERE ARE YOUR DETAILS:
                            - MEMBERSHIP ID: {mem}
                            - BOOK ID: {id}
                            - BOOKING DATE: {current_date}
                            - DUE DATE: {newdate}
                            - REGISTERED EMAIL ADDRESS: {receiver_email}
                            - COST: {m}
                            - TOKEN NUMBER: {token}"""
                            text = f"Subject: {subject}\n\n{message}"
                            try:
                                server = smtplib.SMTP('smtp.gmail.com', 587)
                                server.starttls() 
                                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                                server.sendmail(SENDER_EMAIL, receiver_email, text)
                                print(f"EMAIL SUCCESFULLY SEND TO:{receiver_email}!")
                            except Exception as e:
                                print(f"Failed to send email. Error: {e}")
                            finally:
                                try:
                                    server.quit()
                                except:
                                    pass
                        qry="insert into issue values('{}','{}','{}','{}','{}','{}','{}')".format(current_date,mem,id,newdate,ki,token,r)
                        cursor=con.cursor()
                        cursor.execute(qry)
                        if cursor.rowcount>0:
                            print("[record added]")
                        else:
                            print("[record not added]")
                        con.commit()
                case 2:
                    current_date=date.today()
                    mem=input('ENTER YOUR TOKEN NUMBER: ')
                    qry= "select * from issue where token='{}'".format(mem)
                    cursor = con.cursor()
                    cursor.execute(qry)
                    rows = cursor.fetchall()
                    if not rows:
                        print("No records found for the entered Token Number.")
                    else:
                        for i in rows:
                            booking=i[0]
                            due=i[3]
                            amount=i[6]
                            print('_'*75)
                            print('TODAY CURRENT DATE IS:',current_date)
                            print('YOUR BOOKING DATE IS:',booking)
                            print('YOUR DUE DATE IS:',due)
                            print('YOUR BOOKING AMOUNT IS:',amount)
                            if isinstance(due, str):
                                object1=datetime.strptime(due,"%Y-%m-%d").date()
                            else:
                                object1=due
                            if current_date>object1:
                                days=(current_date-object1).days
                                print(f'YOUR RETURN DATE HAS BEEN EXPIRED BY {days} DAYS')
                                fine=days*20
                                print(f'FINE TO BE PAID: ₹{fine}')
                            else:
                                print('BOOK RETURNED WITHIN DUE DATE. NO FINE.')
                            print('_'*75)
                case 3:
                    mem=input('ENTER MEMBER ID:')
                    qry="select * from issue where mem_id='{}'".format(mem)
                    cursor=con.cursor()
                    cursor.execute(qry)
                    rows=cursor.fetchall()
                    for i in rows:
                        print('-'*75)
                        print('BOOKING DATE:',i[0])
                        print('MEMBER ID:',i[1])
                        print('BOOK ID:',i[2])
                        print('DUE DATE:',i[3])
                        print('EMAIL:',i[4])
                        print('TOKEN:',i[5])
                        print('COST:',i[6])
                        print('-'*75)
                case 4:
                    qry="select * from issue"
                    cursor=con.cursor()
                    cursor.execute(qry)
                    rows=cursor.fetchall()
                    for i in rows:
                        print('-'*75)
                        print('BOOKING DATE:',i[0])
                        print('MEMBER ID:',i[1])
                        print('BOOK ID:',i[2])
                        print('DUE DATE:',i[3])
                        print('EMAIL:',i[4])
                        print('TOKEN:',i[5])
                        print('COST:',i[6])
                        print('-'*75)
                case 5:
                    mem=input('ENTER TOKEN NUMBER TO REMOVE:')
                    qry="delete from issue where token='{}'".format(mem)
                    cursor=con.cursor()
                    cursor.execute(qry)
                    if cursor.rowcount>0:
                        print('Record deleted')
                    else:
                        print('Record not found')
                    con.commit()
                case 6:
                    con.close()
                    return
