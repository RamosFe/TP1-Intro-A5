import socket
from threading import Event

from src.lib.messages.commands import Command, CommandResponse
from src.lib.fs.fs_downloader import FileSystemDownloader


def download(connection: socket.socket, addr: str, max_chunk_size: int, mount_path: str, exit_signal: Event):
    with connection:
        data = connection.recv(max_chunk_size)

        command = Command.from_str(data.decode())
        print(f"{addr}: {command.option.value} file: {command.name} size: {command.size}")

        fs_handler = FileSystemDownloader(mount_path, max_chunk_size)
        if fs_handler.file_exists(filename=command.name):
            response = CommandResponse.err_response(f'file {command.name} already exists').to_str()
            connection.sendall(response.encode())

            print(f"Closing {addr}")
            connection.close()
        else:
            response = CommandResponse.ok_response().to_str()
            connection.sendall(response.encode())

            fs_handler.download_file(connection, command.name, exit_signal)

            print(f"Closing {addr}")
            connection.close()

