import os
import socket
import math
import queue
from threading import Event
from alive_progress import alive_bar

from lib.constants import HARDCODED_BUFFER_SIZE, UPLOAD_FINISH_MSG
from lib.rdt.rdt_sw_socket import RdtSWSocketClient


class FileSystemDownloaderClient:
    """
    A class for downloading files from a server to the local file system.

    Args:
        mount_path (str): The path to the directory where files will be downloaded.
        chunk_size (int): The size of data chunks to be downloaded at a time.

    Attributes:
        _mount_path (str): The path to the directory where files will be downloaded.
        _chunk_size (int): The size of data chunks to be downloaded at a time.

    Methods:
        file_exists(filename: str) -> bool:
            Check if a file with the given filename exists in the download directory.

        download_file(socket: socket.socket, path: str, size: int, exit_signal: Event):
            Download a file from a socket and save it to the specified path with progress.

    """
    def __init__(self, mount_path: str, chunk_size: int):
        if not os.path.exists(mount_path):
            os.makedirs(mount_path)
        self._mount_path = mount_path
        self._chunk_size = chunk_size

    def file_exists(self, filename: str) -> bool:
        """
        Check if a file with the given filename exists in the download directory.

        Args:
            filename (str): The name of the file to check.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        return os.path.exists(os.path.join(self._mount_path, filename))

    def download_file(
        self, socket: RdtSWSocketClient, path: str, size: int, exit_signal: Event
    ):
        """
        Download a file from a socket and save it to the specified path with progress.

        Args:
            socket (socket.socket): The socket from which to receive file data.
            path (str): The path where the file will be saved.
            size (int): The size of the file to be downloaded.
            exit_signal (threading.Event): An event signaling whether to exit the download process.

        Note:
            The download process continues until either the socket is closed or an "UPLOAD_FINISH_MSG" is received in the data.
        """
        steps = math.ceil(size / self._chunk_size)
        with alive_bar(steps, bar="bubbles", title=f"↓ {path}") as bar:
            with open(os.path.join(self._mount_path, path), "wb") as file:
                try:
                    while not exit_signal.isSet():
                        data = socket.recv(HARDCODED_BUFFER_SIZE)
                        bar()
                        if UPLOAD_FINISH_MSG.encode() in data:
                            return # End of file
                        file.write(data)
                except queue.Empty as e:
                    if exit_signal.is_set():
                        print("Closing server due to signal")
                        return
                    else:
                        raise e

            bar.text("✔ Done ✔")
