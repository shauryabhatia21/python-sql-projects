# NESTED LOOPS & MATRIX TRAVERSALS
# Covers: Iterating through 2D student tables, coordinate grids, and matrix operations

def student_record_traversal():
    students = [
        [101, "Shaurya", "Python", 35000],
        [102, "Sumit", "SQL", 28000],
        [103, "Manjit", "Pandas", 30000],
        [104, "Vineet", "NumPy", 25000]
    ]

    print("--- Student Matrix Traversal ---")
    print(f"{'Roll':<10} {'Name':<15} {'Course':<15} {'Fee':<10}")
    print("-" * 50)
    for row in students:
        roll = row[0]
        name = row[1]
        course = row[2]
        fee = row[3]
        print(f"{roll:<10} {name:<15} {course:<15} {fee:<10}")
    print("-" * 50)

def coordinate_grid(rows=3, cols=3):
    print("\n--- Coordinate Grid (Row, Col) ---")
    for r in range(rows):
        for c in range(cols):
            print(f"({r},{c})", end="  ")
        print()

def matrix_addition():
    A = [
        [1, 2],
        [3, 4]
    ]
    B = [
        [5, 6],
        [7, 8]
    ]
    C = [
        [0, 0],
        [0, 0]
    ]

    for i in range(len(A)):
        for j in range(len(A[0])):
            C[i][j] = A[i][j] + B[i][j]

    print("\n--- Matrix Addition (A + B = C) ---")
    for row in C:
        print(row)

if __name__ == '__main__':
    student_record_traversal()
    coordinate_grid()
    matrix_addition()
