from math import ceil
import socket
import threading
from packet import Packet
from receiver_window import ReceiverWindow
from sliding_window import SlidingWindow
from queue import *

PACKET_SIZE = 10

class SenderSR:
    _sender = None
    _window = None
    _response_queue = None
    _seq_num = None
    _ack_queue = None

    def __init__(self, window_size, response_queue, ack_queue, socket, addr):
        self._window = SlidingWindow(window_size,socket)
        self._response_queue =  response_queue
        self._sender = threading.Thread(target=self._send_packets, args=(self._response_queue,socket))
        self._ack_queue = ack_queue
        self._sender.start()
        self._seq_num = 0
        self._socket = socket
        self._addr = addr

        

    def _make_packets(self, data) -> list:
        # crear una lista de paquetes a partir de los datos
        n_packets = ceil(len(data) / PACKET_SIZE)
        packets = []
        for i in range(1, n_packets + 1, 1):
            packet = Packet(self._seq_num + i,data[(i-1) * PACKET_SIZE : i * PACKET_SIZE])
            packets.append(packet)
        
        
        end_packet = Packet(n_packets + 1, b'EOP')
        packets.append(end_packet)
        self._seq_num = self._seq_num + n_packets + 2
        print(f"Lastseq: {end_packet.seq_num}")
        return packets
        #puede pasar que se generen paquetes con un seq numb que desp no se pueden enviar porque 
        #la window esta llena, quizás hay q revisar este caso (ej no mandar toda la data o mandar
        #solo los paquetes que entren en la window)

    def check_ack_queue(self):
        while not self._ack_queue.empty():            
            ack_num = self._ack_queue.get()
            
            with open("client_log.txt", "a") as f:
                f.write(f"Received ack: {ack_num}\n")
            self._window.receive_ack(ack_num)

    def _send_packets(self, response_queue, socket):
        while True:            
            packet = response_queue.get() # Esto seria response_queue
            if packet is None:
                continue
           
            #If the sliding window is full, keep checking for ack of packets
            while not self._window.add_packet(packet):
                self.check_ack_queue()
                
            socket.sendto(packet.into_bytes(),self._addr)
            self.check_ack_queue()

class ReceiverSR:
    _receiver = None
    _window = None
    _data_queue = None
    _ack_queue = None
    _msg_queue = None

    def __init__(self, window_size, data_queue, ack_queue, msg_queue):
        self._window = ReceiverWindow(window_size)
        self._ack_queue = ack_queue
        self._data_queue = data_queue
        self._msg_queue = msg_queue        
        self._receiver = threading.Thread(target=self._receive_packets)
        self._receiver.start()

    def _receive_packets(self):
                
        while True:
            packet = self._data_queue.get(block=True)
            if packet is None:
                continue 
            #ver si el packet es ACK O mensaje, 
            #si es mensaje -> receive window,
            #si es ack -> ACK queue
            packet = Packet.from_bytes(packet)
            
            if packet.is_ack():               
                self._ack_queue.put(packet.seq_num)
                #print(f"Seq sended:{packet.seq_num}")    
                continue
            self._window.add_packet(packet)
            packets = self._window.get_ordered_packets()
            print(packets)
            for pkt in packets:                
                self._msg_queue.put(pkt)
            

class SelectiveRepeatRDT:
    _socket = None
    _sender = None
    _receiver = None

    def __init__(self, window_size, data_queue, socket, addr):
        self._socket = socket
        ack_queue = Queue()
        self._response_queue = Queue()
        self._sender = SenderSR(window_size,self._response_queue , ack_queue,socket,addr) #sender sliding window
        
        self._msg_queue = Queue()
        self._receiver = ReceiverSR(window_size,data_queue, ack_queue, self._msg_queue) # receiver window
                
    
    '''Recibe el mensaje de capa de aplicación para ser desarmado en paquetes y enviado al destinatario'''
    def send_message(self, data):
        # Primero armamos los paquetes a partir de la data.
        
        packets = self._sender._make_packets(data)
        for packet in packets:
            self._response_queue.put(packet)
        
    '''Devuelve un mensaje hacia la capa de aplicación '''
    def receive_message(self) -> str:
        message = ""
                
        # Deberia darnos una lista hasta que llegue el EOP
        packets = self.get_packets()
        print(f"Len{len(packets)}")            
        
        for packet in packets:               
            data = packet.get_data()          
            message += packet.get_data()
        
        return message
    
    def get_packets(self) -> list:
        
        packets = []        
        data = self._msg_queue.get()
        packet = Packet.from_bytes(data) 
        while not packet.data == b'EOP':
            data = self._msg_queue.get()
            packet = Packet.from_bytes(data)   
            packets.append(packet)
        
        return packets
    
    
    