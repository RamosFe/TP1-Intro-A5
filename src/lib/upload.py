from src.lib.constants import BUFFER_SIZE, CHUNK_SIZE, UPLOAD_FINISH_MSG
from src.lib.fs_handler import FileSystemUploader
from src.lib.command_parser import Command, ClientOption, CommandResponse


def upload_file(socket, path, name):
    fs_handler = FileSystemUploader(CHUNK_SIZE)
    file_size = fs_handler.get_file_size(path)

    # TODO check on server side if another file has the same name, also check if the file doesn't has more than the max size
    command = Command(ClientOption.UPLOAD, name, file_size)
    socket.send(command.to_str().encode())
    print(f'Uploading {name} ({file_size} bytes)')

    response = socket.recv(BUFFER_SIZE).decode()
    command = CommandResponse(response)
    if command.is_error():
        print(f'Error: {command.to_str()}')
        return
    print('Server ready to receive file')

    fs_handler.upload_file(socket, path)
    socket.send(UPLOAD_FINISH_MSG)
    print('EOF sent')
