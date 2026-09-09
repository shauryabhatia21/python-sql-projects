# ==============================================================================
# Program: Tuple Foundations, Functions & Packing/Unpacking
# Author: Shaurya Bhatia (Bennett University)
# Description: Demonstrates immutable sequence architecture, single-element tuples,
#              built-in math/statistical operations, sorting, packing, and unpacking.
# ==============================================================================

def demonstrate_tuple_basics():
    print("=" * 60)
    print("        PYTHON TUPLE FOUNDATIONS & OPERATIONS")
    print("=" * 60)

    # 1. Blank tuple creation
    t_blank1 = ()
    t_blank2 = tuple()
    print(f"1. Empty Tuples: t_blank1 = {t_blank1}, t_blank2 = {t_blank2}")

    # 2. Multi-element and single-element tuples
    t1 = (11, 22, 33, 44, 55)
    t_single = (11,)  # Comma required to distinguish from integer in parentheses
    print(f"\n2. Multi-element Tuple: {t1} (Length: {len(t1)})")
    print(f"   Single-element Tuple: {t_single} (Type: {type(t_single)})")

    # 3. Built-in aggregation functions
    print("\n3. Built-in Mathematical Operations on Tuple:")
    print(f"   Elements : {t1}")
    print(f"   Maximum  : {max(t1)}")
    print(f"   Minimum  : {min(t1)}")
    print(f"   Sum      : {sum(t1)}")
    print(f"   Length   : {len(t1)}")
    print(f"   Average  : {sum(t1) / len(t1):.2f}")

    # 4. Sorting tuples (returns a sorted list)
    t_unsorted = (45, 12, 89, 23, 67)
    print(f"\n4. Sorting Tuples:")
    print(f"   Original Tuple   : {t_unsorted}")
    print(f"   Ascending Order  : {sorted(t_unsorted)}")
    print(f"   Descending Order : {sorted(t_unsorted, reverse=True)}")

    # 5. Tuple Packing & Unpacking
    print("\n5. Tuple Packing & Unpacking:")
    packed_tuple = 101, "Shaurya", "AI & Data Science", 95.5  # Packing
    print(f"   Packed Tuple: {packed_tuple} (Type: {type(packed_tuple)})")

    roll, name, department, score = packed_tuple  # Unpacking
    print("   Unpacked Variables:")
    print(f"     - Roll Number : {roll}")
    print(f"     - Student Name: {name}")
    print(f"     - Department  : {department}")
    print(f"     - Score (GPA) : {score}")

    # 6. Immutability demonstration
    print("\n6. Immutability Guarantee:")
    print("   Tuples are immutable; attempts to mutate t1[0] = 99 will raise a TypeError.")
    print("=" * 60)


if __name__ == "__main__":
    demonstrate_tuple_basics()
