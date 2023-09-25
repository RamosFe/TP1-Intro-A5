import socket
import queue
from lib.constants import HARDCODED_BUFFER_SIZE,HARDCODED_CHUNK_SIZE,HARDCODED_HOST,HARDCODED_MOUNT_PATH,HARDCODED_PORT,HARDCODED_TIMEOUT
import math
from lib.rdt.counter import ModuleNCounter
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
        self


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




class RdtSWSocketClient:


    def __init__(self):
        """
        Initializes a new RdtSWSocket object by creating an internal UDP socket.
        """
        self._internal_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

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


        packets_len = math.ceil(len(data) / HARDCODED_CHUNK_SIZE) 
        
        counter = ModuleNCounter(2)
        
        for i in range(packets_len):
            print("--DEBUG-- sending data chunk ",i)
            data_chunk = data[i * HARDCODED_CHUNK_SIZE : (i + 1) * HARDCODED_CHUNK_SIZE] # No puede dar error en python si nos excedemos
            data_chunk = str(counter.get_value()) + data_chunk    
            self._internal_socket.sendto(data_chunk.encode(),addr)
            receive_addr = None
            while True:
                while receive_addr != addr:
                    receive,receive_addr = self._internal_socket.recvfrom(HARDCODED_BUFFER_SIZE)
                    print(f"--DEBUG-- i received {receive.decode()} from addr {receive_addr} when addr {addr} ")
                if receive.decode() != str(counter.get_value()):
                    print(f"--DEBUG-- i received {receive.decode()} and counter {counter.get_value()}")
                    self._internal_socket.sendto(data_chunk.encode(),addr) 
                    continue  

                counter.increment()
                break
            
        print("--DEBUG-- se envio todo")


    def recv(self, bufsize: int) -> bytes:
        """
        Receives data from the socket with the given buffer size.

        Args:
            bufsize (int): The maximum number of bytes to receive.

        Returns:
            bytes: The received data as bytes.
        """
        counter = ModuleNCounter(2)
        while True:
            data,addr = self._internal_socket.recvfrom(bufsize)
            data = data.decode()
            print("--DEBUG-- i RECEIVED" )
            ack = str(counter.get_value())
            message = data[1:]
            self._internal_socket.sendto(ack.encode(), addr)
            counter.increment()
            print(f"Data: {message} ACK: {ack}")

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

