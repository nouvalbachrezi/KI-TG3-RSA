import socket
import pickle
from threading import Thread
from rsa import generate_keypair, decrypt

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = '127.0.0.1'
    port = 8080

    server_socket.bind((host, port))
    server_socket.listen(5)

    print('Server listening....')

    return server_socket

def handle_client(client_socket, client_address, public_key, private_key):
    print(f"Menerima koneksi dari {client_address}")

    client_socket.send(pickle.dumps(public_key))

    while True:
        encrypted_message = client_socket.recv(4096)
        encrypted_message = pickle.loads(encrypted_message)

        decrypted_message = decrypt(private_key, encrypted_message)
        print(f"Menerima pesan terenkripsi dari {client_address}: {encrypted_message}")
        print(f"Pesan terdekripsi: {decrypted_message}\n")

        if decrypted_message == 'quit':
            print(f"Klien {client_address} terputus")
            client_socket.close()
            break

if __name__ == "__main__":
    server_socket = start_server()
    public_key, private_key = generate_keypair()

    while True:
        client_socket, addr = server_socket.accept()

        client_thread = Thread(target=handle_client, args=(client_socket, addr, public_key, private_key))
        client_thread.start()