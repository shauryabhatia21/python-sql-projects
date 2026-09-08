# 15. COUNT EVEN AND ODD NUMBERS
# Takes inputs repeatedly until a negative number is entered, counting evens and odds

count = 0
even = 0
odd = 0

print("Enter positive numbers (enter a negative number to stop):")
while True:
    a = int(input("Enter number: "))
    if a < 0:
        break
    count += 1
    if a % 2 == 0:
        even += 1
    else:
        odd += 1

print("-" * 50)
print(f"Total Numbers Entered: {count}")
print(f"Even Numbers: {even}")
print(f"Odd Numbers: {odd}")
