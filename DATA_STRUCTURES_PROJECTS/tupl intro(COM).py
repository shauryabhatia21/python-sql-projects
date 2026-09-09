"""
Tuple is another data structure of Python.
Tuple is like list, it is a sequential data structure, but the main difference
between tuple and list is tuple is immutable (cannot be modified), whereas list can be modified.
"""

t1 = ()         # will generate blank tuple
t1 = tuple()    # will also generate blank tuple

t1 = (11, 22, 33, 44, 55)  # tuple with specified elements
t1_single = (11,)          # single element tuple

print("Tuple t1:", t1)
print("Single element tuple:", t1_single)

# Built-in functions that can be applied on tuple:
print("Max:", max(t1))
print("Min:", min(t1))
print("Sum:", sum(t1))
print("Len:", len(t1))

# sorted() will sort the elements of tuple and return a list
print("Sorted (Ascending):", sorted(t1))
print("Sorted (Descending):", sorted(t1, reverse=True))

# Packing and unpacking:
a1 = 11, 22, 33, 44, 55    # Packing of tuple
a, b, c, d, e = a1         # Unpacking of tuple
print("Unpacked elements:", a, b, c, d, e)
