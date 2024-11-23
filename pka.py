import rsacustom

class PublicKeyAuthority:
    def __init__(self):
        # Menghasilkan pasangan kunci PKA (RSA) mengelola kunci publik, baik kunci publik milik PKA itu sendiri maupun kunci publik entitas lain yang terdaftar.
        self.public_key, self.private_key = rsa.newkeys(512)  # 512-bit key, bisa disesuaikan
        self.registered_keys = {}  # Menyimpan kunci publik entitas lain
    
    def register_key(self, entity_name, public_key):
        """Menambahkan kunci publik entitas lain ke daftar PKA."""
        self.registered_keys[entity_name] = public_key
    
    def get_public_key(self, entity_name):
        """Mengambil kunci publik untuk entitas tertentu.""" #Fungsi ini akan mencari entity_name dalam dictionary self.registered_keys dan mengembalikan kunci publik yang terdaftar.
        return self.registered_keys.get(entity_name)
    
    def get_pka_public_key(self):
        """Mengambil kunci publik PKA."""
        return self.public_key

# Contoh penggunaan:
pka = PublicKeyAuthority()
# Menyimpan kunci publik untuk server
server_public_key = (65537, 1234567890123456789012345678901234567890)  # Contoh kunci publik server
pka.register_key("server", server_public_key)

# Mengambil kunci publik server
public_key_server = pka.get_public_key("server")
print(public_key_server)
