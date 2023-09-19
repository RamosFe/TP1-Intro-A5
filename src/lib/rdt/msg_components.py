class SequenceNumber:
    def __init__(self, value):
        self._value = value

    @classmethod
    def from_bits(cls, bit_sequence):
        return cls(int(bit_sequence, 2))

    def to_bits(self) -> str:
        return bin(self._value)[2:]


class FileContent:
    def __init__(self, data):
        self._data = data

    @classmethod
    def from_bits(cls, bit_sequence):
        text_data = int(bit_sequence, 2).to_bytes((len(bit_sequence) + 7) // 8, byteorder='big').decode('utf-8')
        return cls(text_data)

    def to_bits(self) -> str:
        byte_data = self._data.encode('utf-8')
        return ''.join(f'{byte:08b}' for byte in byte_data)

    def __str__(self):
        return self._data


class UDPHeader:
    def __init__(self, source_port, destination_port, length, checksum):
        self.source_port = source_port
        self.destination_port = destination_port
        self.length = length
        self.checksum = checksum

    @classmethod
    def from_bits(cls, bit_sequence):
        source_port = int(bit_sequence[0:16], 2)
        destination_port = int(bit_sequence[16:32], 2)
        length = int(bit_sequence[32:48], 2)
        checksum = int(bit_sequence[48:64], 2)
        return cls(source_port, destination_port, length, checksum)


class StopAndWaitMessage:
    def __init__(self, header: UDPHeader, sq_number: SequenceNumber, content: FileContent):
        self.udp_header = header
        self.sequence_number = sq_number
        self.content = content

    @classmethod
    def from_bits(cls, bit_sequence):
        # Extract the bit sequences for UDPHeader, SequenceNumber, and FileContent
        header_bits = bit_sequence[:64]  # Assuming UDPHeader is 64 bits
        sq_number_bits = bit_sequence[64]  # Assuming SequenceNumber is 1 bit
        content_bits = bit_sequence[65:]  # Assuming the rest is for FileContent

        # Create instances of UDPHeader, SequenceNumber, and FileContent using from_bits
        header = UDPHeader.from_bits(header_bits)
        sq_number = SequenceNumber.from_bits(sq_number_bits)
        content = FileContent.from_bits(content_bits)

        return cls(header, sq_number, content)
