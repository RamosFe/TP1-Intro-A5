import queue
import socket
import math
import time
from lib.constants import (
    HARDCODED_BUFFER_SIZE,
    HARDCODED_CHUNK_SIZE,
    HARDCODED_HOST,
    HARDCODED_PORT,
    HARDCODED_TIMEOUT_SW,
    HARDCODED_MAX_TIMEOUT_TRIES,
)
from lib.rdt.counter import ModuleNCounter


class RdtSWSocket:
    """
    A simple Reliable Data Transfer (RDT) socket using a
    Stop-and-Wait (SW) approach over UDP.
    This class encapsulates a basic UDP socket and provides
    methods for sending and receiving data.

    Attributes:
        _internal_socket (socket.socket): The internal
        UDP socket used for communication.

    Methods:
        __init__(): Initializes the RdtSWSocket object and
        creates an internal UDP socket.
        bind(addr: tuple[str, int]): Binds the internal
        socket to the specified address and port.
        sendto(data, addr: tuple[str, int]): Sends data
        to the specified address.
        recv(bufsize: int) -> bytes: Receives data from the
        socket with the given buffer size.
        recvfrom(bufsize: int) -> tuple[bytes, tuple[str, int]]: Receives
        data and the source address.
        close(): Closes the internal socket.

    Note:
        This implementation is basic and lacks error handling
        for various network issues.
    """

    def __init__(self):
        """
        Initializes a new RdtSWSocket object by 
        creating an internal UDP socket.
        """
        self._internal_socket = socket.socket(socket.AF_INET,
                                              socket.SOCK_DGRAM)

    def bind(self, addr: tuple[str, int]):
        """
        Binds the internal socket to the specified address and port.

        Args:
            addr (tuple[str, int]): A tuple containing the host address (str)
            and port number (int).
        """
        self._internal_socket.bind(addr)

    def sendto(self, data, addr: tuple[str, int]):
        """
        Sends data to the specified address using the internal socket.

        Args:
            data: The data to be sent.
            addr (tuple[str, int]): A tuple containing the destination host
            address (str) and port number (int).
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
            tuple[bytes, tuple[str, int]]: A tuple containing the
            received data as bytes
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
        Initializes a new RdtSWSocket object by
        creating an internal UDP socket.
        """
        self.counter = ModuleNCounter(2)
        self._internal_socket = socket.socket(socket.AF_INET, 
                                              socket.SOCK_DGRAM)

    def bind(self, addr: tuple[str, int]):
        """
        Binds the internal socket to the specified address and port.

        Args:
            addr (tuple[str, int]): A tuple containing the host address
            (str) and port number (int).
        """
        self._internal_socket.bind(addr)

    def sendto(self, data, addr: tuple[str, int]):
        """
        Sends data to the specified address using the internal socket.

        Args:
            data: The data to be sent.
            addr (tuple[str, int]): A tuple containing the destination host
            address (str) and port number (int).
        """

        # Obtengo la cantidad de chunks en el paquete
        packets_len = math.ceil(len(data) / HARDCODED_CHUNK_SIZE)

        # Seteo timeout del socket
        self._internal_socket.settimeout(HARDCODED_TIMEOUT_SW)

        # Por cada chunk
        try:
            for i in range(packets_len):
                # Obtengo el chunk
                chunk = data[
                    i * HARDCODED_CHUNK_SIZE: (i + 1) * HARDCODED_CHUNK_SIZE
                ]  # No puede dar error en python si nos excedemos

                # Parseo el paquete
                data_packet = RDTStopWaitPacket(
                    self.counter.get_value(), chunk
                )  # Al generar el paquete, lo generamos en bytes
                # Envio el paquete a la dirección
                self._internal_socket.sendto(data_packet.to_send(), addr)

                # Espero el ACK
                self._recv_ack(addr, data_packet)

        except TimeoutError:
            raise TimeoutError

    def _recv_ack(self, addr: tuple[str, int], data_packet):
        # Addr del propietario del mensaje recibido
        receive_addr = None
        # Timeout para RDT en caso de desconexion
        time_out_errors = TimeOutErrors()

        while not time_out_errors.max_tries_exceeded():
            try:
                receive, receive_addr = self._internal_socket.recvfrom(
                    HARDCODED_BUFFER_SIZE
                )

                # Caso que el sequence number es distinto al esperado
                ack_receive = AckSequenceNumer.from_bytes(receive)
                if ack_receive.ack != self.counter.get_value():
                    continue

                # Si, el sequence number es el que esperabamos, incremento y 
                # sigo con mi vida
                self.counter.increment()
                break
            except TimeoutError:
                if time_out_errors.max_tries_exceeded():
                    raise TimeoutError
                time_out_errors.increase_try()
                self._internal_socket.sendto(data_packet.to_send(), addr)

        if time_out_errors.max_tries_exceeded():
            raise TimeoutError

    def sendto_with_queue(self, data, addr: tuple[str, int], channel: queue.Queue):
        # Obtengo la cantidad de chunks en el paquete
        packets_len = math.ceil(len(data) / HARDCODED_CHUNK_SIZE)
        # Inicializo el counter usado para el sequence number

        # Por cada chunk
        try:
            for i in range(packets_len):
                # Obtengo el chunk
                chunk = data[
                    i * HARDCODED_CHUNK_SIZE: (i + 1) * HARDCODED_CHUNK_SIZE
                ]  # No puede dar error en python si nos excedemos

                # Parseo el paquete
                data_packet = RDTStopWaitPacket(
                    self.counter.get_value(), chunk
                )  # Al generar el paquete, lo generamos en bytes
                # Envio el paquete a la dirección
                self._internal_socket.sendto(data_packet.to_send(), addr)

                # Espero el ACK

                self._recv_ack_with_queue(addr, data_packet, channel=channel)

        except TimeoutError:
            raise TimeoutError

    def _recv_ack_with_queue(
        self, addr: tuple[str, int], data_packet, channel: queue.Queue
    ):
        # Addr del propietario del mensaje recibido
        receive_addr = None
        # Timeout para RDT en caso de desconexion
        time_out_errors = TimeOutErrors()

        # Mientras no pase el numero de intentos para mandar el paquete 
        # definido por el HARDCODED_MAX_TIMEOUT_PACKET, labura
        while not time_out_errors.max_tries_exceeded():
            try:
                receive, receive_addr = channel.get(
                    block=True, timeout=HARDCODED_TIMEOUT_SW
                )
                # Caso que el sequence number es distinto al esperado
                ack_receive = AckSequenceNumer.from_bytes(receive)
                if ack_receive.ack != self.counter.get_value():
                    continue

                # Si, el sequence number es el que esperabamos, 
                # incremento y sigo con mi vida
                self.counter.increment()
                break

            except queue.Empty:

                if time_out_errors.max_tries_exceeded():
                    raise TimeoutError
                time_out_errors.increase_try()
                self._internal_socket.sendto(data_packet.to_send(), addr)

        if time_out_errors.max_tries_exceeded():
            raise TimeoutError

    def recv(self, bufsize: int, data=None, addr=None):
        """
        Receives data from the socket with the given buffer size.

        Args:
            bufsize (int): The maximum number of bytes to receive.

        Returns:
            bytes: The received data as bytes.
        """
        self._internal_socket.settimeout(None)
        if addr is None:
            data, addr = self._internal_socket.recvfrom(bufsize)
        self.addr = addr
        packet = RDTStopWaitPacket.from_bytes(data)
        self._internal_socket.sendto(
            packet.encode_ack(packet.ack), (HARDCODED_HOST, HARDCODED_PORT)
        )  # TODO poner bonito lo del HARDCODED

        if self.counter.get_value() == packet.ack:
            self.counter.increment()
            return packet.data

    def recv_with_queue(self, channel: queue.Queue):
        data, addr = channel.get(block=True)
        self.addr = addr
        packet = RDTStopWaitPacket.from_bytes(data)
        self._internal_socket.sendto(packet.encode_ack(packet.ack), addr)

        if self.counter.get_value() == packet.ack:
            self.counter.increment()
            return packet.data

    def recvfrom(self, bufsize: int) -> tuple[bytes, tuple[str, int]]:
        """
        Receives data and the source address from the socket.

        Args:
            bufsize (int): The maximum number of bytes to receive.

        Returns:
            tuple[bytes, tuple[str, int]]: A tuple containing the received 
            data as bytes
            and the source address as a tuple (host address, port number).
        """
        return self.recv(bufsize), self.addr

    def recvfrom_with_queue(
        self, channel: queue.Queue
    ) -> tuple[bytes, tuple[str, int]]:
        """
        Receives data and the source address from the socket.

        Args:
            bufsize (int): The maximum number of bytes to receive.

        Returns:
            tuple[bytes, tuple[str, int]]: A tuple containing the received data as bytes
            and the source address as a tuple (host address, port number).
        """
        return self.recv_with_queue(channel), self.addr

    def send_with_internal_socket(self, data, addr):
        self._internal_socket.sendto(data, addr)

    def recv_with_internal_socket(self, bufsize):
        return self._internal_socket.recvfrom(bufsize)

    def set_timeout(self, timeout):
        self._internal_socket.settimeout(timeout)

    def close(self):
        """
        Closes the internal socket.
        """
        self._internal_socket.close()


