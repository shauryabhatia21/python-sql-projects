# 06. FACTORIAL OF A NUMBER
# Calculates n! (n factorial) using a for loop

n = int(input("Enter your number: "))

fact = 1
for i in range(1, n + 1):
    fact = fact * i

print(f"Factorial of {n} is: {fact}")
