import random
def gentoken():
    a=random.randint(0,9)
    b=random.randint(0,9)
    c=random.randint(0,9)
    d=random.randint(0,9)
    acno='TO'+str(b)+str(c)+str(d)
    return acno
