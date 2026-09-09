import random
def genphon():
    a=random.randint(0,9)
    b=random.randint(0,9)
    c=random.randint(0,9)
    d=random.randint(0,9)
    e=random.randint(0,9)
    f=random.randint(0,9)
    g=random.randint(0,9)
    h=random.randint(0,9)
    phon="XI"+str(a)+str(b)+str(c)+"XO"+str(d)+str(e)+"N"+str(f)+"P"+str(g)+str(h)
    return phon
