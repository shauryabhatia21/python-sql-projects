import random

def genAcno():
    """Generates an 8-digit random account number string."""
    digits = [str(random.randint(0, 9)) for _ in range(8)]
    return "".join(digits)

def genphon():
    """Generates a unique masked contact ID."""
    a = random.randint(0, 9)
    b = random.randint(0, 9)
    c = random.randint(0, 9)
    d = random.randint(0, 9)
    e = random.randint(0, 9)
    f = random.randint(0, 9)
    g = random.randint(0, 9)
    h = random.randint(0, 9)
    return f"XI{a}{b}{c}XO{d}{e}N{f}P{g}{h}"
