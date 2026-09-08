# INHERITANCE CALCULATOR
# Demonstrates single & multi-level class inheritance with base Calculator and advanced Scientific/Logical operations

import sys
import math

class Calculator:
    def addition(self):
        number1 = float(input("Enter your first number: "))
        number2 = float(input("Enter your second number: "))
        result = number1 + number2
        print('Your result is:', result)
        return result

    def subtraction(self):
        number1 = float(input("Enter your first number: "))
        number2 = float(input("Enter your second number: "))
        result = number1 - number2
        print('Your result is:', result)
        return result

    def multiply(self):
        number1 = float(input("Enter your first number: "))
        number2 = float(input("Enter your second number: "))
        result = number1 * number2
        print('Your result is:', result)
        return result
    
    def divide(self):
        number1 = float(input("Enter your first number: "))
        number2 = float(input("Enter your second number: "))
        if number2 == 0:
            print("Error: Cannot divide by zero.")
            return None
        result = number1 / number2
        print('Your result is:', result)
        return result

class LogicalCalculator(Calculator):
    def square(self):
        number1 = float(input("Enter your number: "))
        result = number1 * number1
        print('Your result is:', result)
        return result

    def square_root(self):
        number1 = float(input("Enter your number: "))
        if number1 < 0:
            print("Error: Cannot calculate square root of a negative number.")
            return None
        result = math.sqrt(number1)
        print('Your result is:', result)
        return result

def main():
    calc = LogicalCalculator()
    while True:
        print("\n" + "=" * 40)
        print("     --- CALCULATOR (INHERITANCE) ---")
        print("=" * 40)
        print('1. Addition')
        print('2. Subtraction')
        print('3. Multiply')
        print('4. Divide')
        print('5. Square')
        print('6. Square Root')
        print('7. Exit')
        print("-" * 40)
        
        try:
            ch = int(input("Enter your choice (1-7): "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue

        match ch:
            case 1:
                calc.addition()
            case 2:
                calc.subtraction()
            case 3:
                calc.multiply()
            case 4:
                calc.divide()
            case 5:
                calc.square()
            case 6:
                calc.square_root()
            case 7:
                print("Exiting calculator... Thank you!")
                sys.exit(0)
            case _:
                print("Invalid choice! Please select between 1 and 7.")

if __name__ == '__main__':
    main()
