"""
Introduction to Object-Oriented Programming (Classes & Objects)
Author: Shaurya Bhatia (Bennett University)
--------------------------------------------------------------------------------
Key Principles:
1. Procedural Programming vs Object-Oriented Programming:
   - In POP, emphasis is placed on functions and actions rather than data.
   - In OOP, data and functionality are bound together into cohesive entities (Classes & Objects).

2. Class & Object Metaphor:
   - A Class is a blueprint/design (e.g., Sony TV design and specifications).
   - An Object is the physical instance built from that blueprint (e.g., The TV on the wall).
   - A Reference Variable is the pointer used to interact with the object (e.g., The Remote Control).
"""

# ==============================================================================
# QUESTION 1: STUDENT PROFILE CLASS
# ==============================================================================

class Student:
    """Represents a student enrolled in a specialized course."""
    def __init__(self, eno, name, course, fee):
        self.eno = eno
        self.name = name
        self.course = course
        self.fee = fee

    def showDetail(self):
        print('Enrollment No :', self.eno)
        print('Student Name  :', self.name)
        print('Course        :', self.course)
        print('Fee (INR)     :', self.fee)
        print('=' * 50)


# ==============================================================================
# QUESTION 2: DISTANCE AND FUEL REQUIREMENT CALCULATOR
# ==============================================================================

class CalFuel:
    """Class representing distance brackets and corresponding fuel capacity requirements."""
    def __init__(self, distance, fuel):
        self.distance = distance
        self.fuel = fuel

    def show(self):
        print('Distance Bracket   :', self.distance)
        print('Fuel Required (L)  :', self.fuel)
        print('=' * 50)


if __name__ == "__main__":
    print("--- 1. Student Class Instances ---")
    s1 = Student(101, 'Shaurya Bhatia', 'Computer Science & Engineering', 85000)
    s1.showDetail()

    s2 = Student(102, 'Abhinav Sharma', 'Machine Learning', 75000)
    s2.showDetail()

    print("--- 2. Fuel Requirement Classification ---")
    c1 = CalFuel('<= 1000 km', 500)
    c1.show()

    c2 = CalFuel('> 1000 and <= 2000 km', 1100)
    c2.show()

    c3 = CalFuel('> 2000 km', 2200)
    c3.show()
