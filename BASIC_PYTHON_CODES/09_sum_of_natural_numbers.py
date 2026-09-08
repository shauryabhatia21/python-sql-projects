# 09. SUM OF FIRST N NATURAL NUMBERS
# Calculates 1 + 2 + 3 + ... + n

n = int(input("Enter value of n: "))

total = 0
for i in range(1, n + 1):
    total += i

print(f"Sum of first {n} natural numbers is: {total}")
