# 01. FOR LOOP BASICS
# Demonstrates vertical, horizontal, stepped, reverse, and 1-to-n iterations.

print("--- 1. Vertical Output (1 to 10) ---")
for i in range(1, 11):
    print(i)

print("\n--- 2. Horizontal Output (1 to 10) ---")
for i in range(1, 11):
    print(i, end='  ')
print()

print("\n--- 3. Stepped Output (Gap of 2) ---")
for i in range(1, 11, 2):
    print(i, end='  ')
print()

print("\n--- 4. Reverse Output (11 down to 1) ---")
for i in range(11, 0, -1):
    print(i, end='  ')
print()

print("\n--- 5. Horizontal 1 to n ---")
n = int(input("Enter value of n: "))
for i in range(1, n + 1, 1):
    print(i, end="   ")
print()
