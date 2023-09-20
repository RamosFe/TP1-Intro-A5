import os
import socket
from src.lib.constants import BUFFER_SIZE, CHUNK_SIZE
from src.lib.fs.fs_list_files import FileSystemLister
from threading import Event




def list_files_server(connection: socket.socket,addr: str, max_chunk_size: int, mount_path: str, exit_signal : Event):
    with connection:
        fs_handler = FileSystemLister(mount_path, max_chunk_size)
        fs_handler.list_files(connection,exit_signal)
    
        
    