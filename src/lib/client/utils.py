#!/usr/bin/env python3

import socket
from threading import Event
from src.lib.commands import Command, MessageOption, CommandResponse
from src.lib.constants import BUFFER_SIZE, CHUNK_SIZE, UPLOAD_FINISH_MSG
from src.lib.fs.fs_uploader import FileSystemUploader
from src.lib.fs.fs_downloader import FileSystemDownloader
from src.rdt_stop_and_wait import RdtWSSocket


def verify_params(args, command: str):
    if not args.host or not args.port:
        return False
    if command == "upload" and (not args.src or not args.name):
        return False
    if command == "download" and (not args.dst or not args.name):
        return False
    return True


def connect(args):
    address = (args.host, args.port)

    client_socket = RdtWSSocket()

    # try:
    client_socket.connect(address)
    # except ConnectionRefusedError:
    #     print("Connection refused. Make sure the server is running.")
    #     return None
    # except TimeoutError:
    #     print("Connection timed out. Check the host and port.")
    #     return None
    # except BrokenPipeError:
    #     print("Connection closed. Reconnect and try again.")
    #     return None
    # except Exception as e:  # TODO specify exception and handle it
    #     print(f"4 😨 An exception has occurred, please try again -> {e}😨")
    #     return None

    if args.verbose:
        print(f"✔ Successfully connected to {args.host}:{args.port} ✔")

    return client_socket


def upload_file(socket, path, name, verbose: bool, adr: str):
    fs_handler = FileSystemUploader(CHUNK_SIZE)
    file_size = fs_handler.get_file_size(path)

    # TODO check on server side if another file has the same name, also check if the file doesn't has more than the max size
    command = Command(MessageOption.UPLOAD, name, file_size)
    print(f"before send with addr  : {adr}")
    print(f"About to send  : {command.to_str()}")
    socket.send(command.to_str().encode(), adr,False)
    if verbose:
        print(
            f"-> Sending request to server to upload file {name} with size {file_size} bytes"
        )

    print("La queda aca")
    response = socket.recv().decode()
    print(f"response = {response}")
    command = CommandResponse(response)
    if command.is_error():
        print(f"❌ Request rejected -> {command._msg} ❌")
        return

    if verbose:
        print("✔ Request accepted ✔")

    fs_handler.upload_file(socket, path, name, verbose, False)

    if verbose:
        print(f"✔ File {name} uploaded successfully ✔")

    socket.send(UPLOAD_FINISH_MSG)


def download_file(connection: socket.socket, dest: str, name: str, verbose: bool):
    fs_handler = FileSystemDownloader("./", CHUNK_SIZE)
    if fs_handler.file_exists(filename=name):
        print(f"❌ File {name} already exists ❌")
        return

    with connection:
        command = Command(MessageOption.DOWNLOAD, name, 0)
        connection.send(command.to_str().encode())

        if verbose:
            print(f"-> Sending request to server to download file {name}")

        response = connection.recv(BUFFER_SIZE).decode()
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
            connection.sendall(response.encode())
            return

        response = CommandResponse.ok_response().to_str()
        connection.sendall(response.encode())

        if verbose:
            print(f"-> Downloading file {name} with name {dest}")

        fs_handler.download_file(connection, dest, Event(), size, False)

        if verbose:
            print(f"✔ File {name} downloaded successfully ✔")

        connection.close()
