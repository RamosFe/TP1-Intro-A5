import socket
from threading import Event
from src.lib.utils import byte_to_srt
from src.lib.fs.fs_uploader import *
from src.lib.commands import Command, CommandResponse, MessageOption
from src.lib.constants import CHUNK_SIZE, BUFFER_SIZE, UPLOAD_FINISH_MSG


# ESTO ES DEL LADO DEL SERVIDOR POR AHORA
#CLIENTE HACE DOWNLOAD, SERVIDOR HACE UPLOAD 

#CLIENTE:   DOWNLOAD filename
#SERVER:    UPLOAD filename size
#CLIENTE:    OK/ERR
#SERVER:   manda archivo

def upload_file(connection: socket.socket, addr: str, max_chunk_size: int, mount_path: str, exit_signal: Event, comm: Command, verbose: bool):
    with connection:
        if verbose:
            print(f'[{addr[0]}:{addr[1]}] Requested download of {comm.name}')
        
        path = mount_path + comm.name
        fs_handler = FileSystemUploader(CHUNK_SIZE)
        
        if not (os.path.exists(path) and os.path.isfile(path)):
            if verbose:
                print(f'[{addr[0]}:{addr[1]}] File {comm.name} not found, cancelling download ❌')
            response = CommandResponse.err_response("ERR File not found")
            connection.send(response.to_str().encode())
            return 

        file_size = fs_handler.get_file_size(path)

        if verbose:
            print(f'[{addr[0]}:{addr[1]}] Asking client to download {comm.name} ({byte_to_srt(file_size)}) ✔')

        command = Command(MessageOption.UPLOAD, comm.name, file_size)
        connection.send(command.to_str().encode())

        response = connection.recv(BUFFER_SIZE).decode()
        command = CommandResponse(response)

        if verbose and command.is_error():
            print(f"[{addr[0]}:{addr[1]}] Client rejected download of {comm.name} ❌")
            return
        elif verbose:
            print(f"[{addr[0]}:{addr[1]}] Client accepted download of {comm.name} ✔")

        fs_handler.upload_file(connection, path, comm.name, False, True)
        connection.send(UPLOAD_FINISH_MSG)

        if verbose:
            print(f'[{addr[0]}:{addr[1]}] File {comm.name} has been downloaded successfully ✔')
    return