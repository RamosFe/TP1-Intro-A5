from src.lib.constants import BUFFER_SIZE, CHUNK_SIZE
from src.lib.fs_handler import FileSystemUploader

def upload_file(socket, path, name):
    fs_handler = FileSystemUploader(CHUNK_SIZE)
    file_size = fs_handler.get_file_size(path)

    socket.send(
        f'UPLOAD {name} {file_size}'.encode())  # TODO check on server side if another file has the same name, also check if the file doesn't has more than the max size
    print(f'Uploading {name} ({file_size} bytes)')

    response = socket.recv(BUFFER_SIZE).decode()
    if response != 'OK':
        print(f'Error: {response}')
        return
    print('Server ready to receive file')

    fs_handler.upload_file(socket, path)
    socket.send(b'UPLOAD EOF')
    print('EOF sent')
