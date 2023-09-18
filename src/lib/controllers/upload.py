from src.lib.constants import BUFFER_SIZE, CHUNK_SIZE, UPLOAD_FINISH_MSG
from src.lib.fs.fs_uploader import FileSystemUploader
from src.lib.messages.commands import Command, MessageOption, CommandResponse

#LADO CLIENTEEEE

def upload_file(socket, path, name, verbose: bool, server: bool):
    fs_handler = FileSystemUploader(CHUNK_SIZE)
    file_size = fs_handler.get_file_size(path)

    # TODO check on server side if another file has the same name, also check if the file doesn't has more than the max size
    command = Command(MessageOption.UPLOAD, name, file_size)
    socket.send(command.to_str().encode())
    
    if verbose and not server: # TODO server side
        print(f"Senting request to server to upload file {name} with size {file_size} bytes")

    response = socket.recv(BUFFER_SIZE).decode()
    command = CommandResponse(response)
    if command.is_error():
        print(f"❌ Request rejected -> {command._msg} ❌")
        return
    
    if verbose and not server: # TODO server side
        print("✔ Request accepted ✔")

    fs_handler.upload_file(socket, path, name, verbose, server)
    socket.send(UPLOAD_FINISH_MSG)
