import queue
import socket
from typing import List, Dict, Tuple
from threading import Event
from lib.commands import Command, CommandResponse
from lib.constants import HARDCODED_CHUNK_SIZE
from lib.fs.fs_downloader import FileSystemDownloader


def download_file(
    channel: queue.Queue,
    socket_to_client: socket.socket,
    addr: tuple[str, int],
    mount_path: str,
    exit_signal: Event,
    comm: Command,
):
    fs_handler = FileSystemDownloader(mount_path, HARDCODED_CHUNK_SIZE)
    if fs_handler.file_exists(filename=comm.name):
        response = CommandResponse.err_response(
            f"ERR file {comm.name} already exists"
        ).to_str()
        socket_to_client.sendto(response.encode(), addr)
    else:
        response = CommandResponse.ok_response().to_str()
        socket_to_client.sendto(response.encode(), addr)
        fs_handler.download_file(channel, comm.name, exit_signal)
