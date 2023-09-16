import socket

from typing import List, Dict

HARDCODED_HOST = '127.0.0.1'
HARDCODED_PORT = 6000
HARDCODED_MAX_SIZE = 1024

def main(host: str, port: int, max_socket_size: int):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print("Waiting connection")
    while True:
        conn, addr = server_socket.accept()
        data = conn.recv(max_socket_size)
        print(f"{addr} sender: data")
        conn.sendall("ACK")

        conn.close()

if __name__ == '__main__':
    main(HARDCODED_HOST, HARDCODED_PORT, HARDCODED_MAX_SIZE)
