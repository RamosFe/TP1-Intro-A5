class SequenceNumber:
    """
    Represents a sequence number.

    Args:
        value (int): The value of the sequence number.

    Methods:
        from_bits(bit_sequence): Creates a SequenceNumber from a binary bit sequence.
        to_bits(): Converts the sequence number to a binary bit sequence.
        get_value(): Returns the integer value of the sequence number.
    """
    def __init__(self, value):
        self._value = value

    @classmethod
    def from_bits(cls, bit_sequence):
        """Creates a SequenceNumber from a binary bit sequence."""
        return cls(int(bit_sequence, 2))

    def to_bits(self) -> str:
        """Converts the sequence number to a binary bit sequence."""
        return bin(self._value)[2:]

    def get_value(self) -> int:
        """Returns the integer value of the sequence number."""
        return self._value


class FileContent:
    """
    Represents content as text data.

    Args:
        data (str): The text data.

    Methods:
        from_bits(bit_sequence): Creates FileContent from a binary bit sequence.
        to_bits(): Converts the text data to a binary bit sequence.
    """
    def __init__(self, data):
        self._data = data

    @classmethod
    def from_bits(cls, bit_sequence):
        """Creates FileContent from a binary bit sequence."""
        text_data = int(bit_sequence, 2).to_bytes((len(bit_sequence) + 7) // 8, byteorder='big').decode('utf-8')
        return cls(text_data)

    def to_bits(self) -> str:
        """Converts the text data to a binary bit sequence."""
        byte_data = self._data.encode('utf-8')
        return ''.join(f'{byte:08b}' for byte in byte_data)

    def __str__(self):
        return self._data


class UDPHeader:
    """
    Represents a UDP header.

    Args:
        source_port (int): Source port number.
        destination_port (int): Destination port number.
        length (int): Length of the UDP packet.
        checksum (int): Checksum value.

    Methods:
        from_bits(bit_sequence): Creates a UDPHeader from a binary bit sequence.
        size_in_bits(): Returns the size of the UDPHeader in bits (assuming a fixed size).
    """
    def __init__(self, source_port, destination_port, length, checksum):
        self.source_port = source_port
        self.destination_port = destination_port
        self.length = length
        self.checksum = checksum

    @classmethod
    def from_bits(cls, bit_sequence):
        """Creates a UDPHeader from a binary bit sequence."""
        source_port = int(bit_sequence[0:16], 2)
        destination_port = int(bit_sequence[16:32], 2)
        length = int(bit_sequence[32:48], 2)
        checksum = int(bit_sequence[48:64], 2)
        return cls(source_port, destination_port, length, checksum)

    @staticmethod
    def size_in_bits() -> int:
        """Returns the size of the UDPHeader in bits (assuming a fixed size)."""
        return 64


class StopAndWaitMessage:
    """
    Represents a Stop-and-Wait message.

    Args:
        header (UDPHeader): The UDP header.
        sq_number (SequenceNumber): The sequence number.
        content (FileContent): The content of the message.

    Methods:
        from_bits(bit_sequence): Creates a StopAndWaitMessage from a binary bit sequence.
        is_corrupted(): Checks if the message is corrupted (always returns False for this example).
    """
    def __init__(self, header: UDPHeader, sq_number: SequenceNumber, content: FileContent):
        self.udp_header = header
        self.sequence_number = sq_number
        self.content = content

    @classmethod
    def from_bits(cls, bit_sequence):
        """Creates a StopAndWaitMessage from a binary bit sequence."""
        # Extract the bit sequences for UDPHeader, SequenceNumber, and FileContent
        header_bits = bit_sequence[:64]  # Assuming UDPHeader is 64 bits
        sq_number_bits = bit_sequence[64]  # Assuming SequenceNumber is 1 bit
        content_bits = bit_sequence[65:]  # Assuming the rest is for FileContent

        # Create instances of UDPHeader, SequenceNumber, and FileContent using from_bits
        header = UDPHeader.from_bits(header_bits)
        sq_number = SequenceNumber.from_bits(sq_number_bits)
        content = FileContent.from_bits(content_bits)

        return cls(header, sq_number, content)

    def is_corrupted(self) -> bool:
        """Checks if the message is corrupted (always returns False for this example)."""

        # TODO Implementation
        return False


class StopAndWaitACK:
    """
    Represents a Stop-and-Wait acknowledgment.

    Args:
        header (UDPHeader): The UDP header.
        sq_number (SequenceNumber): The sequence number.

    Methods:
        from_bits(bit_sequence): Creates a StopAndWaitACK from a binary bit sequence.
        is_corrupted(): Checks if the acknowledgment is corrupted (always returns False for this example).
    """
    def __init__(self, header: UDPHeader ,sqs_number: SequenceNumber):
        self.udp_header = header
        self.sequence_number = sqs_number

    @classmethod
    def from_bits(cls, bit_sequence):
        """Creates a StopAndWaitACK from a binary bit sequence."""
        # Extract the bit sequences for UDPHeader and SequenceNumber
        header_bits = bit_sequence[:64]
        sq_number_bits = bit_sequence[64]

        header = UDPHeader.from_bits(header_bits)
        sq_number = SequenceNumber.from_bits(sq_number_bits)

        return cls(header, sq_number)

    def is_corrupted(self) -> bool:
        """Checks if the acknowledgment is corrupted (always returns False for this example)."""

        # TODO Implementation
        return False
