import socket


class RdtWSSocket:
    def __init__(self):
        self._internal_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def bind(self, ip: str, port: int):
        self._internal_socket.bind((ip, port))

    def connect(self, addr):
        self._internal_socket.connect(addr)

    def send(self, data):
        pass

    def close(self):
        self._internal_socket.close()
