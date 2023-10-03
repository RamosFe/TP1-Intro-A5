class Packet:
    def __init__(self, seq_num, data):
        """
        Initialize a Packet object.

        Args:
            seq_num (int): Sequence number for the packet.
            data (bytes): Data to be carried by the packet.
        """
        self.seq_num = seq_num  # Store the sequence number
        self.data = data  # Store the data payload
        self.timer = None  # Timer for timeout handling
        self.timeouts = 0  # Number of timeouts experienced by the packet

    def into_bytes(self):
        """
        Convert the Packet object into a byte representation.

        Returns:
            bytes: Byte representation of the packet.
        """
        return (
            self.seq_num.to_bytes(4, byteorder="big") + self.data
        )  # Convert seq_num to 4-byte big-endian format
           # and concatenate with data

    @staticmethod
    def from_bytes(bytes):
        """
        Create a Packet object from its byte representation.

        Args:
            bytes (bytes): Byte representation of the packet.

        Returns:
            Packet: The reconstructed Packet object.
        """
        seq_num = int.from_bytes(
            bytes[:4], byteorder="big"
        )  # Extract sequence number from first 4 bytes
        data = bytes[4:]  # Extract data payload from remaining bytes
        return Packet(
            seq_num, data
        )  # Create and return a new Packet object with extracted values

    def is_ack(self):
        """
        Check if the packet is an acknowledgment packet.

        Returns:
            bool: True if the packet is an acknowledgment, False otherwise.
        """
        return self.data == b"ACK"  # Check if data payload is "ACK"

    def get_data(self):
        """
        Get the data payload of the packet.

        Returns:
            bytes: Data payload of the packet.
        """
        return self.data  # Return the data payload

    def get_seqnum(self):
        """
        Get the sequence number of the packet.

        Returns:
            int: Sequence number of the packet.
        """
        return self.seq_num  # Return the sequence number
