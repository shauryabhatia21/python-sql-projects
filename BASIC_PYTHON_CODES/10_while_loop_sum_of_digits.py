# 10. SUM OF DIGITS (WHILE LOOP)
# Extracts each digit and calculates their sum (e.g. 195 -> 1 + 9 + 5 = 15)

n = int(input("Enter number: "))

temp = n
s = 0

while n > 0:
    digit = n % 10
    s += digit
    n = n // 10

print(f"Sum of digits of {temp} is: {s}")
