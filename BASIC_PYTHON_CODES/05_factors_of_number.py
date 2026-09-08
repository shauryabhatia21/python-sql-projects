# 05. FACTORS OF A GIVEN NUMBER
# Finds and prints all divisors / factors of a number

n = int(input("Enter your number: "))

print(f"Factors of {n} are:")
for i in range(1, n + 1):
    if n % i == 0:
        print(i, end=' ')
print()
