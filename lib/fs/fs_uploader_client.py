import os
import math
from alive_progress import alive_bar
from lib.rdt.rdt_sw_socket import RdtSWSocketClient
from lib.rdt.socket_interface import SocketInterface
from selective_repeat import SelectiveRepeatRDT


class FileSystemUploaderClient:
    """
    A class for uploading files to a server.

    Args:
        chunk_size (int): The size of data chunks to be sent at a time.

    Attributes:
        _chunk_size (int): The size of data chunks to be sent at a time.

    Methods:
        get_file_size(path: str) -> int:
            Get the size of a file.

        upload_file(sender, addr, path: str, name: str, verbose: bool):
            Upload a file to a server.

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

    def upload_file(self, senderSW, senderSR, addr: str, path: str, name: str, verbose: bool):
        """
        Upload a file to a server.

        Args:
            sender: The object responsible for sending data to the server.
            addr: The address of the server.
            path (str): The path to the file to be uploaded.
            name (str): The name of the file being uploaded.
            verbose (bool): If True, print verbose information about the upload.

        Note:
            The upload process continues until the entire file is sent.
        """
        
        with open(path, "rb") as file:
            steps = math.ceil(self.get_file_size(path) / self._chunk_size)
            if verbose:
                print(f"-> Uploading file {name}")

            with alive_bar(steps, bar="bubbles", title=f"↑ {name}") as bar:
                # data = file.read()
                # sender.sendto(data, addr)
                # bar()
                for chunk in iter(lambda: file.read(self._chunk_size), b""):
                    try:
                        if senderSW is not None:
                            senderSW.sendto(chunk, addr)
                        else:
                            senderSR.send_message(chunk)
                    except TimeoutError:
                        raise TimeoutError
                    bar()

            bar.text("✔ Done ✔")
