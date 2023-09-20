import socket
from src.lib.constants import BUFFER_SIZE, CHUNK_SIZE, LIST_FILES_FINISH
from threading import Event

def list_files_client(client_socket,exit_signal : Event):
    client_socket.send('LS'.encode())
    while not exit_signal.isSet():
        data = client_socket.recv(CHUNK_SIZE)
        if data == LIST_FILES_FINISH:
            print('\n')
            break
        print(data.decode(),end='')
    


