from typing import Protocol


class SocketInterface(Protocol):
    """
    A protocol for objects that provide socket-like functionality.

    Methods:
        bind(addr: tuple[str, int]): Bind the socket to a specific address.
        sendto(data, addr: tuple[str, int]): Send data to a specific address.
        recv(bufsize: int) -> bytes: Receive data with a specified buffer size.
        recvfrom(bufsize: int) -> tuple[bytes, tuple[str, int]]: Receive data and the source address.
        close(): Close the socket or release its resources.
    """

    def bind(self, addr: tuple[str, int]):
        """
        Bind the socket to a specific address.

        Args:
            addr (tuple[str, int]): A tuple containing the host address (str) and port number (int).
        """
        pass

    def sendto(self, data, addr: tuple[str, int]):
        """
        Send data to a specific address.

        Args:
            data: The data to be sent.
            addr (tuple[str, int]): A tuple containing the destination host address (str) and port number (int).
        """
        pass

    def recv(self, bufsize: int) -> bytes:
        """
        Receive data with a specified buffer size.

        Args:
            bufsize (int): The maximum number of bytes to receive.

        Returns:
            bytes: The received data as bytes.
        """
        pass

    def recvfrom(self, bufsize: int) -> tuple[bytes, tuple[str, int]]:
        """
        Receive data and the source address.

        Args:
            bufsize (int): The maximum number of bytes to receive.

        Returns:
            tuple[bytes, tuple[str, int]]: A tuple containing the received data as bytes
            and the source address as a tuple (host address, port number).
        """
        pass

    def close(self):
        """
        Close the socket or release its resources.
        """
        pass
