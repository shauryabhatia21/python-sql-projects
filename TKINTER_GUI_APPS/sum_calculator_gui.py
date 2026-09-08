from tkinter import *

root = Tk()
root.title("ADDITION CALCULATOR")
root.minsize(450, 550)
root.maxsize(450, 550)
root.configure(bg="#F7FAFC")

num1 = IntVar()
num2 = IntVar()
result = StringVar()

def sumNumber():
    try:
        x = num1.get() + num2.get()
        result.set(f"SUM IS: {x}")
    except Exception as e:
        result.set("Invalid Input")

# Title
Label(root, text="TWO NUMBER ADDER", font=("Arial Bold", 16), bg="#F7FAFC", fg="#2D3748").pack(pady=20)

# Inputs
Label(root, text='ENTER FIRST NUMBER', font=("Arial Bold", 11), bg="#F7FAFC").pack(pady=5)
Entry(root, textvariable=num1, font=("Arial", 12), justify='center').pack()

Label(root, text='ENTER SECOND NUMBER', font=("Arial Bold", 11), bg="#F7FAFC").pack(pady=5)
Entry(root, textvariable=num2, font=("Arial", 12), justify='center').pack()

# Action Button
Button(root, text="CALCULATE SUM", font=('Arial Bold', 11), bg="#3182CE", fg="white", padx=20, pady=6, command=sumNumber).pack(pady=25)

# Result
Label(root, font=("Arial Bold", 14), fg="#2B6CB0", bg="#F7FAFC", textvariable=result).pack(pady=10)

if __name__ == '__main__':
    root.mainloop()
