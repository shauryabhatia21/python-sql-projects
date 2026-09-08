# 21. HOLLOW SQUARE PATTERN (STAR COMBINATION)
# Prints numbers on outer border and asterisks in the middle

print("Pattern Output:")
for i in range(1, 6):
    for j in range(1, 6):
        if i == 1 or i == 5:
            print(j, end=" ")
        else:
            if j == 1 or j == 5:
                print(j, end=' ')
            else:
                print(end="* ")
    print()

# Expected Output:
# 1 2 3 4 5
# 1 * * * 5
# 1 * * * 5
# 1 * * * 5
# 1 2 3 4 5
