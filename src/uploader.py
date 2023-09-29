import os
import socket
from typing import Tuple

from lib.commands import Command, MessageOption, CommandResponse
from lib.fs.fs_uploader_client import FileSystemUploaderClient
from lib.client_lib import utils as parser_utils
from lib.client_lib import parser
from lib.constants import HARDCODED_BUFFER_SIZE, HARDCODED_CHUNK_SIZE, UPLOAD_FINISH_MSG, HARCODED_BUFFER_SIZE_FOR_FILE
from lib.rdt.rdt_sw_socket import RdtSWSocketClient
from lib.rdt.rdt_sw_socket import RdtSWSocket


def main(name: str, path: str, addr: Tuple[str, int], verbose: bool):
    """
    Main function to upload a file to a server.

    Args:
        name (str): The name of the file to be uploaded.
        path (str): The path to the file on the local system.
        addr (Tuple[str, int]): A tuple containing the server's address (hostname or IP) and port.
        verbose (bool): Whether to print verbose output.

    Returns:
        None
    """
    # Creates the upload handler
    fs_handler = FileSystemUploaderClient(HARCODED_BUFFER_SIZE_FOR_FILE)
    # Get the file size
    file_size = fs_handler.get_file_size(path=path)

    # Creates the client socket
    client_socket = RdtSWSocketClient()

    # Creates the upload command and sends it
    command = Command(MessageOption.UPLOAD, name, file_size)
    client_socket._internal_socket.sendto(command.to_str().encode(), addr)

    # Log the command if verbose
    if verbose:
        print(
            f"-> Sending request to server to upload file {name} with size {file_size} bytes"
        )

    # Wait for server response and check the type of response
    response = client_socket._internal_socket.recv(HARDCODED_BUFFER_SIZE).decode()
    print("-> Server response: ", response)
    response_command = CommandResponse(response)
    # If error, return
    if response_command.is_error():
        print(f"❌ Request rejected -> {response_command._msg} ❌")
        return

    if verbose:
        print("✔ Request accepted ✔")

    # Else, send the file using the uploader
    try:
        fs_handler.upload_file(client_socket, addr, path, name, verbose)
    except TimeoutError:
        print("❌ Error: Connecction error, maximun times tried ❌")
        return

    if verbose:
        print(f"✔ File {name} uploaded successfully ✔")

    try:
        client_socket.sendto(UPLOAD_FINISH_MSG.encode(), addr)
    except TimeoutError:
        print("❌ Error: server did not respond to upload finish message ❌")


if __name__ == "__main__":
    args = parser.parse_arguments("upload")
    if not parser_utils.verify_params(args, "upload"):
        print("❌ Error: missing required argument(s) ❌")
        args.print_help()
    elif not (os.path.exists(args.src) and os.path.isfile(args.src)):
        print(f"❌ Error: file {args.src} does not exist ❌")
    else:
        main(args.name, args.src, (args.host, args.port), args.verbose)
