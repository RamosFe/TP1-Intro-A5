import socket

class RdtSWSocket:
    """
    A simple Reliable Data Transfer (RDT) socket using a Stop-and-Wait (SW) approach over UDP.
    This class encapsulates a basic UDP socket and provides methods for sending and receiving data.

    Attributes:
        _internal_socket (socket.socket): The internal UDP socket used for communication.

    Methods:
        __init__(): Initializes the RdtSWSocket object and creates an internal UDP socket.
        bind(addr: tuple[str, int]): Binds the internal socket to the specified address and port.
        sendto(data, addr: tuple[str, int]): Sends data to the specified address.
        recv(bufsize: int) -> bytes: Receives data from the socket with the given buffer size.
        recvfrom(bufsize: int) -> tuple[bytes, tuple[str, int]]: Receives data and the source address.
        close(): Closes the internal socket.

    Note:
        This implementation is basic and lacks error handling for various network issues.
    """

    def __init__(self):
        """
        Initializes a new RdtSWSocket object by creating an internal UDP socket.
        """
        self._internal_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def bind(self, addr: tuple[str, int]):
        """
        Binds the internal socket to the specified address and port.

        Args:
            addr (tuple[str, int]): A tuple containing the host address (str) and port number (int).
        """
        self._internal_socket.bind(addr)

    def sendto(self, data, addr: tuple[str, int]):
        """
        Sends data to the specified address using the internal socket.

        Args:
            data: The data to be sent.
            addr (tuple[str, int]): A tuple containing the destination host address (str) and port number (int).
        """
        self._internal_socket.sendto(data, addr)

    def recv(self, bufsize: int) -> bytes:
        """
        Receives data from the socket with the given buffer size.

        Args:
            bufsize (int): The maximum number of bytes to receive.

        Returns:
            bytes: The received data as bytes.
        """
        return self._internal_socket.recv(bufsize)

    def recvfrom(self, bufsize: int) -> tuple[bytes, tuple[str, int]]:
        """
        Receives data and the source address from the socket.

        Args:
            bufsize (int): The maximum number of bytes to receive.

        Returns:
            tuple[bytes, tuple[str, int]]: A tuple containing the received data as bytes
            and the source address as a tuple (host address, port number).
        """
        return self._internal_socket.recvfrom(bufsize)

    def close(self):
        """
        Closes the internal socket.
        """
        self._internal_socket.close()
