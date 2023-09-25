from typing import Protocol


class SocketInterface(Protocol):
    def bind(self, addr: tuple[str, int]):
        pass

    def sendto(self, data, addr: tuple[str, int]):
        pass

    def recv(self, bufsize: int):
        pass

    def recvfrom(self, bufsize: int):
        pass

    def close(self):
        pass