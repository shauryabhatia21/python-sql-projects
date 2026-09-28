"""
Multilevel Academic Inheritance (PDetail -> Marks -> Result)
Author: Shaurya Bhatia (Bennett University)
--------------------------------------------------------------------------------
Demonstrates:
- Base class PDetail: Student personal and course details
- Intermediate class Marks: Inherits PDetail and adds term evaluation scores
- Derived class Result: Inherits Marks and calculates aggregate totals and averages
"""

class PDetail:
    def __init__(self, eno, name, course, fees):
        self.eno = eno
        self.name = name
        self.course = course
        self.fees = fees

    def showDetail(self):
        print('Enrollment No is:', self.eno)
        print('Student Name is:', self.name)
        print('Course is:', self.course)
        print('Fee is:', self.fees)
        print('=' * 50)


class Marks(PDetail):
    def __init__(self, eno, name, course, fees, term1, term2):
        super().__init__(eno, name, course, fees)
        self.term1 = term1
        self.term2 = term2

    def getTotal(self):
        return self.term1 + self.term2

    def showMarks(self):
        print('Marks in Term 1:', self.term1)
        print('Marks in Term 2:', self.term2)
        print('=' * 50)


class Result(Marks):
    def __init__(self, eno, name, course, fees, term1, term2):
        super().__init__(eno, name, course, fees, term1, term2)
        self.total = 0
        self.amarks = 0.0

    def showResult(self):
        print("\n" + "=" * 50)
        print("          ACADEMIC RESULT CARD          ")
        print("=" * 50)
        self.showDetail()
        self.showMarks()
        self.total = self.getTotal()
        self.amarks = self.total / 2
        print('Total Marks:', self.total)
        print('Average Percentage:', f"{self.amarks:.2f}%")
        print('=' * 50)


if __name__ == "__main__":
    r1 = Result(101, 'Shaurya Bhatia', 'Computer Science & Engineering', 85000, 94, 98)
    r1.showResult()
