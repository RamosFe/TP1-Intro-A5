import socket
from threading import Event


def download(connection: socket.socket, addr: str, max_chunk_size: int, exit_signal: Event):
    with connection:
        data = connection.recv(max_chunk_size)

        # TODO Refactor entity
        command, filename, size = data.decode().split()
        print(f"{addr}: {command} file: {filename} size: {size}")
        connection.sendall("OK".encode())

        while not exit_signal.isSet():
            data = connection.recv(max_chunk_size)

            if not data:
                break

            print(f"{addr} sender: {data.decode()}")

        print(f"Closing {addr}")
        connection.close()

