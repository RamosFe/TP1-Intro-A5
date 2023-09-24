from queue import Queue
import socket
from threading import Event
from src.lib.fs.fs_uploader import *
from src.lib.commands import Command, CommandResponse, MessageOption
from src.lib.constants import CHUNK_SIZE, BUFFER_SIZE, UPLOAD_FINISH_MSG


# ESTO ES DEL LADO DEL SERVIDOR POR AHORA
#CLIENTE HACE DOWNLOAD, SERVIDOR HACE UPLOAD 

#CLIENTE:   DOWNLOAD filename
#SERVER:    UPLOAD filename size
#CLIENTE:    OK/ERR
#SERVER:   manda archivo

def upload_file(channel_from_client: Queue, channel_to_sender: Queue, addr: str, max_chunk_size: int, mount_path: str, exit_signal: Event, comm: Command):
    
    print(f"{addr}: {comm.option.value} file: {comm.name}")
    
    path = mount_path + comm.name
    print(f"path a pasar: {path}")
    fs_handler = FileSystemUploader(CHUNK_SIZE)
    
    if not (os.path.exists(path) and os.path.isfile(path)):
        response = CommandResponse.err_response("ERR File not found")
        channel_to_sender.put((response.to_str().encode(),addr))
        return 

    file_size = fs_handler.get_file_size(path)

    command = Command(MessageOption.UPLOAD, comm.name, file_size)
    channel_to_sender.put((command.to_str().encode(),addr))

    while True:
        if not channel_from_client.empty():
            response = channel_from_client.get()
            command = CommandResponse(response.decode())

            if command.is_error():
                print(f"❌ Request rejected ❌")
                return

            print(f"✔ Request accepted sending file {comm.name} to {addr} ✔")
            fs_handler.upload_file((channel_to_sender,addr), path, comm.name, False, True)
            channel_to_sender.put((UPLOAD_FINISH_MSG,addr))
            return