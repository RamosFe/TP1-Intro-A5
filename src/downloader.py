import os
import socket
from threading import Event

from lib.fs.fs_downloader_client import FileSystemDownloaderClient
from lib.client_lib import parser, utils as parser_utils
from lib.constants import HARDCODED_CHUNK_SIZE, HARDCODED_BUFFER_SIZE
from lib.commands import Command, CommandResponse, MessageOption


def main():
    """
    Entry point of the download client application.

    This function parses command-line arguments, verifies them, and initiates the file download process.

    Returns:
        None
    """
    args = parser.parse_arguments("download")

    if not parser_utils.verify_params(args, "download"):
        print("❌ Error: missing required argument(s) ❌")
        args.print_help()
        return

    if os.path.exists(args.dst) and os.path.isdir(args.dst):
        print(f"❌ Error: {args.dst} is a directory ❌")
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if client_socket is None:
        return

    print(f"💾 📥 Downloading {args.name} from {args.host}:{args.port} to {args.dst}")
    download_file(client_socket, args.dst, args.name, args.verbose, args.host, args.port)

    client_socket.close()
    print("Bye! See you next time 😉")


def download_file(
    connection: socket.socket, dest: str, name: str, verbose: bool, host: str, port: int
):
    """
    Download a file from a server using a UDP socket connection.

    Args:
        connection (socket.socket): The socket connection to the server.
        dest (str): The destination path where the file will be saved.
        name (str): The name of the file to be downloaded.
        verbose (bool): Whether to print verbose output.
        host (str): The hostname or IP address of the server.
        port (int): The port number for the server.

    Returns:
        None
    """
    fs_handler = FileSystemDownloaderClient("./", HARDCODED_CHUNK_SIZE)
    if fs_handler.file_exists(filename=name):
        print(f"❌ File {name} already exists ❌")
        return

    with connection:
        command = Command(MessageOption.DOWNLOAD, name, 0)
        connection.sendto(command.to_str().encode(), (host, port))

        if verbose:
            print(f"-> Sending request to server to download file {name}")

        response = connection.recv(HARDCODED_BUFFER_SIZE).decode()
        command = CommandResponse(response)
        if command.is_error():
            print(f"❌ Request rejected -> {command._msg} ❌")
            return

        if verbose:
            print("✔ Request accepted ✔")

        size = command.size()

        user_input = input(f"Download file {name} with size {size} bytes? [y/n]: ")
        if user_input.lower() not in ("y", "yes"):
            print("❌ Download canceled ❌")
            response = CommandResponse.err_response("ERR Download canceled").to_str()
            connection.sendto(response.encode(), (host, port))
            return

        response = CommandResponse.ok_response().to_str()
        connection.sendto(response.encode(), (host, port))

        if verbose:
            print(f"-> Downloading file {name} with name {dest}")

        fs_handler.download_file(connection, dest, size, Event())

        if verbose:
            print(f"✔ File {name} downloaded successfully ✔")

        connection.close()


if __name__ == "__main__":
    main()
