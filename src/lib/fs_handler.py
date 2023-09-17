import os
import socket
from threading import Event

from src.lib.constants import UPLOAD_FINISH_MSG

class FileSystemUploader:
    def __init__(self, chunk_size: int):
        self._chunk_size = chunk_size

    def get_file_size(self, path: str):
        try:
            return os.path.getsize(path)

        # TODO Handle error nicely
        except FileNotFoundError as e:
            print(f"File not found {path}")
            raise e
        except Exception as e:
            print(f'Error: {e}')
            raise e

    def upload_file(self, socket: socket.socket, path: str):
        try:
            with open(path, 'rb') as file:
                for chunk in iter(lambda: file.read(self._chunk_size), b''):
                    socket.send(chunk)
                print('File sent')
        # TODO Handle error nicely
        except FileNotFoundError as e:
            print(f"File not found {path}")
            raise e
        except Exception as e:
            print(f'Error: {e}')
            raise e


class FileSystemDownloader:
    def __init__(self, mount_path: str, chunk_size: int):
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

                print(data)
                file.write(data)
