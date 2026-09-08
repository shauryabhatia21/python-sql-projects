from tkinter import *
from tkinter import messagebox
import mysql.connector as m1
import os

# Database connection details (replace with your password):
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'YOUR_PASSWORD')
DB_NAME = os.getenv('DB_NAME', 'ots')

def get_connection():
    return m1.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)

def addRec():
    try:
        con = get_connection()
        if con.is_connected():
            eno1 = eno.get()
            name1 = name.get()
            course1 = course.get()
            fees1 = fees.get()

            if eno1 == 0 or name1 == '':
                messagebox.showwarning("Input Error", "Please enter Enrollment Number and Name")
                return

            qry = "insert into student values({},'{}','{}',{})".format(eno1, name1, course1, fees1)
            cursor = con.cursor()
            cursor.execute(qry)
            if cursor.rowcount > 0:
                print("record added")
                print('-'*75)
                messagebox.showinfo("Success", "Record added successfully!")
                # Reset fields
                eno.set(0)
                name.set('')
                course.set('')
                fees.set(0)
            else:
                print("record not added")
                print('-'*75)
                messagebox.showerror("Error", "Record could not be added")
            con.commit()
            con.close()
    except Exception as e:
        print('Connection or Query Error:', e)
        messagebox.showerror("Database Error", f"Error: {e}")

root = Tk()
eno = IntVar()
name = StringVar()
course = StringVar()
fees = IntVar()

root.title("STUDENT ADMISSION WINDOW")
root.minsize(450, 420)
root.maxsize(450, 420)

Label(root, text="STUDENT REGISTRATION FORM", font=("BOLD", 14), pady=10).pack()

lbleno = Label(root, text="ENTER YOUR ENROLLMENT NUMBER", font=("BOLD", 11)).pack(pady=4)
txteno = Entry(root, textvariable=eno, font=("Arial", 11)).pack(pady=4)

lblname = Label(root, text='ENTER YOUR NAME', font=("BOLD", 11)).pack(pady=4)
txtname = Entry(root, textvariable=name, font=("Arial", 11)).pack(pady=4)

lblcourse = Label(root, text='ENTER COURSE NAME', font=("BOLD", 11)).pack(pady=4)
txtcourse = Entry(root, textvariable=course, font=("Arial", 11)).pack(pady=4)

lblfees = Label(root, text='ENTER YOUR FEES', font=("BOLD", 11)).pack(pady=4)
txtfees = Entry(root, textvariable=fees, font=("Arial", 11)).pack(pady=4)

bt1 = Button(root, text="SAVE RECORD", font=('BOLD', 11), bg='#4CAF50', fg='white', padx=20, pady=5, command=addRec).pack(pady=15)

root.mainloop()
