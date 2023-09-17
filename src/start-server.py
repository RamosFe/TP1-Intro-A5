import socket
from threading import Thread, Event
from typing import List

from src.lib.download import download
from src.lib.constants import CHUNK_SIZE

HARDCODED_HOST = '127.0.0.1'
HARDCODED_PORT = 6000


def main(host: str, port: int, max_chunk_size: int):
    exit_signal_event = Event()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((host, port))
    server_socket.listen()

    print("Waiting connection")
    clients: List[Thread] = []
    while True:
        try:
            conn, addr = server_socket.accept()
            new_client = Thread(target=download, args=(conn, addr, max_chunk_size, exit_signal_event))
            clients.append(new_client)
            new_client.start()
        except KeyboardInterrupt:
            print("CTRL-C")
            exit_signal_event.set()

            for client in clients:
                client.join()
            server_socket.close()
            break


if __name__ == '__main__':
    main(HARDCODED_HOST, HARDCODED_PORT, CHUNK_SIZE)
