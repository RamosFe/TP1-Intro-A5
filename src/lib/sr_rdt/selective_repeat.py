from math import ceil
import socket
import threading
from lib.constants import HARDCODED_CHUNK_SIZE
from lib.sr_rdt.packet import Packet
from lib.sr_rdt.receiver_window import ReceiverWindow
from lib.sr_rdt.sliding_window import SlidingWindow

from threading import Event
from queue import *
class SenderSR:
    _sender = None
    _window = None
    _response_queue = None
    _seq_num = None
    _ack_queue = None
    _stop_event = None
    _socket = None

    def __init__(self, window_size, response_queue, ack_queue, socket, addr, stop_event: Event):
        """
        Initialize the SenderSR object.

        Args:
            window_size (int): Size of the sliding window.
            response_queue (queue.Queue): Queue for packets waiting to be sent.
            ack_queue (queue.Queue): Queue for received acknowledgments.
            socket (socket.socket): The socket used for communication.
            addr (tuple): The address to which packets will be sent.
            stop_event (threading.Event): Event to signal when to stop the sender thread.
        """
        # Initialize various attributes
        self._window = SlidingWindow(window_size, socket, addr, stop_event)  # Initialize sliding window
        self._response_queue = response_queue  # Store response queue
        self._stop_event = stop_event  # Store stop event
        self._ack_queue = ack_queue  # Store acknowledgment queue
        self._seq_num = 1  # Initialize sequence number
        self._socket = socket  # Store socket
        self._addr = addr  # Store address

        # Start the sender thread
        self._sender = threading.Thread(target=self._send_packets, args=(self._response_queue, socket))
        self._sender.start()

    def _make_packets(self, data) -> list:
        """
        Create a list of packets from the provided data.

        Args:
            data (bytes): The data to be split into packets.

        Returns:
            list: List of packets.
        """
        # Calculate the number of packets needed for the data
        n_packets = ceil(len(data) / HARDCODED_CHUNK_SIZE)  # Calculate number of packets
        packets = []
        for i in range(1, n_packets + 1, 1):
            chunk = data[(i-1) * HARDCODED_CHUNK_SIZE : i * HARDCODED_CHUNK_SIZE]  # Extract a chunk of data
            packet = Packet(self._seq_num , chunk)  # Create a packet with the chunk
            packets.append(packet)  # Add packet to the list
            self._seq_num += 1  # Increment sequence number
        
        # Add an end-of-packet (EOP) marker
        end_packet = Packet(self._seq_num, b'EOP')  # Create an EOP packet
        self._seq_num += 1  # Increment sequence number
        packets.append(end_packet)  # Add EOP packet to the list
        return packets

    def check_ack_queue(self):
        """
        Check the acknowledgment queue for received acknowledgments.
        """
        while not self._ack_queue.empty():  # While acknowledgment queue is not empty
            ack_num = self._ack_queue.get()  # Get acknowledgment number
            self._window.receive_ack(ack_num)  # Pass acknowledgment to sliding window

    def _send_packets(self, response_queue, socket):
        """
        Send packets from the response queue.

        Args:
            response_queue (queue.Queue): Queue containing packets to be sent.
            socket (socket.socket): The socket for sending packets.
        """
        while not self._stop_event.is_set():  # While stop event is not set
            
            try:
                packet = response_queue.get_nowait()  # Get a packet from the response queue (non-blocking)
            except Empty:
                # Handle the case where the queue is empty
                self.check_ack_queue()  # Check for acknowledgments
                continue
            
            if packet is None:  # If packet is None, skip
                continue
            
            # If the sliding window is full, keep checking for acknowledgment of packets
            while not self._window.add_packet(packet) and not self._stop_event.is_set():
                self.check_ack_queue()  # Check for acknowledgments
            
            if self._stop_event.is_set():  # If stop event is set, break out of loop
                break
                
            if packet.seq_num == 100:  # If sequence number is 100 (assuming this is a special condition)
                continue
            socket.sendto(packet.into_bytes(), self._addr)  # Send the packet
            self.check_ack_queue()  # Check for acknowledgments

    def packets_pending(self):
        """
        Check if there are pending packets to be sent.

        Returns:
            bool: True if there are pending packets, False otherwise.
        """
        return not self._window.is_empty() or not self._response_queue.empty()  # Check if window or response queue is not empty
    
    def close(self):
        """
        Close the SenderSR.
        """
        self._window.close()  # Close the sliding window
        self._sender.join()  # Join the sender thread

