# 18. SLANT NUMBER TRIANGLE PATTERN (1 to 5)
# Prints an incremental triangle of numbers

print("Pattern Output:")
for i in range(1, 6):
    for j in range(1, i + 1):
        print(j, end=' ')
    print()

# Expected Output:
# 1 
# 1 2 
# 1 2 3 
# 1 2 3 4 
# 1 2 3 4 5
