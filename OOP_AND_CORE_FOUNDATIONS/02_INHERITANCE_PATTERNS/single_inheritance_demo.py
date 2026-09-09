"""
Introduction to Single Inheritance in Python
Author: Shaurya Bhatia (Bennett University)
--------------------------------------------------------------------------------
Demonstrates:
- Base class 'First'
- Derived class 'Second' inheriting 'First'
- Calling derived and base class methods via derived object
"""

class First:
    """Base class."""
    def show1(self):
        print("I am showing show1() of First (Base Class)")


class Second(First):
    """Derived class inheriting from First."""
    def show2(self):
        print("I am showing show2() of Second (Derived Class)")


if __name__ == "__main__":
    print("--- Single Inheritance Demo ---")
    s1 = Second()
    s1.show2()
    s1.show1()
    print("=" * 50)
