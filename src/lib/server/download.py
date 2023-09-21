
from threading import Event
from src.lib.commands import Command, CommandResponse
import socket

from src.lib.fs.fs_downloader import FileSystemDownloader

# ESTO ES DEL LADO DEL SERVIDOR POR AHORA
#CLIENTE HACE UPLOAD, SERVIDOR HACE DOWNLOAD 

#CLIENTE:   UPLOAD filename size
#SERVER:    OK/ERR
#CLIENTE:   manda archivo

def download_file(connection: socket.socket, addr: str, max_chunk_size: int, mount_path: str, exit_signal: Event, comm: Command):
    with connection:
        print(f"{addr}: {comm.option.value} file: {comm.name} size: {comm.size}")
        
        fs_handler = FileSystemDownloader(mount_path, max_chunk_size)
        if fs_handler.file_exists(filename=comm.name):
            response = CommandResponse.err_response(f'ERR file {comm.name} already exists').to_str()
            connection.sendall(response.encode())
        else:
            response = CommandResponse.ok_response().to_str()
            connection.sendall(response.encode())
            fs_handler.download_file(connection, comm.name, exit_signal, 0) # TODO change size
        print(f"Closing {addr}<-<-<-")
        connection.close()  

