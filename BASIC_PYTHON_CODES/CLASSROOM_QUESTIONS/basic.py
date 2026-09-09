"""
Basic Python Foundations & Loop Exercises (Classroom Notes)
Author: Shaurya Bhatia (Bennett University)
--------------------------------------------------------------------------------
In Python, there are 3 primary loop structures:
1. for loop
2. while loop
3. for...else loop

Syntax of for loop:
    for i in range(begin, end, step):
        # body of loop

Rules:
* If begin is not given, starts from 0
* If step is not given, default is +1
* If step is positive, stops at end - 1
* If step is negative, stops at end + 1
"""

# ==============================================================================
# SECTION 1: FOR LOOP BASICS
# ==============================================================================

def vertical_numbers():
    """Prints numbers 1 to 10 vertically."""
    print("--- 1. Vertical 1-10 ---")
    for i in range(1, 11):
        print(i)


def horizontal_numbers():
    """Prints numbers 1 to 10 horizontally."""
    print("\n--- 2. Horizontal 1-10 ---")
    for i in range(1, 11):
        print(i, end='  ')
    print()


def step_two_numbers():
    """Prints odd numbers with a gap of 2."""
    print("\n--- 3. Step of 2 ---")
    for i in range(1, 11, 2):
        print(i, end='  ')
    print()


def reverse_numbers():
    """Prints numbers 11 down to 1."""
    print("\n--- 4. Reverse 11 to 1 ---")
    for i in range(11, 0, -1):
        print(i, end='  ')
    print()


# ==============================================================================
# SECTION 2: ALGORITHM PROBLEMS
# ==============================================================================

def power_multiplication(a=2, b=4):
    """Calculates power via multiplication/repeated addition concept."""
    print(f"\n--- Power concept of {a}^{b} ---")
    result = a ** b
    print("Result:", result)
    return result


def hcf_two_numbers(a=12, b=18):
    """Computes Highest Common Factor (HCF / GCD)."""
    print(f"\n--- HCF of {a} and {b} ---")
    hcf = 1
    m = min(a, b)
    for i in range(1, m + 1):
        if a % i == 0 and b % i == 0:
            hcf = i
    print("HCF is:", hcf)
    return hcf


def check_prime(n=7):
    """Checks if a number is prime."""
    print(f"\n--- Prime check for {n} ---")
    if n <= 1:
        print(f"{n} is not prime")
        return False
    c = 0
    for i in range(1, n + 1):
        if n % i == 0:
            c += 1
    if c == 2:
        print(f"{n} is a Prime number")
        return True
    else:
        print(f"{n} is not a Prime number")
        return False


def factors_of_number(n=24):
    """Prints all factors of a given number."""
    print(f"\n--- Factors of {n} ---")
    factors = [i for i in range(1, n + 1) if n % i == 0]
    print(f"Factors: {factors}")
    return factors


def factorial_of_number(n=5):
    """Computes factorial n!"""
    print(f"\n--- Factorial of {n} ---")
    f = 1
    for i in range(1, n + 1):
        f *= i
    print(f"{n}! = {f}")
    return f


def check_perfect_number(n=6):
    """Checks if a number is equal to sum of its proper divisors."""
    print(f"\n--- Perfect number check for {n} ---")
    s = sum(i for i in range(1, n) if n % i == 0)
    if s == n:
        print(f"{n} is a Perfect Number")
        return True
    else:
        print(f"{n} is not a Perfect Number")
        return False


def multiplication_table(n=5):
    """Prints multiplication table for n."""
    print(f"\n--- Multiplication Table of {n} ---")
    for i in range(1, 11):
        print(f"{n} x {i} = {n * i}")


# ==============================================================================
# SECTION 3: STAR & NUMBER PATTERNS
# ==============================================================================

def pattern_grid_numbers():
    """Grid pattern: 1 2 3 across 5 rows."""
    print("\n--- Pattern 1: Number Grid ---")
    for i in range(1, 6):
        for j in range(1, 4):
            print(j, end=' ')
        print()


def pattern_slant_triangle():
    """Slant triangle: 1 to i."""
    print("\n--- Pattern 2: Slant Triangle ---")
    for i in range(1, 6):
        for j in range(1, i + 1):
            print(j, end=' ')
        print()


def pattern_inverted_triangle():
    """Inverted triangle."""
    print("\n--- Pattern 3: Inverted Triangle ---")
    for i in range(6, 1, -1):
        for j in range(1, i):
            print(j, end=' ')
        print()


def pattern_pyramid():
    """Centered number pyramid."""
    print("\n--- Pattern 4: Number Pyramid ---")
    for i in range(1, 5):
        for k in range(4, i, -1):
            print(end=' ')
        for j in range(1, i + 1):
            print(j, end=' ')
        print()


if __name__ == "__main__":
    print("Running Basic Python Classroom Demonstration...")
    vertical_numbers()
    horizontal_numbers()
    step_two_numbers()
    reverse_numbers()
    power_multiplication()
    hcf_two_numbers()
    check_prime()
    factors_of_number()
    factorial_of_number()
    check_perfect_number()
    multiplication_table()
    pattern_grid_numbers()
    pattern_slant_triangle()
    pattern_inverted_triangle()
    pattern_pyramid()
    print("\n" + "=" * 50)
    print("Execution completed successfully!")
