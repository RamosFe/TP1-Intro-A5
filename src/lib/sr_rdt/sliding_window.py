import threading
from lib.constants import HARDCODED_MAX_TIMEOUT_TRIES, HARDCODED_TIMEOUT


class SlidingWindow:
    def __init__(self, window_size, socket, addr, stop_event):
        """
        Initialize the SlidingWindow object.

        Args:
            window_size (int): Size of the sliding window.
            socket (socket.socket): The socket used for communication.
            addr (tuple): The address of the sender/receiver.
            stop_event (threading.Event): Event to signal stopping the process.
        """
        self.window_size = window_size  # Set the window size
        self.buffer = []  # Initialize a buffer to store packets
        self.base_seq_num = 1  # Initialize the base sequence number
        self.socket = socket  # Store the socket
        self.addr = addr  # Store the address
        self.stop_event = stop_event  # Store the stop event

    def add_packet(self, packet):
        """
        Add a packet to the buffer if there is space in the window.

        Args:
            packet: The packet to add.

        Returns:
            bool: True if the packet was added, False otherwise.
        """
        # If there is space in the window
        if len(self.buffer) < self.window_size:
            # Create a timer for the packet
            packet.timer = threading.Timer(HARDCODED_TIMEOUT, self.timeout, [packet])
            packet.timer.start()
            # Add the packet to the buffer
            self.buffer.append(packet)
            
            return True
        
        return False

    def get_packet(self, seq_num):
        """
        Get a packet with a specific sequence number from the buffer.

        Args:
            seq_num (int): The sequence number of the desired packet.

        Returns:
            Packet or None: The packet with the specified sequence number, or None if not found.
        """
        for packet in self.buffer:
            if packet.seq_num == seq_num:
                return packet
        return None

    def timeout(self, packet):
        """
        Handle timeout event for a packet.

        Args:
            packet: The packet for which the timeout occurred.
        """
        if self.base_seq_num <= packet.seq_num < self.base_seq_num + self.window_size:
            if packet.timeouts >= HARDCODED_MAX_TIMEOUT_TRIES:
                self.stop_event.set()
            else:
                self.socket.sendto(packet.into_bytes(), self.addr)
                packet.timer = threading.Timer(HARDCODED_TIMEOUT, self.timeout, [packet])
                packet.timer.start()
                packet.timeouts += 1

    def receive_ack(self, ack_num):
        """
        Handle receiving an acknowledgment.

        Args:
            ack_num (int): The sequence number of the acknowledgment.
        """
        # Validate that it's within the window range
        if self.base_seq_num <= ack_num < self.base_seq_num + self.window_size:
            packet = self.get_packet(ack_num)

            # If the packet does not exist, return
            if not packet:
                return
            
            # If the packet has a timer, cancel it
            if packet.timer != None:
                packet.timer.cancel()
            
            packet.timer = None

            # If it's the base of the window, move the window
            if ack_num == self.base_seq_num:                        
                self.buffer.pop(0)
                self.base_seq_num += 1
                while len(self.buffer) > 0:                     
                    next_packet = self.buffer[0]
                    # If not received yet (has a timer), stop
                    if not next_packet or next_packet.timer is not None:
                        break
                    # Otherwise, remove it from the buffer and continue with the next
                    self.buffer.pop(0)
                    self.base_seq_num += 1
                    
    def is_empty(self):
        """
        Check if the buffer is empty.

        Returns:
            bool: True if the buffer is empty, False otherwise.
        """
        return len(self.buffer) == 0

    def close(self):
        """
        Close the window, canceling timers.
        """
        for packet in self.buffer:
            if packet.timer != None:
                packet.timer.cancel()
                packet.timer = None

    def len_buf(self):
        """
        Get the length of the buffer.

        Returns:
            int: The length of the buffer.
        """
        return len(self.buffer)

    def return_buf(self):
        """
        Return the buffer.

        Returns:
            list: The buffer.
        """
        return self.buffer