from tkinter import *

root = Tk()
root.title("PERCENTAGE CALCULATOR")
root.minsize(500, 700)
root.maxsize(500, 700)
root.configure(bg="#F0F4F8")

# Input variables
num1 = IntVar()
num2 = IntVar()
num3 = IntVar()
num4 = IntVar()
num5 = IntVar()

# Output variables
sum_result = StringVar()
pct_result = StringVar()

# Calculation functions
def calculate_sum():
    total = num1.get() + num2.get() + num3.get() + num4.get() + num5.get()
    sum_result.set(f"TOTAL SUM: {total}")

def calculate_percentage():
    total = num1.get() + num2.get() + num3.get() + num4.get() + num5.get()
    percentage = total / 5.0
    pct_result.set(f"PERCENTAGE: {percentage:.2f}%")

# Title Banner
Label(root, text="STUDENT MARKS CALCULATOR", font=("Arial Bold", 16), bg="#F0F4F8", fg="#1A365D").pack(pady=15)

# Input Fields
Label(root, text='ENTER SUBJECT 1 MARKS', font=("Arial Bold", 11), bg="#F0F4F8").pack(pady=3)
Entry(root, textvariable=num1, font=("Arial", 12), justify='center').pack()

Label(root, text='ENTER SUBJECT 2 MARKS', font=("Arial Bold", 11), bg="#F0F4F8").pack(pady=3)
Entry(root, textvariable=num2, font=("Arial", 12), justify='center').pack()

Label(root, text='ENTER SUBJECT 3 MARKS', font=("Arial Bold", 11), bg="#F0F4F8").pack(pady=3)
Entry(root, textvariable=num3, font=("Arial", 12), justify='center').pack()

Label(root, text='ENTER SUBJECT 4 MARKS', font=("Arial Bold", 11), bg="#F0F4F8").pack(pady=3)
Entry(root, textvariable=num4, font=("Arial", 12), justify='center').pack()

Label(root, text='ENTER SUBJECT 5 MARKS', font=("Arial Bold", 11), bg="#F0F4F8").pack(pady=3)
Entry(root, textvariable=num5, font=("Arial", 12), justify='center').pack()

# Action Buttons
Button(root, text="CALCULATE SUM", font=('Arial Bold', 10), bg="#2B6CB0", fg="white", padx=15, pady=5, command=calculate_sum).pack(pady=12)
Label(root, font=("Arial Bold", 13), fg="#2B6CB0", bg="#F0F4F8", textvariable=sum_result).pack()

Button(root, text="CALCULATE PERCENTAGE", font=('Arial Bold', 10), bg="#2F855A", fg="white", padx=15, pady=5, command=calculate_percentage).pack(pady=12)
Label(root, font=("Arial Bold", 13), fg="#2F855A", bg="#F0F4F8", textvariable=pct_result).pack()

if __name__ == '__main__':
    root.mainloop()
