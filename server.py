import socket
import select
import threading  
import sys
from rsacustom import decrypt, PublicKeyAuthority, generate_keypair
from des import encryption, decryption

class Server:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8080
        self.threads = []
        self.pka = PublicKeyAuthority()  # Public Key Authority

        # Generate public and private keys for the server
        public_key, private_key = generate_keypair()
        self.pka.register_key("server", public_key, private_key)  # Register server's keys

    def open_socket(self):
        """Membuka socket server dan memulai mendengarkan koneksi."""
        print(f"Starting server on {self.host}:{self.port}")
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            print("Binding the server socket...")  # Debugging print
            self.server.bind((self.host, self.port))
            print("Server started successfully")  # Debugging print
            self.server.listen(3)
            print(f"Server is listening on {self.host}:{self.port}...")
        except socket.error as e:
            print(f"Failed to bind to {self.host}:{self.port} - Error: {e}")
            sys.exit(1)

    def run(self):
        """Memulai server untuk menerima koneksi klien."""
        self.open_socket()
        input_list = [self.server]
        try:
            while True:
                print("Waiting for client connection...")
                read_ready, _, _ = select.select(input_list, [], [])
                for r in read_ready:
                    if r == self.server:
                        client_socket, client_address = self.server.accept()
                        print(f"Connection established with {client_address}")
                        c = Client(client_socket, client_address, input_list, self.pka)
                        c.start()
                        self.threads.append(c)
                    else:
                        print("Unexpected data received or connection issue")
        except KeyboardInterrupt:
            print("Shutting down the server...")
        finally:
            self.server.close()
            for c in self.threads:
                c.join()

class Client(threading.Thread):
    def __init__(self, client, address, input_list, pka):
        threading.Thread.__init__(self)
        self.sock = client
        self.SOCKET_LIST = input_list
        self.client = client
        self.address = address
        self.size = 1024
        self.pka = pka

    def run(self):
        """Mengelola komunikasi dengan klien."""
        try:
            while True:
                data = self.client.recv(self.size)
                if data:
                    try:
                        # Pisahkan kunci DES terenkripsi dan pesan terenkripsi
                        encrypted_des_key, encrypted_msg = data.split(b'|')

                        # Dekripsi kunci DES menggunakan kunci privat RSA
                        des_key = decrypt(self.pka.get_private_key("server"), encrypted_des_key)

                        # Dekripsi pesan menggunakan kunci DES
                        decrypted = decryption(encrypted_msg.decode('utf-8'))

                        print(f"\nCiphertext received: {encrypted_msg}")
                        print(f"Decrypted Text: {decrypted}\n")

                        # Balas dengan pesan terenkripsi
                        print("Masukkan Pesan untuk dikirim ke klien:")
                        response = input()
                        encrypted_response = encryption(response)
                        self.client.send(encrypted_response.encode('utf-8'))
                    except Exception as e:
                        print(f"Error processing data: {e}")
                        break
                else:
                    print(f"Client {self.address} closed the connection.")
                    self.client.close()
                    break
        except Exception as e:
            print(f"Error with client {self.address}: {e}")
        finally:
            if self.sock in self.SOCKET_LIST:
                self.SOCKET_LIST.remove(self.sock)
            self.client.close()

if __name__ == "__main__":
    try:
        print("Starting the server...")

        # Kode tambahan untuk pengujian koneksi server
        host = '127.0.0.1'
        port = 8080

        test_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            test_server.bind((host, port))
            test_server.listen(1)
            print(f"Test Server is listening on {host}:{port}...")
            client, addr = test_server.accept()
            print(f"Test Connection established with {addr}")
            client.send(b"Hello from test server")
            client.close()
        except Exception as e:
            print(f"Test Server Error: {e}")
        finally:
            test_server.close()

        # Jalankan server utama
        server = Server()
        server.run()
    except KeyboardInterrupt:
        print("Server dihentikan.")
        sys.exit(0)
