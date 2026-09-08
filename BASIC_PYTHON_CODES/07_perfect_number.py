# 07. PERFECT NUMBER CHECKER
# A number is perfect if the sum of its proper divisors equals the number itself (e.g., 6 = 1 + 2 + 3)

n = int(input("Enter your number: "))

s = 0
for i in range(1, n):
    if n % i == 0:
        s += i

if s == n:
    print(f"{n} is a Perfect Number")
else:
    print(f"{n} is Not a Perfect Number")
