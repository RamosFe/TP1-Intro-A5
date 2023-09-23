import socket
from threading import Event

from src.lib.commands import Command, CommandResponse, MessageOption
from src.lib.server.download import download_file
from src.lib.server.upload import upload_file
from src.lib.fs.fs_downloader import FileSystemDownloader


def handler(connection: socket.socket, addr: str, max_chunk_size: int, mount_path: str, exit_signal: Event, verbose: bool):
    with connection:
        if verbose:
            print(f'Connection received from {addr[0]}:{addr[1]}')

        data = connection.recv(max_chunk_size)
        command = Command.from_str(data.decode())
        if command.option == MessageOption.UPLOAD:
            return download_file(connection, addr, max_chunk_size, mount_path, exit_signal,command, verbose)        
        elif command.option == MessageOption.DOWNLOAD:
            return upload_file(connection, addr, max_chunk_size, mount_path, exit_signal,command, verbose)
        connection.close()
            