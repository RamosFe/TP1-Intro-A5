import os
import socket
from threading import Event
from alive_progress import alive_bar
from math import ceil
from src.rdt_stop_and_wait import RdtWSSocket
from src.lib.constants import UPLOAD_FINISH_MSG
from queue import Queue


class FileSystemDownloader:
    def __init__(self, mount_path: str, chunk_size: int):
        if not os.path.exists(mount_path):
            os.makedirs(mount_path)
        self._mount_path = mount_path
        self._chunk_size = chunk_size

    def file_exists(self, filename: str) -> bool:
        return os.path.exists(os.path.join(self._mount_path, filename))

    # receiver si es server va a ser un channel, si es el cliente va a ser el socket nuestro
    def download_file(
        self, receiver, path: str, exit_signal: Event, size: int, server: bool
    ):
        if server:
            self._download_file_server(receiver, path, exit_signal)
        else:
            self._download_file_client(
                receiver, path, exit_signal, size
            )  # aca el receiver es el socket a enviar

    def _download_file_server(
        self, channel_from_client: Queue, path: str, exit_signal: Event
    ):
        print(f"ctrl+f 123456 Downloading {path}...")
        with open(os.path.join(self._mount_path, path), "wb") as file:
            while not exit_signal.isSet():
                data = channel_from_client.get()

                if UPLOAD_FINISH_MSG in data:
                    file.write(data[: data.index(UPLOAD_FINISH_MSG)])
                    break

                file.write(data)

    def _download_file_client(
        self, socket: RdtWSSocket, path: str, exit_signal: Event, size: int
    ):
        steps = ceil(size / self._chunk_size)
        with alive_bar(steps, bar="bubbles", title=f"↓ {path}") as bar:
            with open(os.path.join(self._mount_path, path), "wb") as file:
                while not exit_signal.isSet():
                    data = socket.recv()
                    bar()

                    if UPLOAD_FINISH_MSG in data:
                        file.write(data[: data.index(UPLOAD_FINISH_MSG)])
                        break

                    file.write(data)

            bar.text("✔ Done ✔")
