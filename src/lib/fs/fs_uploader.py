import os
import socket


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
