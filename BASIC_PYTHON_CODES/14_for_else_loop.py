# 14. FOR-ELSE LOOP DEMO
# In Python, the 'else' block of a 'for' loop executes only if the loop terminates normally (without hitting a 'break')

n = int(input("Enter number to test with for-else: "))

if n <= 1:
    print(f"{n} is not a prime number")
else:
    for i in range(2, n):
        if n % i == 0:
            print(f"{n} is Not a Prime Number (divisible by {i})")
            break
    else:
        # Executes only if loop completed without breaking
        print(f"{n} is a Prime Number (for-else condition met)")
