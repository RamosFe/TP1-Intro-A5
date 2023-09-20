import socket
from threading import Event

from src.lib.messages.commands import Command, CommandResponse, MessageOption
from src.lib.controllers.download_srv import download_file
from src.lib.controllers.upload_srv import upload_file
from src.lib.fs.fs_downloader import FileSystemDownloader

#LADO SERVIDOR

def handler(connection: socket.socket, addr: str, max_chunk_size: int, mount_path: str, exit_signal: Event):
    with connection:
        data = connection.recv(max_chunk_size)

        command = Command.from_str(data.decode())

        if command.option == MessageOption.UPLOAD:
            return download_file(connection, addr, max_chunk_size, mount_path, exit_signal,command)        
        elif command.option == MessageOption.DOWNLOAD:
            return upload_file(connection, addr, max_chunk_size, mount_path, exit_signal,command)
        connection.close()
        raise Exception
            
