"""
Modular Extended Calculator (Inheritance & Match-Case Architecture)
Author: Shaurya Bhatia (Bennett University)
--------------------------------------------------------------------------------
Demonstrates:
- Base class 'Calculator' implementing arithmetic operations (+, -, *, /)
- Derived class 'LogicalCalculator' extending functionality with Square and Square Root
- Python 3.10+ match-case CLI menu loop
"""

import sys
import math


class Calculator:
    """Base class for standard arithmetic operations."""
    def addition(self):
        number1 = float(input("Enter first number: "))
        number2 = float(input("Enter second number: "))
        result = number1 + number2
        print(f"Result (Addition): {result}")
        print('=' * 50)
        return result

    def subtraction(self):
        number1 = float(input("Enter first number: "))
        number2 = float(input("Enter second number: "))
        result = number1 - number2
        print(f"Result (Subtraction): {result}")
        print('=' * 50)
        return result

    def multiply(self):
        number1 = float(input("Enter first number: "))
        number2 = float(input("Enter second number: "))
        result = number1 * number2
        print(f"Result (Multiplication): {result}")
        print('=' * 50)
        return result

    def divide(self):
        number1 = float(input("Enter numerator: "))
        number2 = float(input("Enter denominator: "))
        if number2 == 0:
            print("Error: Cannot divide by zero.")
            print('=' * 50)
            return None
        result = number1 / number2
        print(f"Result (Division): {result}")
        print('=' * 50)
        return result


class LogicalCalculator(Calculator):
    """Derived class inheriting standard arithmetic and adding scientific methods."""
    def square(self):
        number = float(input("Enter number to square: "))
        result = number * number
        print(f"Result ({number}^2): {result}")
        print('=' * 50)
        return result

    def square_root(self):
        number = float(input("Enter number for square root: "))
        if number < 0:
            print("Error: Cannot calculate square root of a negative real number.")
            print('=' * 50)
            return None
        result = math.sqrt(number)
        print(f"Result (sqrt({number})): {result}")
        print('=' * 50)
        return result

    # Kept for backward compatibility
    def Square(self):
        return self.square()

    def SquareRoot(self):
        return self.square_root()


def main():
    calc = LogicalCalculator()
    while True:
        print("\n" + "=" * 50)
        print("          LOGICAL CALCULATOR MENU (OOP)          ")
        print("=" * 50)
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiply")
        print("4. Divide")
        print("5. Square")
        print("6. Square Root")
        print("7. Exit")
        print("=" * 50)
        
        try:
            ch = int(input("Enter your choice (1-7): "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 7.")
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
                calc.Square()
            case 6:
                calc.SquareRoot()
            case 7:
                print("Exiting Calculator. Thank you!")
                sys.exit(0)
            case _:
                print("Invalid choice. Please select from 1 to 7.")


if __name__ == "__main__":
    main()
