import random
def genissue():
    a=random.randint(0,9)
    b=random.randint(0,9)
    c=random.randint(0,9)
    d=random.randint(0,9)
    e=random.randint(0,9)
    f=random.randint(0,9)
    g=random.randint(0,9)
    h=random.randint(0,9)
    acno='IS'+str(a)+'TC'+str(b)+str(c)+str(d)
    return acno
