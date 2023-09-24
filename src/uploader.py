import os
import socket
from typing import Tuple

from lib.commands import Command, MessageOption, CommandResponse
from lib.fs.fs_uploader import FileSystemUploader
from lib.client import parser as ps
from lib.constants import HARDCODED_BUFFER_SIZE, HARDCODED_CHUNK_SIZE, UPLOAD_FINISH_MSG


def main(name: str, path: str, addr: Tuple[str, int], verbose: bool):
    # Creates the upload handler
    fs_handler = FileSystemUploader(HARDCODED_CHUNK_SIZE)
    # Get the file size
    file_size = fs_handler.get_file_size(path=path)

    # Creates the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Creates the upload command and sends it
    command = Command(MessageOption.UPLOAD, name, file_size)
    client_socket.sendto(command.to_str().encode(), addr)

    # Log the command if verbose
    if verbose:
        print(
            f"-> Sending request to server to upload file {name} with size {file_size} bytes"
        )

    # Wait for server response and check the type of response
    response = client_socket.recv(HARDCODED_BUFFER_SIZE).decode()
    response_command = CommandResponse(response)

    # If error, return
    if response_command.is_error():
        print(f"❌ Request rejected -> {response_command._msg} ❌")
        return

    if verbose:
        print("✔ Request accepted ✔")

    # Else, send the file using the uploader
    fs_handler.upload_file(client_socket, addr, path, name, verbose)
    if verbose:
        print(f"✔ File {name} uploaded successfully ✔")

    client_socket.sendto(UPLOAD_FINISH_MSG.encode(), addr)


if __name__ == "__main__":
    args = ps.parse_arguments("upload")
    if not ps.verify_params(args, "upload"):
        print("❌ Error: missing required argument(s) ❌")
        args.print_help()
    elif not (os.path.exists(args.src) and os.path.isfile(args.src)):
        print(f"❌ Error: file {args.src} does not exists ❌")
    else:
        main(args.name, args.src, (args.host, args.port), args.verbose)
