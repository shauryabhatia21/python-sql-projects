# 02. POWER CALCULATION (a raised to power b)
# Calculates a^b using repeated multiplication

a = int(input("Enter base number (a): "))
b = int(input("Enter exponent power (b): "))

result = 1
for i in range(1, b + 1):
    result = result * a

print(f"{a} raised to power {b} is: {result}")
