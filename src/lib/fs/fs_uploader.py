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
            return -1
        except Exception as e:
            print("😨 An exception occurred, please try again 😨")
            return -1

    def is_file(file_path):
        return os.path.exists(file_path) and os.path.isfile(file_path)

    def upload_file(
        self, socket: socket.socket, path: str, name: str, verbose: bool, server: bool
    ):
        try:
            with open(path, "rb") as file:
                steps = ceil(os.path.getsize(path) / self._chunk_size)
                if verbose:
                    print(f"-> Uploading file {name}")

                if server:
                    for chunk in iter(lambda: file.read(self._chunk_size), b""):
                        socket.send(chunk)
                else:
                    with alive_bar(steps, bar="bubbles", title=f"↑ {name}") as bar:
                        for chunk in iter(lambda: file.read(self._chunk_size), b""):
                            socket.send(chunk)
                            bar()

                    bar.text("✔ Done ✔")

        except FileNotFoundError as e:
            print(f"❌ File not found {path} ❌")
            socket.send(b"ERR File not found")

        except Exception as e:
            print(f"😨 An exception occurred, please try again 😨 -> {e}")
