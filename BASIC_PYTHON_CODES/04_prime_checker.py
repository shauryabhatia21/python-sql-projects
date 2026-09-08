# 04. PRIME NUMBER CHECKER
# Checks if a given number is prime (divisible only by 1 and itself)

n = int(input("Enter number to check: "))

if n <= 1:
    print(f"{n} is not a prime number")
else:
    count = 0
    for i in range(1, n + 1):
        if n % i == 0:
            count += 1

    if count == 2:
        print(f"{n} is a Prime Number")
    else:
        print(f"{n} is Not a Prime Number")
