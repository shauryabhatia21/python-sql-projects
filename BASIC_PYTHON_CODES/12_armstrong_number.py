# 12. ARMSTRONG NUMBER CHECKER
# A number is Armstrong if sum of cubes of its digits equals the number (e.g. 153 = 1^3 + 5^3 + 3^3)

n = int(input("Enter number: "))

temp = n
s = 0

while n > 0:
    digit = n % 10
    s += (digit ** 3)
    n = n // 10

if s == temp:
    print(f"{temp} is an Armstrong Number")
else:
    print(f"{temp} is Not an Armstrong Number")
