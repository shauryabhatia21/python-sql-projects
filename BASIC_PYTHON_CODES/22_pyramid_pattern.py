# 22. PYRAMID PATTERN
# Prints centered number pyramid using leading spaces

print("Pattern Output:")
for i in range(1, 5):
    for k in range(4, i - 1, -1):
        print(end=' ')
    for j in range(1, i + 1):
        print(j, end='  ')
    print()

# Expected Output:
#     1  
#    1  2  
#   1  2  3  
#  1  2  3  4
