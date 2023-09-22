import socket
import textwrap
from src.msg_components import (
    SequenceNumber,
    FileContent,
    StopAndWaitMessage,
    StopAndWaitACK,
)
from src.module_counter import ModuleNCounter

MAX_SIZE_OF_SEQUENCE_NUMBER = 1
HARDCODED_MAX_CHUNK_SIZE = 1024


class RdtWSSocket:
    """
    Represents a reliable data transfer over UDP using Stop-and-Wait protocol.

    Args:
        chunk_size (int): Maximum size of data chunks.

    Attributes:
        _internal_socket (socket.socket): The internal UDP socket.
        _max_chunks_size (int): Maximum size of data chunks.
    """

    def __init__(self, chunk_size: int = HARDCODED_MAX_CHUNK_SIZE):
        self._internal_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._max_chunks_size = chunk_size

    def bind(self, ip: str, port: int):
        """
        Bind the internal socket to the specified IP address and port.

        Args:
            ip (str): IP address to bind to.
            port (int): Port number to bind to.
        """
        self._internal_socket.bind((ip, port))

    def connect(self, addr):
        """
        Connect to a remote address.

        Args:
            addr: A tuple containing the remote IP address and port.
        """
        self._internal_socket.connect(addr)

    def accept(self):
        return self._internal_socket.accept()

    def send(self, data: str):
        """
        Send data using the Stop-and-Wait protocol.

        Args:
            data (str): The data to send.
        """
        # Divides the str into strings with the specified chunk size
        chunks = textwrap.wrap(
            data, (self._max_chunks_size - MAX_SIZE_OF_SEQUENCE_NUMBER) // 8
        )
        # Starts the counter
        counter = ModuleNCounter(2)
        for chunk in chunks:
            while True:
                # Create the sequence number for the msg
                sequence_number = SequenceNumber(counter.get_value())
                # Select the file content from the pair for the message based on the counter
                file_content = FileContent(chunk)
                # Creates the message concatenating the bits of the
                # sequence number and the file content
                msg = sequence_number.to_bits() + file_content.to_bits()
                # Sends the msg
                self._internal_socket.send(msg.encode())

                # Waits for the ACK
                response = self._internal_socket.recv(
                    self._max_chunks_size
                )  # TODO ADD TIMEOUT
                # Parses the ACK Response
                ack_response = StopAndWaitACK.from_bits(response.decode())
                if response is None:
                    # TODO HANDLE RESPONSE NONE (Raise error)
                    return "Error"
                # TODO WAIT RESPONSE

                # Checks if it is the expected sequence number and is not corrupted
                if (
                    ack_response.sequence_number.get_value() == counter.get_value()
                    or not ack_response.is_corrupted()
                ):  # TODO; cheqiear si sacamos el .is_corrupted
                    counter.increment()
                    break

    def recv(self):
        """
        Receive data using the Stop-and-Wait protocol.

        Returns:
            list: A list of received data chunks.
        """

        # Creates the sequence number counter
        counter = ModuleNCounter(2)
        # Creates the buffer
        # TODO Buffer limit size ?
        buffer = []

        while True:
            # Wait for a message
            response = self._internal_socket.recv(self._max_chunks_size)

            # If there is no message, the socket is close
            if not response:
                break

            # Parses the message
            message = StopAndWaitMessage.from_bits(response.decode())

            # TODO Validate checksum corruption
            # If it is not corrupted and the sequence number is the expected, process it
            if (
                not message.is_corrupted()
                and message.sequence_number.get_value() == counter.get_value()
            ):
                # Adds the content to the buffer
                buffer.append(
                    str(message.content)
                )  # TODO change to bytes instead of strings....

                # Creates the ACK Response and send it
                ack_response = message.sequence_number.to_bits()
                self._internal_socket.send(ack_response.encode())

                # Increment the sequence number counter
                counter.increment()
            else:
                # Creates the ACK Response with the next sequence number value
                # due to being corrupted or not the expected sequence number
                ack_response = SequenceNumber(
                    (message.sequence_number.get_value() + 1) % 2
                ).to_bits()  #  ? Check if needs to % 2 the number or if rotates by module
                self._internal_socket.send(ack_response.encode())

        return buffer

    def close(self):
        """Close the internal socket."""
        self._internal_socket.close()
