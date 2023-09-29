import os
import queue
from threading import Event
from lib.rdt.rdt_sw_socket import RdtSWSocketClient
from lib.constants import UPLOAD_FINISH_MSG, HARDCODED_TIMEOUT


class FileSystemDownloaderServer:
    """
    A class for downloading files to the local file system.

    Args:
        mount_path (str): The path to the directory where files will be downloaded.
        chunk_size (int): The size of data chunks to be downloaded at a time.

    Attributes:
        _mount_path (str): The path to the directory where files will be downloaded.
        _chunk_size (int): The size of data chunks to be downloaded at a time.

    Methods:
        file_exists(filename: str) -> bool:
            Check if a file with the given filename exists in the download directory.

        download_file(channel: queue.Queue, path: str, exit_signal: Event):
            Download a file from a queue channel and save it to the specified path.

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

    def download_file(self, channel: queue.Queue,socket: RdtSWSocketClient, path: str, exit_signal: Event):
        """
        Download a file from a queue channel and save it to the specified path.

        Args:
            channel (queue.Queue): A queue containing data chunks to be downloaded.
            path (str): The path where the file will be saved.
            exit_signal (threading.Event): An event signaling whether to exit the download process.

        Raises:
            queue.Empty: If the queue is empty and the exit_signal is not set.

        Note:
            The download process continues until either the queue is empty and the exit_signal is not set
            or an "UPLOAD_FINISH_MSG" is received in the data.
        """
        with open(os.path.join(self._mount_path, path), "wb") as file:
            try:
                while not exit_signal.is_set():
                    data = socket.recv_with_queue(channel)
                    print(f"data recibida es {data}")
                    if data is None:
                        continue
                    if UPLOAD_FINISH_MSG.encode() in data:
                        print(f"falta escribir esta data {data[:data.index(UPLOAD_FINISH_MSG.encode())]}")
                        # file.write(data[:data.index(UPLOAD_FINISH_MSG.encode())])
                        return
                    print(f"Estoy escribiendo esta data {data}")
                    file.write(data)
                print("Closing download")
            except queue.Empty as e:
                if exit_signal.is_set():
                    print("Closing server due to signal")
                    return
                else:
                    raise e
