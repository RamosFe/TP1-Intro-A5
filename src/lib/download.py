import socket
from threading import Event

from src.lib.command_parser import Command


def download(connection: socket.socket, addr: str, max_chunk_size: int, exit_signal: Event):
    with connection:
        data = connection.recv(max_chunk_size)

        # TODO Refactor entity
        command = Command.from_str(data.decode())
        print(f"{addr}: {command.option.value} file: {command.name} size: {command.size}")
        connection.sendall("OK".encode())

        while not exit_signal.isSet():
            data = connection.recv(max_chunk_size)

            if not data:
                break

            print(f"{addr} sender: {data.decode()}")

        print(f"Closing {addr}")
        connection.close()

