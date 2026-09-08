# 24. MENU DRIVEN PROGRAM USING FUNCTIONS
# Interactive console menu with reusable math & logic functions

import sys

def sum_of_digits(n):
    s = 0
    temp = n
    while n > 0:
        a = n % 10
        s = s + a
        n = n // 10
    print(f"Sum of digits of {temp} is: {s}")

def greatest_in_three(a, b, c):
    if a >= b and a >= c:
        print(f"{a} is the greatest number")
    elif b >= a and b >= c:
        print(f"{b} is the greatest number")
    else:
        print(f"{c} is the greatest number")

def check_prime(n):
    if n <= 1:
        print(f"{n} is not a prime number")
        return
    for i in range(2, n):
        if n % i == 0:
            print(f"{n} is Not a prime number")
            break
    else:
        print(f"{n} is a Prime number")

def reverse_number(n):
    s = 0
    temp = n
    while n > 0:
        a = n % 10
        s = s * 10 + a
        n = n // 10
    print(f"Reverse of {temp} is: {s}")

def main():
    while True:
        print("\n" + "=" * 50)
        print("          *** PYTHON BASIC MAIN MENU ***")
        print("=" * 50)
        print("1. Sum of digits")
        print("2. Greatest in 3 numbers")
        print("3. Prime number check")
        print("4. Reverse of a number")
        print("5. Exit")
        print("-" * 50)
        
        try:
            choice = int(input("Enter your choice (1-5): "))
        except ValueError:
            print("Invalid input! Please enter an integer.")
            continue

        match choice:
            case 1:
                x = int(input("Enter number for sum of digits: "))
                sum_of_digits(x)
            case 2:
                f = int(input("Enter first number: "))
                g = int(input("Enter second number: "))
                h = int(input("Enter third number: "))
                greatest_in_three(f, g, h)
            case 3:
                x = int(input("Enter number to check prime: "))
                check_prime(x)
            case 4:
                k = int(input("Enter number to reverse: "))
                reverse_number(k)
            case 5:
                print("Thank you for using the program! Goodbye.")
                sys.exit(0)
            case _:
                print("Invalid choice! Please select between 1 and 5.")

if __name__ == "__main__":
    main()
