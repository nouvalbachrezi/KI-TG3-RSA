import random
import math
from sympy import mod_inverse

class PublicKeyAuthority:
    def __init__(self):
        self.public_keys = {}
        self.private_keys = {}  # Menambahkan private_keys untuk menyimpan private key

    def register_key(self, username, public_key, private_key=None):
        """Mendaftarkan public key dan private key untuk pengguna tertentu."""
        self.public_keys[username] = public_key
        if private_key:  # Jika private key diberikan, daftarkan juga
            self.private_keys[username] = private_key

    def get_public_key(self, username):
        """Mengambil public key pengguna berdasarkan username."""
        return self.public_keys.get(username)

    def get_private_key(self, username):
        """Mengambil private key pengguna berdasarkan username."""
        return self.private_keys.get(username)


def is_prime(n):
    """Memeriksa apakah suatu bilangan adalah bilangan prima."""
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_keypair(bits=1024):
    """Menghasilkan pasangan kunci RSA (public key dan private key)."""
    # Hasilkan dua bilangan prima berbeda p dan q
    p = q = 1
    while not is_prime(p):
        p = random.getrandbits(bits)
    while not is_prime(q) or p == q:
        q = random.getrandbits(bits)
    
    # n = p * q
    n = p * q
    phi = (p - 1) * (q - 1)

    # e dipilih menjadi koprima dengan phi
    e = random.randrange(2, phi)
    while math.gcd(e, phi) != 1:
        e = random.randrange(2, phi)

    # d adalah kebalikan modular dari e mod phi
    d = mod_inverse(e, phi)

    # Public key is (e, n)
    # Private key is (d, n)
    return ((e, n), (d, n))

def encrypt(public_key, plaintext):
    """Mengenkripsi teks menggunakan public key."""
    e, n = public_key
    return [pow(ord(char), e, n) for char in plaintext]

def decrypt(private_key, ciphertext):
    """Mendekripsi teks menggunakan private key."""
    d, n = private_key
    return ''.join([chr(pow(char, d, n)) for char in ciphertext])
