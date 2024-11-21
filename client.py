import socket
import pickle
from rsa import encrypt

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = '127.0.0.1'
    port = 8080

    client_socket.connect((host, port))
    return client_socket

def send_messages(public_key, client_socket):
    while True:
        message = input('Masukkan pesan: ')

        encrypted_message = encrypt(public_key, message)
        print('Pesan awal', message)
        print('Pesan terenkripsi', encrypted_message)
        print("\n")

        client_socket.send(pickle.dumps(encrypted_message))

if __name__ == "__main__":
    client_socket = connect_to_server()
    public_key = pickle.loads(client_socket.recv(4096))

    send_messages(public_key, client_socket)
    client_socket.close()