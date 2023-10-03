import os
import math
from alive_progress import alive_bar
from lib.rdt.rdt_sw_socket import RdtSWSocketClient
from lib.sr_rdt.selective_repeat import SelectiveRepeatRDT


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
        
    # Open the file in binary mode for reading
        with open(path, "rb") as file:
            # Calculate the number of progress steps based on chunk size and file size
            steps = math.ceil(self.get_file_size(path) / self._chunk_size)

            # Print information about the file being uploaded if verbose is True
            if verbose:
                print(f"-> Uploading file {name}")

            # Initialize a progress bar
            with alive_bar(steps, bar="bubbles", title=f"↑ {name}") as bar:
                # Iterate over the file in chunks of size _chunk_size
                for chunk in iter(lambda: file.read(self._chunk_size), b""):
                    try:
                        if senderSW is not None:
                            # Send the chunk using senderSW (stop-and-wait)
                            senderSW.sendto(chunk, addr)
                        else:
                            # Send the chunk using senderSR (selective repeat)
                            senderSR.send_message(chunk)

                    except TimeoutError:
                        raise TimeoutError
                    
                    # Update the progress bar
                    bar()

            # Display a completion message when the upload is finished
            bar.text("✔ Done ✔")
