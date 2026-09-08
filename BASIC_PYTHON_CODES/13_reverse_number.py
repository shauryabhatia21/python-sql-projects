# 13. REVERSE A NUMBER
# Reverses any integer using arithmetic operations (e.g. 195 -> 591)

n = int(input("Enter number to reverse: "))

temp = n
rev = 0

while n > 0:
    digit = n % 10
    rev = rev * 10 + digit
    n = n // 10

print(f"Original Number: {temp}")
print(f"Reversed Number: {rev}")
