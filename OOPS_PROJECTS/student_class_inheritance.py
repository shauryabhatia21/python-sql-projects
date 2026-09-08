# MULTI-LEVEL INHERITANCE: STUDENT ACADEMIC SYSTEM
# Hierarchy: PDetail (Personal Details) -> Marks (Term Marks) -> Result (Calculated Average & Grade)

class PDetail:
    def __init__(self, eno, name, course, fees):
        self.eno = eno
        self.name = name
        self.course = course
        self.fees = fees

    def showDetail(self):
        print('Enrollment No :', self.eno)
        print('Student Name  :', self.name)
        print('Course Name   :', self.course)
        print('Fees Paid     :', self.fees)

class Marks(PDetail):
    def __init__(self, eno, name, course, fees, term1, term2):
        super().__init__(eno, name, course, fees)
        self.term1 = term1
        self.term2 = term2

    def getTotal(self):
        return self.term1 + self.term2

    def showMarks(self):
        print('Term 1 Marks  :', self.term1)
        print('Term 2 Marks  :', self.term2)

class Result(Marks):
    def __init__(self, eno, name, course, fees, term1, term2):
        super().__init__(eno, name, course, fees, term1, term2)
        self.total = 0
        self.amarks = 0.0

    def showResult(self):
        print("\n" + "=" * 45)
        print("          STUDENT RESULT SHEET")
        print("=" * 45)
        self.showDetail()
        print("-" * 45)
        self.showMarks()
        print("-" * 45)
        self.total = self.getTotal()
        self.amarks = self.total / 2.0
        print('Total Marks   :', self.total)
        print('Average Score :', self.amarks)
        print('Result Status :', "PASSED" if self.amarks >= 40 else "FAILED")
        print("=" * 45)

if __name__ == '__main__':
    print("Creating sample student result using multi-level inheritance:")
    r1 = Result(101, 'Shaurya Bhatia', 'Python & Data Science', 35000, 88, 94)
    r1.showResult()
