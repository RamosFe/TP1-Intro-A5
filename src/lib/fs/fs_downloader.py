import os
import queue
from threading import Event

from lib.constants import UPLOAD_FINISH_MSG, HARDCODED_TIMEOUT


class FileSystemDownloader:
    def __init__(self, mount_path: str, chunk_size: int):
        if not os.path.exists(mount_path):
            os.makedirs(mount_path)
        self._mount_path = mount_path
        self._chunk_size = chunk_size

    def file_exists(self, filename: str) -> bool:
        return os.path.exists(os.path.join(self._mount_path, filename))

    def download_file(self, channel: queue.Queue, path: str, exit_signal: Event):
        with open(os.path.join(self._mount_path, path), "wb") as file:
            try:
                while not exit_signal.is_set():
                    data = channel.get(block=True, timeout=HARDCODED_TIMEOUT)
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
