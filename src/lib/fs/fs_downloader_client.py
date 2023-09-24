import os
import socket
import math
import queue

from lib.constants import HARDCODED_BUFFER_SIZE, UPLOAD_FINISH_MSG
from threading import Event
from alive_progress import alive_bar


class FileSystemDownloaderClient:
    def __init__(self, mount_path: str, chunk_size: int):
        if not os.path.exists(mount_path):
            os.makedirs(mount_path)
        self._mount_path = mount_path
        self._chunk_size = chunk_size

    def file_exists(self, filename: str) -> bool:
        return os.path.exists(os.path.join(self._mount_path, filename))

    def download_file(
        self, socket: socket.socket, path: str, size: int, exit_signal: Event
    ):
        steps = math.ceil(size / self._chunk_size)
        with alive_bar(steps, bar="bubbles", title=f"↓ {path}") as bar:
            with open(os.path.join(self._mount_path, path), "wb") as file:
                try:
                    while not exit_signal.isSet():
                        data = socket.recv(HARDCODED_BUFFER_SIZE)
                        bar()

                        if UPLOAD_FINISH_MSG in data.decode():
                            file.write(data[: data.decode().index(UPLOAD_FINISH_MSG)])
                            break

                        file.write(data)
                except queue.Empty as e:
                    if exit_signal.is_set():
                        print("Closing server due to signal")
                        return
                    else:
                        raise e

            bar.text("✔ Done ✔")
