# 08. MULTIPLICATION TABLE
# Prints mathematical table of any number from 1 to 10

n = int(input("Enter number for table: "))

print(f"--- Multiplication Table of {n} ---")
for i in range(1, 11):
    print(f"{n} x {i} = {n * i}")
