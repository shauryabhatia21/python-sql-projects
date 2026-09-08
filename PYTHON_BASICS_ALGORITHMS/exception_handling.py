# EXCEPTION HANDLING & ERROR PREVENTION
# Covers: try-except, catching specific built-in exceptions, using 'raise', and the 'finally' clause

def safe_division(a, b):
    try:
        result = a / b
        print(f"Division Result: {a} / {b} = {result}")
        return result
    except ZeroDivisionError:
        print("Caught Error: Cannot divide a number by zero!")
        return None
    except TypeError:
        print("Caught Error: Inputs must be numerical values!")
        return None
    finally:
        print("Cleanup: safe_division execution finished.")

def check_even_or_raise(n):
    try:
        if n % 2 == 0:
            print(f"Success: {n} is an Even Number.")
        else:
            raise ValueError(f"Custom Validation Failed: {n} is an Odd Number!")
    except ValueError as e:
        print(f"Caught Custom Raised Exception: {e}")

def list_access_demo(numbers, index):
    try:
        val = numbers[index]
        print(f"Element at index {index} is: {val}")
    except IndexError:
        print(f"IndexError: Index {index} is out of bounds for list of size {len(numbers)}!")

if __name__ == '__main__':
    print("--- 1. Safe Division Tests ---")
    safe_division(10, 2)
    safe_division(10, 0)

    print("\n--- 2. Custom Raise Tests ---")
    check_even_or_raise(4)
    check_even_or_raise(7)

    print("\n--- 3. List Bounds Checking ---")
    sample_list = [10, 20, 30]
    list_access_demo(sample_list, 1)
    list_access_demo(sample_list, 5)
