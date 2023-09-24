import queue
import socket
import os
from threading import Event
from lib.commands import Command, CommandResponse, MessageOption
from lib.constants import HARDCODED_CHUNK_SIZE, UPLOAD_FINISH_MSG
from lib.fs.fs_uploader_server import FileSystemUploaderServer


def upload_file(
    channel: queue.Queue,
    socket_to_client: socket.socket,
    addr: tuple[str, int],
    mount_path: str,
    exit_signal: Event,
    comm: Command,
):
    path = mount_path + comm.name
    print(f"El path es {path}")
    if not (os.path.exists(path) and os.path.isfile(path)):
        response = CommandResponse.err_response("ERR File not found").to_str()
        socket_to_client.sendto(response.encode(), addr)
        return

    fs_handler = FileSystemUploaderServer(HARDCODED_CHUNK_SIZE)

    file_size = fs_handler.get_file_size(path)
    command = Command(MessageOption.UPLOAD, comm.name, file_size)
    socket_to_client.sendto(command.to_str().encode(), addr)

    response = channel.get()
    command = CommandResponse(response.decode())

    if command.is_error():
        print(f"❌ Request rejected ❌")
        return

    print(f"✔ Request accepted sending file {comm.name} to {addr} ✔")
    fs_handler.upload_file(socket_to_client, addr, path, comm.name, False, exit_signal)
    socket_to_client.sendto(UPLOAD_FINISH_MSG.encode(), addr)
    return
