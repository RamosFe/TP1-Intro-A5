import os
import socket
from alive_progress import alive_bar
import time
from math import ceil

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
        
    def is_file(file_path):
        return os.path.exists(file_path) and os.path.isfile(file_path)

    def upload_file(self, socket: socket.socket, path: str, name: str, verbose: bool, server: bool):
        try:
            with open(path, 'rb') as file:
                steps = ceil(os.path.getsize(path) / self._chunk_size)
                calibration = '{percentage:.2f}%' # not verbose
                if verbose:
                    calibration = '{step}/{steps} ({percentage:.2f}%, {elapsed}s elapsed)' # verbose
                    print(f"Uploading file {name}")

                if server:
                    for chunk in iter(lambda: file.read(self._chunk_size), b''):
                        socket.send(chunk)
                else:
                    with alive_bar(steps, bar='bubbles', title=f'↑ {name}') as bar:
                        for chunk in iter(lambda: file.read(self._chunk_size), b''):
                            socket.send(chunk)
                            bar()
                    
                    bar.text('✔ Done ✔')

                if verbose:
                    print(f"File {name} uploaded successfully")
        
        except FileNotFoundError as e:
            print(f"File not found {path}")
            raise e
        except Exception as e: # TODO Handle error nicely
            print(f'Error: {e}')
            raise e
