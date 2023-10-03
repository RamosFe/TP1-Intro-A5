import queue
import socket
import os
from threading import Event

from lib.commands import Command, CommandResponse, MessageOption
from lib.constants import HARCODED_BUFFER_SIZE_FOR_FILE, UPLOAD_FINISH_MSG, HARDCODED_CHUNK_SIZE
from lib.fs.fs_uploader import FileSystemUploaderServer

from lib.handshake import ThreeWayHandShake
from lib.rdt.rdt_sw_socket import RdtSWSocketClient


def upload_file(
    channel: queue.Queue,
    socketSW,
    addr: tuple[str, int],
    socketSR,
    mount_path: str,
    exit_signal: Event,
    comm: Command,
):
    """
    Upload a file to a client socket.

    Args:
        channel (queue.Queue): A queue containing data chunks to be uploaded.
        socket_to_client (socket.socket): The socket used to send data to the client.
        addr (tuple[str, int]): The address of the client.
        mount_path (str): The path to the directory where files will be uploaded.
        exit_signal (threading.Event): An event signaling whether to exit the upload process.
        comm (Command): The command object containing information about the upload.

    Note:
        This function checks if the file exists on the server and whether it's a valid file.
        If the file doesn't exist or is not valid, it sends an error response to the client.
        If the file exists and is valid, it sends an upload request to the client and proceeds with the upload.
    """
# Construct the full path of the file to be uploaded
    path = mount_path + comm.name

    # If using stop-and-wait (socketSW is not None), initialize a ThreeWayHandShake object
    if socketSW is not None:
        three_way_hand_shake = ThreeWayHandShake(socketSW)

    # Check if the file exists and is a valid file
    if not (os.path.exists(path) and os.path.isfile(path)):
        response = CommandResponse.err_response("ERR File not found").to_str()

        # If using stop-and-wait, send an error response with ThreeWayHandShake
        if socketSW is not None:
            three_way_hand_shake.send_with_queue_upload(response, addr, channel)
        else:
            # If using selective repeat, send an error response with socketSR
            socketSR.send_message(response.encode())
        return

    # Initialize a file system handler for uploading
    fs_handler = FileSystemUploaderServer(HARDCODED_CHUNK_SIZE)

    # Get the size of the file to be uploaded
    file_size = fs_handler.get_file_size(path)

    # Create a command object to send to the client
    command = Command(MessageOption.UPLOAD, comm.name, file_size)

    # If using stop-and-wait, send the command with ThreeWayHandShake
    if socketSW is not None:
        try:
            command = CommandResponse(three_way_hand_shake.send_with_queue_upload(command.to_str(), addr, channel).decode())
        except TimeoutError:
            print("❌ Request not answered ❌")
            return
    else:
        # If using selective repeat, send the command with socketSR
        socketSR.send_message(command.to_str().encode())
        response = socketSR.receive_message()
        command = CommandResponse(response.decode())

    # Check if the received command is an error response
    if command.is_error():
        print(f"❌ Request rejected ❌")
        return

    print(f"✔ Request accepted sending file {comm.name} to {addr} ✔")

    try:
        # Start the upload process
        fs_handler.upload_file(socketSW, socketSR, addr, path, comm.name, False, exit_signal, channel)
    except TimeoutError:
        if socketSR is not None:
            socketSR.close_connection()
        print("❌ Connection Timeout Error ❌")
        return

    # Send an upload finish message to signal completion
    if socketSW is not None:
        socketSW.sendto_with_queue(UPLOAD_FINISH_MSG.encode(), addr, channel)
    else:
        socketSR.send_message(UPLOAD_FINISH_MSG.encode())
        socketSR.close_connection()
    return