class ReceiverSR:
    _receiver = None
    _window = None
    _data_queue = None
    _ack_queue = None
    _msg_queue = None
    _stop_event = None

    def __init__(self, window_size, data_queue, ack_queue, sock, msg_queue, addr, stop_event):
        """
        Initialize the ReceiverSR object.

        Args:
            window_size (int): Size of the receiver window.
            data_queue (queue.Queue): Queue for received data packets.
            ack_queue (queue.Queue): Queue for sending acknowledgments.
            sock (socket.socket): The socket used for communication.
            msg_queue (queue.Queue): Queue for ordered packets to be processed.
            addr (tuple): The address from which packets are received.
            stop_event (threading.Event): Event to signal when to stop the receiver thread.
        """
        # Initialize various attributes
        self._window = ReceiverWindow(window_size)  # Initialize receiver window
        self._stop_event = stop_event  # Store stop event
        self._ack_queue = ack_queue  # Store acknowledgment queue
        self._data_queue = data_queue  # Store data queue
        self._msg_queue = msg_queue  # Store message queue        
        self._receiver = threading.Thread(target=(self._receive_packets), args=(sock, addr))  # Initialize receiver thread
        self._receiver.start()  # Start the receiver thread

    def _receive_packets(self, socket, addr):
        """
        Receive and process packets.

        Args:
            socket (socket.socket): The socket used for communication.
            addr (tuple): The address from which packets are received.
        """
        while not self._stop_event.is_set():  # While stop event is not set
            try:
                packet = self._data_queue.get_nowait()  # Get a packet from the data queue (non-blocking)
                if packet is None:  # If packet is None, continue
                    continue 
            except Empty:
                continue  # Handle the case where the queue is empty

            packet = Packet.from_bytes(packet)  # Convert bytes to packet object
            
            if packet.is_ack():  # If packet is an acknowledgment
                self._ack_queue.put(packet.seq_num)  # Put acknowledgment in the queue                
                continue
            
            if self._window.already_received(packet.seq_num):  # If packet has already been received
                ack = Packet(packet.seq_num, b'ACK')  # Create an acknowledgment packet
                socket.sendto(ack.into_bytes(), addr)  # Send the acknowledgment
                continue

            if not self._window.add_packet(packet):  # If packet is successfully added to the window    
                continue
            
            ack = Packet(packet.seq_num, b'ACK')  # Create an acknowledgment packet
            socket.sendto(ack.into_bytes(), addr)  # Send the acknowledgment
            
            packets = self._window.get_ordered_packets()  # Get ordered packets from the window
            for pkt in packets:  # For each packet in the ordered list               
                self._msg_queue.put(pkt)  # Put the packet in the message queue
        
    def close(self):
        """
        Close the ReceiverSR.
        """
        self._receiver.join()  # Join the receiver thread
        
                                                             
class SelectiveRepeatRDT:
    # Class Variables
    _socket = None
    _sender = None
    _receiver = None
    _data_queue = None
    _stop_event = None
    _response_queue = None
    _msg_queue = None

    def __init__(self, window_size, data_queue, socket, addr):
        """
        Initialize the SelectiveRepeatRDT object.

        Args:
            window_size (int): Size of the sliding window.
            data_queue (queue.Queue): Queue for sending/receiving data.
            socket (socket.socket): The socket used for communication.
            addr (tuple): The address of the sender/receiver.
        """
        # Initialize class attributes
        self._socket = socket
        self._data_queue = data_queue  # Store data queue
        self._stop_event = Event()  # Initialize stop event
        self._response_queue = Queue()  # Initialize response queue
        self._msg_queue = Queue()  # Initialize message queue
        ack_queue = Queue()  # Initialize acknowledgment queue

        # Initialize sender sliding window
        self._sender = SenderSR(window_size, self._response_queue, ack_queue, socket, addr, stop_event=self._stop_event)

        # Initialize receiver window
        self._receiver = ReceiverSR(window_size, data_queue, ack_queue, socket, self._msg_queue, addr, stop_event=self._stop_event)

    
    def send_message(self, data):
        """
        Receive a message from the application layer, break it into packets, and send it to the recipient.

        Args:
            data (bytes): The data to be sent.
        """
        # Assemble packets from the data.
        while self._response_queue.qsize() > 8 and not self._stop_event.is_set():
            continue

        if self._stop_event.is_set():
            raise TimeoutError

        packets = self._sender._make_packets(data)
        for packet in packets:
            self._response_queue.put(packet)


    def receive_message(self) -> bytes:
        """
        Receive a message from the recipient and return it to the application layer.

        Returns:
            bytes: The received message.
        """
        message = b''

        # Should give us a list until the EOP (End of Packet) marker arrives.
        packets = self.get_packets()

        for packet in packets:
            message += packet.get_data()

        return message

    def get_packets(self) -> list:
        """
        Retrieve a list of packets from the message queue.

        Returns:
            list: List of received packets.
        """
        packet = None
        packets = []

        while not self._stop_event.is_set() and packet is None:
            try:
                packet = self._msg_queue.get(timeout=0.05)
            except Empty:
                continue

        if self._stop_event.is_set() or not packet:
            raise TimeoutError

        while not packet.data == b'EOP':
            packets.append(packet)
            packet = self._msg_queue.get()

        return packets

    def close_connection(self): 
        """
        Close the connection gracefully.
        """
        print("Closing connection...")

        while self.packets_pending() and not self._stop_event.is_set():
            continue

        # Send signal to threads to terminate
        self._stop_event.set()
        self._sender.close()
        self._receiver.close()

        print("Connection closed completely")

    def packets_pending(self) -> bool:
        """
        Check if there are pending packets to be sent.

        Returns:
            bool: True if there are pending packets, False otherwise.
        """
        return self._sender.packets_pending()            

    def get_event(self) -> Event:
        """
        Get the stop event.

        Returns:
            threading.Event: The stop event.
        """
        return self._stop_event