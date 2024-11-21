import random

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(pow(num, 0.5)) + 1):
        if num % i == 0:
            return False
    return True

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def multiplicative_inverse(e, phi):
    d = 0
    x1, x2 = 0, 1
    y1, y2 = 1, 0
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = y2 - temp1 * y1

        x2 = x1
        x1 = x
        y2 = y1
        y1 = y

    if temp_phi == 1:
        d = y2 + phi

    return d

def generate_large_primes():
    primes = [i for i in range(100, 1000) if is_prime(i)]
    p = random.choice(primes)
    q = random.choice(primes)
    
    while p == q:
        q = random.choice(primes)
    return p, q

def generate_keypair():
    p, q = generate_large_primes()
    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(1, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(1, phi)

    d = multiplicative_inverse(e, phi)

    public_key = (e, n)
    private_key = (d, n)
    
    return public_key, private_key

def encrypt(public_key, plain_text):
    e, n = public_key
    cipher = [pow(ord(char), e, n) for char in plain_text]
    return cipher

def decrypt(private_key, cipher_text):
    d, n = private_key
    plain = [chr(pow(char, d, n)) for char in cipher_text]
    return ''.join(plain)