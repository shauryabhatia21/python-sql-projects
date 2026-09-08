from tkinter import *

root = Tk()
root.title("CALCULATOR")
root.configure(background="lightblue")
root.geometry('420x650+240+40')
root.resizable(False, False)

expression = ""

def btn_click(item):
    global expression
    expression = expression + str(item)
    input_text.set(expression)

def clear():
    global expression
    expression = ""
    input_text.set("")

def calculate():
    global expression
    try:
        # replace 'X' with '*' for python eval
        eval_expr = expression.replace('X', '*').replace('_', '-')
        result = str(eval(eval_expr))
        input_text.set(result)
        expression = result
    except Exception:
        input_text.set("Error")
        expression = ""

input_text = StringVar()

e1 = Entry(root, textvariable=input_text, font=('Arial', 30), width=13, justify='right', highlightthickness=5)
e1.grid(row=0, column=1, columnspan=4, pady=8, padx=10)

# Number Buttons
n0 = Button(root, text='0', font=('Arial', 20), padx=33, pady=33, command=lambda: btn_click('0'))
n1 = Button(root, text='1', font=('Arial', 20), padx=33, pady=33, command=lambda: btn_click('1'))
n2 = Button(root, text='2', font=('Arial', 20), padx=33, pady=33, command=lambda: btn_click('2'))
n3 = Button(root, text='3', font=('Arial', 20), padx=33, pady=33, command=lambda: btn_click('3'))
n4 = Button(root, text='4', font=('Arial', 20), padx=33, pady=33, command=lambda: btn_click('4'))
n5 = Button(root, text='5', font=('Arial', 20), padx=33, pady=33, command=lambda: btn_click('5'))
n6 = Button(root, text='6', font=('Arial', 20), padx=33, pady=33, command=lambda: btn_click('6'))
n7 = Button(root, text='7', font=('Arial', 20), padx=33, pady=33, command=lambda: btn_click('7'))
n8 = Button(root, text='8', font=('Arial', 20), padx=33, pady=33, command=lambda: btn_click('8'))
n9 = Button(root, text='9', font=('Arial', 20), padx=33, pady=33, command=lambda: btn_click('9'))

# Operation Buttons
b1 = Button(root, text='+', font=('Arial', 20), padx=33, pady=33, fg='blue', command=lambda: btn_click('+'))
b2 = Button(root, text='-', font=('Arial', 20), padx=33, pady=33, fg='blue', command=lambda: btn_click('-'))
b3 = Button(root, text='/', font=('Arial', 20), padx=37, pady=33, fg='blue', command=lambda: btn_click('/'))
b4 = Button(root, text='X', font=('Arial', 20), padx=33, pady=33, fg='blue', command=lambda: btn_click('X'))
b5 = Button(root, text='.', font=('Arial BOLD', 20), padx=33, pady=33, fg='blue', command=lambda: btn_click('.'))
b6 = Button(root, text='=', font=('Arial', 20), padx=33, pady=33, fg='blue', command=calculate)
b7 = Button(root, text='CLEAR', font=('Arial', 20), padx=50, pady=20, fg='blue', command=clear)
b8 = Button(root, text='EXIT', font=('Arial', 20), padx=60, pady=20, fg='blue', command=root.destroy)

# Grid Layout
n1.grid(row=1, column=1)
n2.grid(row=1, column=2)
n3.grid(row=1, column=3)
n4.grid(row=2, column=1)
n5.grid(row=2, column=2)
n6.grid(row=2, column=3)
n7.grid(row=3, column=1)
n8.grid(row=3, column=2)
n9.grid(row=3, column=3)
n0.grid(row=4, column=1)

b1.grid(row=1, column=4)
b2.grid(row=2, column=4)
b3.grid(row=3, column=4)
b6.grid(row=4, column=2)
b5.grid(row=4, column=3)
b4.grid(row=4, column=4)

b7.grid(row=5, column=1, columnspan=2, pady=5)
b8.grid(row=5, column=3, columnspan=2, pady=5)

if __name__ == '__main__':
    root.mainloop()
