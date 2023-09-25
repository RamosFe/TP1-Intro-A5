import os
import socket
from alive_progress import alive_bar
from threading import Event


class FileSystemUploaderServer:
    def __init__(self, chunk_size: int):
        self._chunk_size = chunk_size

    def get_file_size(self, path: str) -> int:
        return os.path.getsize(path)

    def upload_file(
        self,
        sender: socket.socket,
        addr: tuple[str, int],
        path: str,
        name: str,
        verbose: bool,
        exit_signal: Event,
    ):
        # TODO Handle Errors
        with open(path, "rb") as file:
            if verbose:
                print(f"-> Uploading file {name}")

            for chunk in iter(lambda: file.read(self._chunk_size), b""):
                if exit_signal.is_set():
                    sender.sendto(chunk, addr)
                    print("Closing server due to signal")
                    break
                sender.sendto(chunk, addr)
