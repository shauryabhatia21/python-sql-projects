"""
Inner Classes & Functional Programming in Python
Author: Shaurya Bhatia (Bennett University)
--------------------------------------------------------------------------------
Topics Covered:
1. Inner (Nested) Classes:
   - Definition: A class declared inside another class.
   - Use Case: When an object of one type cannot logically exist without an object of another type.
   - Real-World Examples:
     * Car and Engine: An Engine only exists in the context of a Car.
     * University and Department: A Department belongs to a University.
     * Person and DateOfBirth (DOB): A DOB object belongs to a Person.
   - An inner class object is always associated with the outer class instance.

2. Anonymous Functions (Lambda Expressions):
   - Syntax: lambda arguments: expression
   - Used for quick, one-line functions without standard 'def' keyword.

3. Higher-Order Built-in Functions:
   - map(function, iterable): Transforms each element.
   - filter(function, iterable): Filters elements where function evaluates to True.
   - reduce(function, iterable): Aggregates sequence elements into a single accumulated result.
"""

from functools import reduce


# ==============================================================================
# SECTION 1: INNER / NESTED CLASSES
# ==============================================================================

class Outer:
    """Outer class demonstration."""
    def __init__(self):
        print("Outer class object is created.")

    def myMethod(self):
        print("Method of outer class.")

    class Inner:
        """Inner class declared inside Outer."""
        def __init__(self):
            print("Inner class object is created.")

        def m1(self):
            print("Method of inner class.")


# Instantiation techniques for inner classes:
print("--- Inner Class Instantiation ---")
# Method 1: Two-step creation
o = Outer()
i = o.Inner()
i.m1()

# Method 2: Chained instantiation
i2 = Outer().Inner()
i2.m1()

# Method 3: One-liner invocation
Outer().Inner().m1()
print("=" * 50)


# Real-World Inner Class Example: Person and Date of Birth
class Person:
    """Person entity with an encapsulated DOB inner class."""
    def __init__(self, name="Shaurya", dd=15, month=5, year=2005):
        self.name = name
        self.dob = self.DOB(dd, month, year)

    def display(self):
        print(f"Name: {self.name}")
        self.dob.display()
        print("=" * 50)

    class DOB:
        """Date of Birth inner class."""
        def __init__(self, dd, month, year):
            self.dd = dd
            self.month = month
            self.year = year

        def display(self):
            print(f"Date of Birth: {self.dd:02d}/{self.month:02d}/{self.year}")


print("--- Person & Inner DOB Class ---")
p = Person("Shaurya Bhatia", 15, 8, 2005)
p.display()


# ==============================================================================
# SECTION 2: ANONYMOUS FUNCTIONS (LAMBDA EXPRESSIONS)
# ==============================================================================

print("--- Lambda Functions ---")
# Cube calculation
cube = lambda x: x ** 3
print("Cube of 3:", cube(3))

# Max of two numbers using ternary conditional inside lambda
find_max = lambda a, b: a if a > b else b
print("Max of 11 and 33:", find_max(11, 33))

# Addition of two numbers
add = lambda a, b: a + b
print("Sum of 2 and 3:", add(2, 3))
print("=" * 50)


# ==============================================================================
# SECTION 3: MAP FUNCTION
# ==============================================================================

print("--- map() Demonstrations ---")
nums = [1, 2, 3, 4, 5]

# Using a standard function
def square(a):
    return a ** 2

squared_standard = list(map(square, nums))
print("Squared (via def):", squared_standard)

# Using lambda with map
squared_lambda = list(map(lambda x: x ** 2, nums))
print("Squared (via lambda):", squared_lambda)

# Measuring string lengths with map
names = ['manish', 'vineet', 'ravi']
lengths = list(map(len, names))
print("String lengths of names:", lengths)

# Multi-iterable addition via map
x = [11, 22, 33, 44]
y = [10, 23, 22, 33]
summed_lists = list(map(lambda a, b: a + b, x, y))
print("Element-wise sums:", summed_lists)
print("=" * 50)


# ==============================================================================
# SECTION 4: FILTER FUNCTION
# ==============================================================================

print("--- filter() Demonstrations ---")
a1 = [11, 22, 33, 44, 55, 66]
evens = list(filter(lambda x: x % 2 == 0, a1))
print("Even numbers:", evens)

# Filter words starting with 'a'
names_list = ['arun', 'ravi', 'harsh', 'abhi', 'arnav']
starts_with_a = list(filter(lambda x: x.startswith('a'), names_list))
print("Names starting with 'a':", starts_with_a)

# Filter empty strings or non-alphabetic
mixed = ['arun', 'shaurya', 'arnav', '', ' ', '123']
only_alpha = list(filter(lambda x: x.isalpha(), mixed))
non_empty = list(filter(lambda x: len(x.strip()) > 0, mixed))
print("Alphabetic strings only:", only_alpha)
print("Non-empty strings:", non_empty)
print("=" * 50)


# ==============================================================================
# SECTION 5: REDUCE FUNCTION
# ==============================================================================

print("--- reduce() Demonstrations ---")
n = [1, 2, 3, 4, 10]

# Cumulative sum
sum_result = reduce(lambda x, y: x + y, n)
print("Cumulative sum of [1, 2, 3, 4, 10]:", sum_result)

# Cumulative max
max_result = reduce(lambda x, y: max(x, y), n)
print("Max value via reduce:", max_result)
print("=" * 50)
