"""
Exception Handling in Python: Concepts & Demonstrations
Author: Shaurya Bhatia (Bennett University)
--------------------------------------------------------------------------------
Key Concepts Covered:
1. What is an Exception:
   - Run-time error that disrupts the normal flow of instruction execution.
   - Handled gracefully using try, except, else, and finally blocks.

2. Compile-Time vs Run-Time Errors:
   - Compile-Time: Syntax/grammatical errors detected before bytecode generation.
   - Run-Time: Logical failures during execution (e.g., ZeroDivisionError, IndexError, ValueError).

3. Block Roles:
   - try: Contains code that might potentially raise an exception.
   - except: Catches and handles specific or general exceptions.
   - else: Executes only if the try block ran without raising any exception.
   - finally: Guarantees execution regardless of whether an exception occurred or was handled.

4. The 'raise' Keyword:
   - Allows programmers to deliberately raise an exception based on custom conditions.

5. Custom User-Defined Exceptions:
   - Classes derived from the built-in Exception class.
"""


# ==============================================================================
# SECTION 1: BASIC TRY - EXCEPT WITH SPECIFIC & GENERAL HANDLERS
# ==============================================================================

def divide_numbers_demo(a, b):
    """Demonstrates division with specific ZeroDivisionError & TypeError handling."""
    print(f"\n--- Attempting Division: {a} / {b} ---")
    try:
        result = a / b
        print(f"Success! Result: {result}")
        return result
    except ZeroDivisionError as zde:
        print(f"[Handled ZeroDivisionError]: Cannot divide by zero -> {zde}")
        return None
    except TypeError as te:
        print(f"[Handled TypeError]: Non-numeric operand provided -> {te}")
        return None
    except Exception as e:
        print(f"[Handled General Exception]: An unexpected error occurred -> {e}")
        return None


# Test demonstrations
divide_numbers_demo(10, 2)
divide_numbers_demo(10, 0)
divide_numbers_demo(10, "two")


# ==============================================================================
# SECTION 2: LIST INDEX BOUNDS & VALUE ERRORS
# ==============================================================================

def safe_list_access_demo():
    """Demonstrates handling of IndexError."""
    print("\n--- List Index Bounds Handling ---")
    sample_list = [11, 22, 33, 44, 55]
    indices_to_test = [1, 4, 10]
    
    for idx in indices_to_test:
        try:
            print(f"Accessing index {idx}: Value = {sample_list[idx]}")
        except IndexError as ie:
            print(f"[Handled IndexError]: Index {idx} is out of range for list of length {len(sample_list)} -> {ie}")


safe_list_access_demo()


# ==============================================================================
# SECTION 3: THE 'finally' & 'else' BLOCKS
# ==============================================================================

def divide_with_finally(numerator, denominator):
    """
    Demonstrates try, except, else, and finally lifecycle.
    'finally' always executes whether an error occurred or not.
    """
    print(f"\n--- Demonstrating finally block for {numerator} / {denominator} ---")
    try:
        val = numerator / denominator
    except ZeroDivisionError as err:
        print(f"[Handler]: Division failed -> {err}")
        val = 0
    else:
        print("[Else]: Calculation completed smoothly without any exceptions!")
    finally:
        print("[Finally]: Resource cleanup completed. Finally block always executes.")
    return val


divide_with_finally(50, 5)
divide_with_finally(50, 0)


# ==============================================================================
# SECTION 4: THE 'raise' KEYWORD & CUSTOM EXCEPTIONS
# ==============================================================================

class NegativeNumberError(Exception):
    """Custom exception raised when an unexpected negative number is encountered."""
    pass


def validate_positive_number(num):
    """Validates if a number is non-negative, otherwise raises a custom exception."""
    print(f"\n--- Validating input: {num} ---")
    try:
        if num < 0:
            raise NegativeNumberError(f"Negative value ({num}) is not allowed in this domain.")
        print(f"Validation passed: {num} is positive or zero.")
    except NegativeNumberError as nne:
        print(f"[Custom Exception Caught]: {nne}")


validate_positive_number(42)
validate_positive_number(-15)

print("\n" + "=" * 50)
print("Exception Handling Demonstration Completed Successfully!")
print("=" * 50)
