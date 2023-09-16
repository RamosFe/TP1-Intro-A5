import socket
from threading import Thread, Event

from typing import List

HARDCODED_HOST = '127.0.0.1'
HARDCODED_PORT = 6004
HARDCODED_MAX_SIZE = 1024

exit_signal = Event()
def client_logic(connection: socket.socket, addr, max_size: int):
    with connection:
        data = connection.recv(max_size)
        command, filename, size = data.decode().split()
        print(f"{addr}: {command} file: {filename} size: {size}")
        connection.sendall("OK".encode())

        while not exit_signal.set:
            data = connection.recv(max_size)
            
            if not data:
                break

            print(f"{addr} sender: {data.decode()}")
    print(f"Closing  {addr}") 
    connection.close()


def main(host: str, port: int, max_socket_size: int):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((host, port))
    server_socket.listen()

    print("Waiting connection")
    clients: List[Thread] = []
    while True:
        try:
            conn, addr = server_socket.accept()
            new_client = Thread(target=client_logic, args=(conn, addr, max_socket_size))
            clients.append(new_client)
            new_client.start()
        except KeyboardInterrupt:
            print("CTRL-C")
            exit_signal.set()

            for client in clients:
                client.join()
            server_socket.close()
            break

if __name__ == '__main__': 
    main(HARDCODED_HOST, HARDCODED_PORT, HARDCODED_MAX_SIZE)

