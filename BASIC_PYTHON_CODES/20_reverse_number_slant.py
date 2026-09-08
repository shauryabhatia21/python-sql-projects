# 20. REVERSE NUMBER SLANT PATTERN
# Prints counting down from row index down to 1

print("Pattern Output:")
for i in range(1, 6):
    for j in range(i, 0, -1):
        print(j, end='')
    print()

# Expected Output:
# 1
# 21
# 321
# 4321
# 54321
