import socket
from des import encryption, decryption
from rsacustom import encrypt, PublicKeyAuthority

class Client:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8080
        self.pka = PublicKeyAuthority()  # Public Key Authority

        # Registrasi public key server ke PKA (simulasi)
        server_public_key = (65537, 1234567890123456789012345678901234567890)  # Contoh public key server
        self.pka.register_key("server", server_public_key)

    def open_socket(self):
        """Membuka koneksi socket ke server."""
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.host, self.port))
            print(f"Terhubung ke server di {self.host}:{self.port}")
        except Exception as e:
            print(f"Gagal terhubung ke server: {e}")
            exit(1)

    def run(self):
        """Memulai komunikasi dengan server."""
        self.open_socket()
        try:
            while True:
                print("Masukkan Pesan (atau ketik 'exit' untuk keluar):")
                msg = input()
                if msg.lower() == 'exit':
                    print("Mengakhiri koneksi...")
                    break

                # Langkah 1: Enkripsi Kunci DES menggunakan RSA
                des_key = 'N8srVEjRsHlIoOMk'  # Contoh kunci DES
                username = "server"  # Nama pengguna yang sesuai untuk public key
                server_public_key = self.pka.get_public_key(username)  # Ambil public key server dari PKA

                if not server_public_key:
                    print("Public key server tidak ditemukan!")
                    break

                # Enkripsi kunci DES menggunakan public key server
                encrypted_des_key = encrypt(server_public_key, des_key)

                # Langkah 2: Enkripsi Pesan menggunakan DES
                encrypted_msg = encryption(msg)

                # Kirim kunci DES yang terenkripsi dan pesan yang terenkripsi
                payload = bytes(str(encrypted_des_key), 'utf-8') + b'|' + encrypted_msg.encode('utf-8')
                self.client.send(payload)

                # Terima pesan terenkripsi dari server
                encrypted_response = self.client.recv(1024).decode('utf-8')
                print(f"\nCiphertext dari server: {encrypted_response}")

                # Dekripsi Pesan
                decrypted_response = decryption(encrypted_response)
                print(f"Pesan yang telah didekripsi: {decrypted_response}\n")

        except Exception as e:
            print(f"Terjadi kesalahan saat berkomunikasi dengan server: {e}")
        finally:
            self.client.close()
            print("Koneksi ditutup.")

if __name__ == "__main__":
    client = Client()
    client.run()