class TimeOutErrors:
    def __init__(self):
        self.tries = 0

    def increase_try(self):
        self.tries += 1

    def reset_tries(self):
        self.tries = 0

    def get_tries(self):
        return self.tries

    def max_tries_exceeded(self):

        return self.tries > HARDCODED_MAX_TIMEOUT_TRIES

    def get_timeout(self):
        return HARDCODED_TIMEOUT_SW

    def time_to_receive_data(self):
        start_time = time.time()
        end_time = start_time + HARDCODED_TIMEOUT_SW
        return time.time() < end_time


class RDTStopWaitPacket:
    def __init__(self, ack: int, data):

        self.data = self._to_bytes(data)
        self._ack = AckSequenceNumer(ack)

    @classmethod
    def from_bytes(cls, data: bytes):
        ack = data[0]
        message = data[1:]
        return cls(ack, message)

    def _to_bytes(self, data):
        if not type(data) == bytes:
            data = data.encode()
        return data

    def to_send(self):
        return self._ack.encode() + self.data

    def encode_ack(self, ack: int):
        return AckSequenceNumer(ack).encode()

    @property
    def ack(self):
        return self._ack.ack

    @ack.setter
    def ack(self, ack):
        self._ack = AckSequenceNumer(ack)


class AckSequenceNumer:
    def __init__(self, ack: int):
        self.ack = ack

    def encode(self):
        return self.ack.to_bytes(1, byteorder="big")

    @classmethod
    def from_bytes(cls, data):
        ack = data[0]
        return cls(ack)
