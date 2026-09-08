# 19. INVERTED NUMBER TRIANGLE PATTERN
# Prints a reverse decremental triangle from 5 down to 1

print("Pattern Output:")
for i in range(7, 1, -1):
    for j in range(1, i - 1):
        print(j, end=' ')
    print()

# Expected Output:
# 1 2 3 4 5 
# 1 2 3 4 
# 1 2 3 
# 1 2 
# 1
