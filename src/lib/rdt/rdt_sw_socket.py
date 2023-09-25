import socket


class RdtSWSocket:
    def __init__(self):
        self._internal_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def bind(self, addr: tuple[str, int]):
        self._internal_socket.bind(addr)

    def sendto(self, data, addr: tuple[str, int]):
        self._internal_socket.sendto(data, addr)

    def recv(self, bufsize: int):
        return self._internal_socket.recv(bufsize)

    def recvfrom(self, bufsize: int):
        return self._internal_socket.recvfrom(bufsize)

    def close(self):
        self._internal_socket.close()
