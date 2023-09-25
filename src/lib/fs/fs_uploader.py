import os
import socket
from threading import Event

from lib.rdt.socket_interface import SocketInterface


class FileSystemUploaderServer:
    """
    A class for uploading files from the local file system to a client.

    Args:
        chunk_size (int): The size of data chunks to be sent at a time.

    Attributes:
        _chunk_size (int): The size of data chunks to be sent at a time.

    Methods:
        get_file_size(path: str) -> int:
            Get the size of a file.

        upload_file(
            sender: socket.socket, addr: tuple[str, int], path: str, name: str,
            verbose: bool, exit_signal: Event
        ):
            Upload a file to a client socket.

    """
    def __init__(self, chunk_size: int):
        self._chunk_size = chunk_size

    def get_file_size(self, path: str) -> int:
        """
        Get the size of a file.

        Args:
            path (str): The path to the file.

        Returns:
            int: The size of the file in bytes.
        """
        return os.path.getsize(path)

    def upload_file(
        self,
        sender: SocketInterface,
        addr: tuple[str, int],
        path: str,
        name: str,
        verbose: bool,
        exit_signal: Event,
    ):
        """
        Upload a file to a client socket.

        Args:
            sender (socket.socket): The socket used to send data to the client.
            addr (tuple[str, int]): The address of the client.
            path (str): The path to the file to be uploaded.
            name (str): The name of the file being uploaded.
            verbose (bool): If True, print verbose information about the upload.
            exit_signal (threading.Event): An event signaling whether to exit the upload process.

        Note:
            The upload process continues until either the entire file is sent or an exit signal is set.
        """
        with open(path, "rb") as file:
            if verbose:
                print(f"-> Uploading file {name}")

            for chunk in iter(lambda: file.read(self._chunk_size), b""):
                if exit_signal.is_set():
                    sender.sendto(chunk, addr)
                    print("Closing server due to signal")
                    break
                sender.sendto(chunk, addr)
