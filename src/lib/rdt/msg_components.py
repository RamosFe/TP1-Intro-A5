SEQUENCENUMBERBITLENGTH = 1

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
    def __init__(self, sq_number: SequenceNumber, content: FileContent):
        self.sequence_number = sq_number
        self.content = content

    @classmethod
    def from_bits(cls, bit_sequence):
        """Creates a StopAndWaitMessage from a binary bit sequence."""
        # Extract the bit sequences for UDPHeader, SequenceNumber, and FileContent
    
        sq_number_bits = bit_sequence[SEQUENCENUMBERBITLENGTH]  # Assuming SequenceNumber is 1 bit
        content_bits = bit_sequence[SEQUENCENUMBERBITLENGTH:]  # Assuming the rest is for FileContent

        # Create instances of UDPHeader, SequenceNumber, and FileContent using from_bits
        sq_number = SequenceNumber.from_bits(sq_number_bits)
        content = FileContent.from_bits(content_bits)

        return cls(sq_number, content)

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
    def __init__(self,sqs_number: SequenceNumber):
        self.sequence_number = sqs_number

    @classmethod
    def from_bits(cls, bit_sequence):
        """Creates a StopAndWaitACK from a binary bit sequence."""
        # Extract the bit sequences for SequenceNumber
        sq_number_bits = bit_sequence[SEQUENCENUMBERBITLENGTH]
        sq_number = SequenceNumber.from_bits(sq_number_bits)
        return cls(sq_number)

    def is_corrupted(self) -> bool:
        """Checks if the acknowledgment is corrupted (always returns False for this example)."""

        # TODO Implementation
        return False
