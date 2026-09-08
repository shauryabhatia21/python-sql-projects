# 23. REVERSE PYRAMID COUNTDOWN PATTERN
# Prints counting down rows from n

n = int(input("Enter value of n (e.g. 5): "))

print("Pattern Output:")
for i in range(1, n + 1):
    for k in range(n + 1, i - 1, -1):
        print(k, end=' ')
    print()

# Expected Output (for n=5):
# 6 5 4 3 2 1 
# 6 5 4 3 2 
# 6 5 4 3 
# 6 5 4 
# 6 5 
