# 11. SUM OF ONLY EVEN DIGITS
# Extracts digits and sums only the even ones (e.g. 245 -> 2 + 4 = 6)

n = int(input("Enter number: "))

temp = n
s = 0

while n > 0:
    digit = n % 10
    if digit % 2 == 0:
        s += digit
    n = n // 10

print(f"Sum of even digits of {temp} is: {s}")
