import queue
import socket
import os
from threading import Event

from lib.commands import Command, CommandResponse, MessageOption
from lib.constants import HARCODED_BUFFER_SIZE_FOR_FILE, UPLOAD_FINISH_MSG
from lib.fs.fs_uploader import FileSystemUploaderServer
from lib.handshake import ThreeWayHandShake
from lib.rdt.rdt_sw_socket import RdtSWSocketClient


def upload_file(
    channel: queue.Queue,
    socket_to_client: RdtSWSocketClient,
    addr: tuple[str, int],
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
    path = mount_path + comm.name
    three_way_hand_shake = ThreeWayHandShake(socket_to_client)
    if not (os.path.exists(path) and os.path.isfile(path)):
        response = CommandResponse.err_response("ERR File not found").to_str()

        three_way_hand_shake.send_with_queue_upload(response,addr,channel) # TODO CON ERROR
        # socket_to_client._internal_socket.sendto(response.encode(), addr)
        return

    fs_handler = FileSystemUploaderServer(HARCODED_BUFFER_SIZE_FOR_FILE)

    file_size = fs_handler.get_file_size(path)
    command = Command(MessageOption.UPLOAD, comm.name, file_size)

    try:
        command = CommandResponse(three_way_hand_shake.send_with_queue_upload(command.to_str(),addr,channel).decode())
    
    except TimeoutError:
        print("❌ Request not answered ❌")
        return

    # socket_to_client._internal_socket.sendto(command.to_str().encode(), addr)

    # response = channel.get()
    # command = CommandResponse(response[0].decode())

    if command.is_error():
        print(f"❌ Request rejected ❌")
        return

    print(f"✔ Request accepted sending file {comm.name} to {addr} ✔")
    fs_handler.upload_file(socket_to_client, addr, path, comm.name, False, exit_signal,channel)
    socket_to_client.sendto_with_queue(UPLOAD_FINISH_MSG.encode(), addr,channel)
    return
