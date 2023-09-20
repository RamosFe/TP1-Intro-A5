from threading import Event
from src.lib.constants import CHUNK_SIZE, BUFFER_SIZE
from src.lib.messages.commands import Command, CommandResponse
import socket
from src.lib.messages.commands import Command, CommandResponse, MessageOption

from src.lib.fs.fs_downloader import FileSystemDownloader


def download_file(connection: socket.socket, dest: str, name: str, verbose: bool, server: bool):
    fs_handler = FileSystemDownloader("./", CHUNK_SIZE)
    if fs_handler.file_exists(filename=name):
        print(f'file {name} already exists')
        return
    
    with connection:
        #print(f"{addr}: {comm.option.value} file: {comm.name} size: {comm.size}")

        command = Command(MessageOption.DOWNLOAD, name, 0)
        connection.send(command.to_str().encode())

        if verbose and not server: # TODO server side
            print(f"Senting request to server to download file {name}")

        response = connection.recv(BUFFER_SIZE).decode()
        command = CommandResponse(response)
        if command.is_error():
            print(f"❌ Request rejected -> {command._msg} ❌")
            return
        
        if verbose and not server: # TODO server side
            print("✔ Request accepted ✔")

        print(command)
        size = command.size

        # user_input = input(f"Download file {name} with size {size} bytes? [y/n]: ")
        # if user_input.lower() not in ("y", "yes"):
        #     return
        
        response = CommandResponse.ok_response().to_str()
        connection.sendall(response.encode())
        fs_handler.download_file(connection, dest, Event(), size)
        #print(f"Closing {addr}")
        connection.close()  