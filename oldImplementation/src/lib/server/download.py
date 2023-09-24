
from threading import Event
from src.lib.commands import Command, CommandResponse
import socket
from queue import Queue
from src.lib.fs.fs_downloader import FileSystemDownloader

# ESTO ES DEL LADO DEL SERVIDOR POR AHORA
#CLIENTE HACE UPLOAD, SERVIDOR HACE DOWNLOAD 

#CLIENTE:   UPLOAD filename size
#SERVER:    OK/ERR
#CLIENTE:   manda archivo


def download_file(channel_from_client: Queue, channel_to_sender: Queue, addr: str, max_chunk_size: int, mount_path: str, exit_signal: Event, comm: Command):
    fs_handler = FileSystemDownloader(mount_path, max_chunk_size)
    if fs_handler.file_exists(filename=comm.name):
        response = CommandResponse.err_response(f'ERR file {comm.name} already exists').to_str()
        channel_to_sender.put((response.encode(),addr))
    else:
        print(f'File {comm.name}, sending ok')
        response = CommandResponse.ok_response().to_str()
        channel_to_sender.put((response.encode(),addr))
        print(f'File {comm.name}, sending file')
        fs_handler.download_file(channel_from_client, comm.name, exit_signal, 0, True) # TODO change size

            
