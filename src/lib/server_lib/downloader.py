import queue
import socket
from threading import Event

from lib.commands import Command, CommandResponse
from lib.constants import HARDCODED_CHUNK_SIZE
from lib.fs.fs_downloader import FileSystemDownloaderServer
from lib.handshake import ThreeWayHandShake
from lib.rdt.rdt_sw_socket import RdtSWSocketClient


def download_file(
    channel: queue.Queue,
    socket_to_client: RdtSWSocketClient,
    addr: tuple[str, int],
    mount_path: str,
    exit_signal: Event,
    comm: Command,
):
    """
    Download a file from a channel and save it to the local file system.

    Args:
        channel (queue.Queue): A queue containing data chunks to be downloaded.
        socket_to_client (socket.socket): The socket to send responses to the client.
        addr (tuple[str, int]): The address of the client.
        mount_path (str): The path to the directory where files will be downloaded.
        exit_signal (threading.Event): An event signaling whether to exit the download process.
        comm (Command): The command object containing information about the download.

    Note:
        This function sends responses to the client indicating whether the download can proceed or not.
        If the file already exists in the download directory, it sends an error response.
        If the file does not exist, it sends an OK response and proceeds with the download.
    """
    fs_handler = FileSystemDownloaderServer(mount_path, HARDCODED_CHUNK_SIZE)
    three_way_handshake = ThreeWayHandShake(socket_to_client)
    try:
        if fs_handler.file_exists(filename=comm.name):
            response = CommandResponse.err_response(
                f"ERR file {comm.name} already exists"
            ).to_str()
            three_way_handshake.send_with_queue(response, addr,channel)
        else:
            response = CommandResponse.ok_response().to_str()
            three_way_handshake.send_with_queue(response, addr,channel)
            fs_handler.download_file(channel,socket_to_client, comm.name, exit_signal)
    except TimeoutError:
        print(" --FEBUG-- Yo soy el timeout y ordeno que Tomi y Cami Ayala salgan a tomar una birra")
        return

