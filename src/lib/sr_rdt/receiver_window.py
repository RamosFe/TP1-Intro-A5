from collections import *


class ReceiverWindow:
    # Class-level variables to keep track of window, base sequence number, 
    # window size, and received packets
    window = None
    base_seq = None
    window_size = None
    received = None

    def __init__(self, window_size):
        """
        Initialize the ReceiverWindow object.

        Args:
            window_size (int): Size of the receiver window.
        """
        # Initialize window as an ordered dictionary (to maintain packet order)
        self.window = OrderedDict()
        self.window_size = window_size  # Set the window size
        self.base_seq = 1  # Initialize base sequence number to 1

    def add_packet(self, packet) -> bool:
        """
        Add a packet to the receiver window.

        Args:
            packet (Packet): The packet to be added.

        Returns:
            bool: True if the packet is successfully added, False otherwise.
        """
        # Check if the packet's sequence number is within the window range
        if self.window_size + self.base_seq < packet.seq_num:
            return False

        # Add the packet to the window
        self.window[packet.seq_num] = packet
        return True

    def get_ordered_packets(self) -> list:
        """
        Get a list of packets in order of their sequence numbers.

        Returns:
            list: List of packets in order.
        """
        packets = []

        # Iterate until the base sequence number is in the window
        while self.base_seq in self.window:
            packet = self.window[self.base_seq]
            packets.append(packet)  # Append packet to the list
            del self.window[self.base_seq]  # Remove packet from window
            self.base_seq += 1  # Update base sequence number
        return packets

    def already_received(self, seq_num) -> bool:
        """
        Check if a packet with a given sequence number has already been received.

        Args:
            seq_num (int): The sequence number to check.

        Returns:
            bool: True if the packet has already been received, False otherwise.
        """
        return seq_num < self.base_seq or seq_num in self.window
