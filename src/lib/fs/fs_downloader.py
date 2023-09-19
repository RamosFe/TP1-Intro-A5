import os
import socket
from threading import Event

from src.lib.constants import UPLOAD_FINISH_MSG


class FileSystemDownloader:
    def __init__(self, mount_path: str, chunk_size: int):        
        if not os.path.exists(mount_path):
            os.makedirs(mount_path)
        self._mount_path = mount_path
        self._chunk_size = chunk_size

    def file_exists(self, filename: str) -> bool:
        return os.path.exists(os.path.join(self._mount_path, filename))



    def download_file(self, socket: socket.socket, path: str, exit_signal: Event):
        with open(os.path.join(self._mount_path, path), 'wb') as file:
            while not exit_signal.isSet():
                data = socket.recv(self._chunk_size)

                if data == UPLOAD_FINISH_MSG:
                    break

                print(data.decode())
                file.write(data)
