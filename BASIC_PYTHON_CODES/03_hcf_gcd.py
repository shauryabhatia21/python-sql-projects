# 03. HCF / GCD OF TWO NUMBERS
# Finds Highest Common Factor of two numbers using for loop

a = int(input("Enter first number: "))
b = int(input("Enter second number: "))

m = min(a, b)
hcf = 1

for i in range(1, m + 1):
    if a % i == 0 and b % i == 0:
        hcf = i

print(f"HCF of {a} and {b} is: {hcf}")
