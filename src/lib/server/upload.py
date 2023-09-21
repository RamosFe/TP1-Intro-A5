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

def upload_file(connection: socket.socket, addr: str, max_chunk_size: int, mount_path: str, exit_signal: Event, comm: Command):
    with connection:
        print(f"{addr}: {comm.option.value} file: {comm.name}")
        
        path = mount_path + comm.name
        print(f"path a pasar: {path}")
        fs_handler = FileSystemUploader(CHUNK_SIZE)
        
        if not (os.path.exists(path) and os.path.isfile(path)):
            response = CommandResponse.err_response("ERR File not found")
            connection.send(response.to_str().encode())
            return 

        file_size = fs_handler.get_file_size(path)

        command = Command(MessageOption.UPLOAD, comm.name, file_size)
        connection.send(command.to_str().encode())

        response = connection.recv(BUFFER_SIZE).decode()
        command = CommandResponse(response)

        if command.is_error():
            print(f"❌ Request rejected ❌")
            return

        print(f"✔ Request accepted sending file {comm.name} to {addr} ✔")
        fs_handler.upload_file(connection, path, comm.name, False, True)
        connection.send(UPLOAD_FINISH_MSG)
    return