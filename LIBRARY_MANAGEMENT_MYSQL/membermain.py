import mysql.connector as m1
import membershipno
import smtplib
from datetime import datetime, date, timedelta
from db_config import get_connection
from email_config import SENDER_EMAIL, SENDER_PASSWORD

def genmember():
    con = get_connection()
    while True:
        print('****[MEMBERS MENUE]****')
        print('1.ADD MEMBER')
        print('2.DLETE MEMBER')
        print('3.CHANGE NAME')
        print('4.DISPLAY ALL RECORDS')
        print('5.SEARCH MEMBER')
        print('6.RETURN TO THE MAIN MENUE')
        print('-'*75)
        try:
            ch=int(input('ENTER YOUR CHOISE:'))
        except ValueError:
            print('Please enter a valid number')
            continue
        print('-'*75)
        match ch:
            case 1:
                mem=membershipno.genAcno()
                name=input('ENTER YOUR NAME:')
                date1=date.today()
                print('JOINING DATE',date1)
                receiver_email= input("ENTER RECIVER EMAIL: ")
                print('YOUR MEMBERSHIP ID IS :',mem)
                subject = "THANK YOU FOR JOINING IN LIBRARY"
                message = f"""Thank you for being a valuable customer in our library.
                - HERE ARE YOUR REGISTRATION DETAILS:
                - REGISTERED NAME: {name}
                - DATE OF JOINING: {date1}
                - REGISTERED EMAIL ADDRESS: {receiver_email}"""
                text = f"Subject: {subject}\n\n{message}"
                try:
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    print("SENDING GMAIL...")
                    server.starttls() 
                    server.login(SENDER_EMAIL, SENDER_PASSWORD)
                    server.sendmail(SENDER_EMAIL, receiver_email, text)
                    print(f"EMAIL SUCCESFULLY SEND TO:{receiver_email}!")
                except Exception as e:
                    print(f"\nFailed to send email. Error: {e}")
                finally:
                    try:
                        server.quit()
                    except:
                        pass
                qry="insert into library values('{}','{}','{}','{}')".format(mem,name,date1,receiver_email)
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
                mem=input('ENTER YOUR MEMBERSHIP ID:')
                qry="delete from library where membership='{}'".format(mem)
                cursor=con.cursor()
                cursor.execute(qry)
                if cursor.rowcount>0:
                    print('record deleted')
                    print('-'*75)
                else:
                    print('record not found')
                    print('-'*75)
                con.commit()
            case 3:
                mem=input('ENTER YOUR MEMBERSHIP ID:')
                name=input('ENTER YOUR NEW NAME:')
                qry="update library set name='{}' where membership='{}'".format(name,mem)
                cursor=con.cursor()
                cursor.execute(qry)
                if cursor.rowcount>0:
                    print('record updated')
                    print('-'*75)
                else:
                    print('record not updated')
                    print('-'*75)
                con.commit()
            case 4:
                qry="select * from library"
                cursor=con.cursor()
                cursor.execute(qry)
                rows=cursor.fetchall()
                for i in rows:
                    print('-'*75)
                    print('MEMBERSHIP NO:',i[0])
                    print('NAME:',i[1])
                    print('JOINING DATE:',i[2])
                    print('EMAIL:',i[3])
                    print('-'*75)
            case 5:
                mem=input('ENTER MEMBERSHIP ID:')
                qry="select * from library where membership='{}'".format(mem)
                cursor=con.cursor()
                cursor.execute(qry)
                rows=cursor.fetchall()
                for i in rows:
                    print('-'*75)
                    print('MEMBERSHIP NO:',i[0])
                    print('NAME:',i[1])
                    print('JOINING DATE:',i[2])
                    print('EMAIL:',i[3])
                    print('-'*75)
            case 6:
                con.commit()
                con.close()
                return
