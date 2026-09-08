"""
NumPy (Numerical Python) Demonstrations & Fundamentals
Covers:
- ndarray properties (ndim, shape, size, dtype)
- Array creation (zeros, ones, eye, arange, linspace)
- Slicing and Views vs Copies
- Vectorized operations and Math
- Aggregation functions and Reshaping
- Boolean masking and Matrix multiplication
"""

import numpy as np

print("--- 1. NumPy Array Creation & Properties ---")
arr = np.array([[1, 2, 3], [4, 5, 6]])
print("Array:\n", arr)
print("Dimensions (ndim) :", arr.ndim)
print("Shape             :", arr.shape)
print("Total Elements    :", arr.size)
print("Data Type (dtype) :", arr.dtype)

print("\n--- 2. Built-in Creation Functions ---")
zeros_arr = np.zeros((2, 3))
print("Zeros (2x3):\n", zeros_arr)

ones_arr = np.ones((2, 2))
print("Ones (2x2):\n", ones_arr)

identity_mat = np.eye(3)
print("Identity Matrix (3x3):\n", identity_mat)

stepped_arr = np.arange(0, 10, 2)
print("Arange (0 to 10 with step 2):", stepped_arr)

spaced_arr = np.linspace(0, 1, 5)
print("Linspace (5 equal points between 0 and 1):", spaced_arr)

print("\n--- 3. Slicing, Views vs Copies ---")
a1 = np.array([11, 22, 33, 44, 55])
# Slice creates a view
view_a = a1[::]
view_a[1] = 99
print("Original after view modification:", a1)

# .copy() creates an independent copy
copy_a = a1.copy()
copy_a[1] = 22
print("Original untouched after copy modification:", a1)
print("Copy array:", copy_a)

print("\n--- 4. Vectorized Mathematical Operations ---")
a = np.array([10, 20, 30])
b = np.array([4, 5, 6])
print("a + b =", a + b)
print("a * b =", a * b)
print("Square root of a =", np.sqrt(a))
print("Exponential of b =", np.exp(b))
print("Log of a =", np.log(a))

print("\n--- 5. Aggregations & Reshaping ---")
nums = np.array([10, 20, 30, 40])
print("Sum  :", np.sum(nums))
print("Mean :", np.mean(nums))
print("Std  :", np.std(nums))

grid12 = np.arange(1, 13)
reshaped = grid12.reshape(3, 4)
print("Reshaped (3x4):\n", reshaped)

print("\n--- 6. Boolean Masking ---")
mask = nums > 25
print("Values > 25 mask:", mask)
print("Filtered values :", nums[mask])

print("\n--- 7. Matrix Multiplication ---")
m1 = np.array([[1, 2], [3, 4]])
m2 = np.array([[5, 6], [7, 8]])
print("Matrix Product (m1 @ m2):\n", np.matmul(m1, m2))
