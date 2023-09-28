import socket
import threading
from sliding_window import SlidingWindow
from queue import *

class SelectiveRepeatRDT:
    _window = None
    _socket = None
    _send_queue = None
    _received_queque = None
    _ack_queue = None
    _sender = None
    _receiver = None

    def __init__(self, window_size, socket, queue):
        self._window = SlidingWindow(window_size, socket)
        self._socket = socket
        self._send_queue = queue
        self._ack_queue = Queue()
        self._sender = threading.Thread(target=self._send_packets, args=(self._send_queue,))
        self._receiver = threading.Thread(target=self._receive_packets, args=(self._socket,))
        self._sender.start()
        self._receiver.start()
    
    def send(self, data, address):
        packets = self._make_packets(data, address)
        for packet in packets:
            self._send_queue.put(packet)
    
    def _make_packets(self, data, address):
        # crear una lista de paquetes a partir de los datos
        pass

    def _send_packets(self, queue):
        while True:
            packet = queue.get()
            if packet is None:
                continue
           
            while not self._window.add_packet(packet):
            # If there is no space, receive an ACK and move the self._window base forward
            # TODO bloquear hasta que haya un ACK.? fijase si esta lockeando o no.
                while not self._ack_queue.empty():            
                    ack_num = self._ack_queue.get()
                    with open("client_log.txt", "a") as f:
                        f.write(f"Received ack: {ack_num}\n")
                    
                    self._window.receive_ack(ack_num)
                
                self._socket.sendto(packet.into_bytes(), packet.dest())
    
    # def _receive_packets(self, socket):
    #     hashed_buffer = {} # usada para darle al usuario paquetes en orden

    #     while True:
    #         data = socket.recv(1024)
    #         packet = data.encode()
    #         if packet is None:
    #             continue
    #         if packet.is_ack():
    #             self._ack_queue.put(packet.seq_num)
    #             continue
    #         src = packet.src()
    #         hashed_buffer[src] = hashed_buffer.get(src, (set(), 0))
    #         if 



            

