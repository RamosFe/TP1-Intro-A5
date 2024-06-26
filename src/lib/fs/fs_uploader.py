import os
import queue
from threading import Event


class FileSystemUploaderServer:
    """
    A class for uploading files from the local file system to a client.

    Args:
        chunk_size (int): The size of data chunks to be sent at a time.

    Attributes:
        _file_buffer_size (int): The size of data chunks to be read from 
        the file at a time.

    Methods:
        get_file_size(path: str) -> int:
            Get the size of a file.

        upload_file(
            sender: socket.socket, addr: tuple[str, int], path: str, name: str,
            verbose: bool, exit_signal: Event
        ):
            Upload a file to a client socket.

    """

    def __init__(self, file_buffer_size: int):
        self._file_buffer_size = file_buffer_size

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
        socketSW,
        socketSR,
        addr: tuple[str, int],
        path: str,
        name: str,
        verbose: bool,
        exit_signal: Event,
        channel: queue.Queue,
    ):
        """
        Upload a file to a client socket.

        Args:
            socketSW: The object responsible for sending data to the client
            using stop-and-wait.
            socketSR: The object responsible for sending data to the client
            using selective repeat.
            addr (tuple[str, int]): The address of the client.
            path (str): The path to the file to be uploaded.
            name (str): The name of the file being uploaded.
            verbose (bool): If True, print verbose information about
            the upload.
            exit_signal (threading.Event): An event signaling whether to
            exit the upload process.
            channel (queue.Queue): A queue for receiving data chunks
            from clients in server.

        Note:
            The upload process continues until either the entire file is sent
            or an exit signal is set.
        """
        # Open the file in binary mode for reading
        with open(path, "rb") as file:
            # Print information about the file being uploaded 
            # if verbose is True
            if verbose:
                print(f"-> Uploading file {name}")

            # Iterate over the file in chunks of size _file_buffer_size
            for chunk in iter(lambda: file.read(self._file_buffer_size), b""):
                # Check if an exit signal is set
                if exit_signal.is_set():
                    if socketSW is not None:
                        # Send the chunk using senderSW (stop-and-wait)
                        socketSW.sendto_with_queue(chunk, addr, channel)
                    else:
                        # Send the chunk using senderSR (selective repeat)
                        socketSR.send_message(chunk)
                    print("Closing server due to signal")
                    break

                if socketSW is not None:
                    # Send the chunk using senderSW (stop-and-wait)
                    socketSW.sendto_with_queue(chunk, addr, channel)
                else:
                    # Send the chunk using senderSR (selective repeat)
                    socketSR.send_message(chunk)
