import socket
from threading import Event

from src.lib.messages.commands import Command, CommandResponse, MessageOption
from src.lib.controllers.download_srv import download_file
from src.lib.controllers.upload_srv import upload_file
from src.lib.fs.fs_downloader import FileSystemDownloader
from src.lib.controllers.list_files_srv import list_files_server

#LADO SERVIDOR

def handler(connection: socket.socket, addr: str, max_chunk_size: int, mount_path: str, exit_signal: Event):
    with connection:
        data = connection.recv(max_chunk_size)

        command = Command.from_str(data.decode())

        match command.option:
            case MessageOption.UPLOAD:
                return download_file(connection, addr, max_chunk_size, mount_path, exit_signal,command)
            case MessageOption.DOWNLOAD:
                return upload_file(connection, addr, max_chunk_size, mount_path, exit_signal)
            case MessageOption.LIST_FILES:
                return list_files_server(connection, addr, max_chunk_size, mount_path, exit_signal)
            case _:
                print("Invalid Option")

        connection.close()
        raise Exception
            
