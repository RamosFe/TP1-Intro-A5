
import os
import socket
from math import ceil

from src.lib.constants import LIST_FILES_FINISH




class FileSystemLister:
    def __init__(self,mount_path: str,chunk_size: int):
        self._chunk_size = chunk_size
        self._mount_path = mount_path

    def list_files(self,socket: socket.socket,exit_signal):
        try:
            entries = '\n'.join(os.listdir(self._mount_path))
            num_chunks = len(entries) // self._chunk_size
            for i in range(num_chunks + 1):
                if not exit_signal.isSet():
                    chunk = entries[i * self._chunk_size : (i+1) * self._chunk_size]
                    socket.send(chunk.encode())
            socket.send(LIST_FILES_FINISH)
        
        except Exception as e:
            print(f'Error: {e}')
            raise e