"""
NumPy (Numerical Python) Foundations & Classroom Demonstrations
Author: Shaurya Bhatia (Bennett University)
--------------------------------------------------------------------------------
NumPy Provides:
1. Fast multi-dimensional arrays (ndarray)
2. Vectorized mathematical functions
3. Linear algebra tools
4. Random number generation
5. Broadcasting (vectorized computation without Python loops)

Why NumPy is Faster Than Standard Lists:
1. Homogeneous contiguous memory storage
2. Cache-friendly C-level pointers
3. Native vectorization
"""

import numpy as np

# ==============================================================================
# SECTION 1: ARRAY PROPERTIES
# ==============================================================================
arr8 = np.array([[1, 2, 3], [4, 5, 6]])

# 1. Dimensions (ndim)
print("Dimensions:", arr8.ndim)

# 2. Shape (rows, cols)
print("Shape:", arr8.shape)

# 3. Total size (count of elements)
print("Total Elements:", arr8.size)

# 4. Data type
print("Data Type:", arr8.dtype)
print("=" * 50)

# ==============================================================================
# SECTION 2: CREATING ARRAYS
# ==============================================================================
# 1D Array
arr1 = np.array([1, 2, 3])
print("1D Array:", arr1)

# 2D Array
arr2 = np.array([[1, 2, 3], [4, 5, 6]])
print("2D Array:\n", arr2)

# Zeros Array
arr3 = np.zeros((2, 3))
print("Zeros (2x3):\n", arr3)

# Ones Array
arr4 = np.ones((2, 2))
print("Ones (2x2):\n", arr4)

# Identity Matrix
arr5 = np.eye(3)
print("Identity Matrix (3x3):\n", arr5)

# arange function (start, stop, step)
arr6 = np.arange(0, 10, 2)
print("Arange (0 to 10 step 2):", arr6)

# linspace (start, stop, number_of_points)
arr7 = np.linspace(0, 1, 5)
print("Linspace (5 points between 0 and 1):", arr7)
print("=" * 50)

# ==============================================================================
# SECTION 3: INDEXING, SLICING, VIEWS VS COPIES
# ==============================================================================
a1 = np.array([11, 22, 33, 44, 55])
# Slicing creates a view:
a2 = a1[:]
a2[1] = 99
print("Modified via view (affects original):", a1)

# Making explicit copy:
a3 = a1.copy()
a3[1] = 22
print("Original unchanged by copy mutation:", a1)
print("Independent copy:", a3)
print("=" * 50)

# ==============================================================================
# SECTION 4: MATHEMATICAL & AGGREGATION OPERATIONS
# ==============================================================================
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print("Element-wise Addition (a + b):", a + b)
print("Element-wise Multiplication (a * b):", a * b)
print("Square Root:", np.sqrt(a))
print("Exponential:", np.exp(a))
print("Natural Log:", np.log(a))

agg_arr = np.array([10, 20, 30, 40])
print("Sum:", np.sum(agg_arr))
print("Mean:", np.mean(agg_arr))
print("Std Deviation:", np.std(agg_arr))
print("=" * 50)

# ==============================================================================
# SECTION 5: RESHAPING & BOOLEAN MASKING
# ==============================================================================
reshaped = np.arange(1, 13).reshape(3, 4)
print("Reshaped (3x4):\n", reshaped)

# Automatic dimension inference with -1:
auto_reshaped = np.arange(1, 13).reshape(3, -1)
print("Auto-inferred Reshape (3x-1):\n", auto_reshaped)

# Boolean masking
mask_arr = np.array([10, 20, 30, 40])
mask = mask_arr > 25
print("Boolean Mask (> 25):", mask)
print("Masked Elements:", mask_arr[mask])

# Matrix multiplication (dot product)
m1 = np.array([[1, 2], [3, 4]])
m2 = np.array([[5, 6], [7, 8]])
print("Matrix Dot Product:\n", np.dot(m1, m2))

# Random integers
random_nums = np.random.randint(1, 10, size=5)
print("Random Integers (1 to 10):", random_nums)
print("=" * 50)
