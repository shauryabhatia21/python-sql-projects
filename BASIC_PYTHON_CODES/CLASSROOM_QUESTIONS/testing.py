import os

if os.path.isfile("myfile.txt"):
    f1=open("myfile.txt","b")
    n=f1.read()
    print(n)
else:
    print("file not exist")
