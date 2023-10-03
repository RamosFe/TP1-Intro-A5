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
    

    def __init__(self, window_size, response_queue, ack_queue, socket, addr,stop_event: Event):
        self._window = SlidingWindow(window_size,socket, addr, stop_event)
        self._response_queue =  response_queue
        self._stop_event = stop_event
        self._ack_queue = ack_queue
        self._seq_num = 1
        self._socket = socket
        self._addr = addr

        self._sender = threading.Thread(target=self._send_packets, args=(self._response_queue,socket))
        self._sender.start()


        

    def _make_packets(self, data) -> list:
        # crear una lista de paquetes a partir de los datos
        n_packets = ceil(len(data) / HARDCODED_CHUNK_SIZE)
        packets = []
        for i in range(1, n_packets + 1, 1):
            chunk = data[(i-1) * HARDCODED_CHUNK_SIZE : i * HARDCODED_CHUNK_SIZE]
            packet = Packet(self._seq_num , chunk)
            packets.append(packet)
            self._seq_num += 1
        
        
        end_packet = Packet(self._seq_num, b'EOP')
        self._seq_num += 1
        packets.append(end_packet)
        return packets
        #puede pasar que se generen paquetes con un seq numb que desp no se pueden enviar porque 
        #la window esta llena, quizás hay q revisar este caso (ej no mandar toda la data o mandar
        #solo los paquetes que entren en la window)

    def check_ack_queue(self):
        while not self._ack_queue.empty():            
            ack_num = self._ack_queue.get()
            
            
            # with open("client_log.txt", "a") as f:
            #     f.write(f"Received ack: {ack_num}\n")
            self._window.receive_ack(ack_num)

    def _send_packets(self, response_queue, socket):
        while not self._stop_event.is_set():
            
            try:
                packet = response_queue.get_nowait()
            except Empty:
                # Handle the case where the queue is empty
                self.check_ack_queue()
                continue
            
            if packet is None:
                continue
           
            #If the sliding window is full, keep checking for ack of packets
            while not self._window.add_packet(packet):
                self.check_ack_queue()
                
            if packet.seq_num == 100:
                continue
            socket.sendto(packet.into_bytes(),self._addr)
            self.check_ack_queue()

    def packets_pending(self):
        #print(f"slice window : {self._window.is_empty()} and _response {self._response_queue.empty()}")
        # print(f"{self._window.len_buf()}")
        # print(f"{self._window.return_buf()}")
        return not self._window.is_empty() or not self._response_queue.empty()


class ReceiverSR:
    _receiver = None
    _window = None
    _data_queue = None
    _ack_queue = None
    _msg_queue = None

    def __init__(self, window_size, data_queue, ack_queue, sock, msg_queue, addr, stop_event):
        self._window = ReceiverWindow(window_size)
        self.stop_event = stop_event
        self._ack_queue = ack_queue
        self._data_queue = data_queue
        self._msg_queue = msg_queue        
        self._receiver = threading.Thread(target=(self._receive_packets), args=(sock,addr))
        self._receiver.start()

    def _receive_packets(self, socket, addr):
                
        while not self.stop_event.is_set():            
            try:
                packet = self._data_queue.get_nowait()
                if packet is None:
                    continue 
            except Empty:
                continue
            #ver si el packet es ACK O mensaje, 
            #si es mensaje -> receive window,
            #si es ack -> ACK queue
            packet = Packet.from_bytes(packet)
            
            if packet.is_ack():               
                self._ack_queue.put(packet.seq_num)                
                continue
            
            # TODO -> si llega un paquete repetido hay que manejarlo
            
            if self._window.already_received(packet.seq_num): 
                ack = Packet(packet.seq_num, b'ACK')
                socket.sendto(ack.into_bytes(), addr)
                continue

            if not self._window.add_packet(packet):    
                continue
            
            ack = Packet(packet.seq_num, b'ACK')
            socket.sendto(ack.into_bytes(), addr)
            # TODO ventana llena y paquete faltante y ver este sort
            packets = self._window.get_ordered_packets()
            for pkt in packets:               
                self._msg_queue.put(pkt)
                                                             

class SelectiveRepeatRDT:
    _socket = None
    _sender = None
    _receiver = None
    _data_queue = None

    def __init__(self, window_size, data_queue, socket, addr):
        self._socket = socket
        ack_queue = Queue()
        self._stop_event = Event()
        self._data_queue = data_queue
        self._response_queue = Queue()
        self._msg_queue = Queue()
        self._sender = SenderSR(window_size,self._response_queue , ack_queue,socket,addr,stop_event=self._stop_event) #sender sliding window
        self._receiver = ReceiverSR(window_size,data_queue, ack_queue, socket, self._msg_queue, addr, stop_event=self._stop_event) # receiver window
                
    
    '''Recibe el mensaje de capa de aplicación para ser desarmado en paquetes y enviado al destinatario'''
    def send_message(self, data):
        # Primero armamos los paquetes a partir de la data.
        
        while self._response_queue.qsize() > 8:
            continue  # TODO SACAR SI NO ENTRA

        packets = self._sender._make_packets(data)
        for packet in packets:
            #print(f"mando paquete de seq num: {packet.get_seqnum()}")
            self._response_queue.put(packet)
        
    '''Devuelve un mensaje hacia la capa de aplicación '''
    def receive_message(self) -> bytes:
        message = b''
        # Deberia darnos una lista hasta que llegue el EOP
        packets = self.get_packets()         
        for packet in packets:               
            message += packet.get_data()
        return message
    
    def get_packets(self) -> list:
        packets = []
        packet = self._msg_queue.get()
        while not packet.data == b'EOP':
            packets.append(packet)
            packet = self._msg_queue.get() 
        
        return packets

    
    def close_connection(self): 
        print("Cerrando conexión...")
        while self.packets_pending():
            # print("Esperando a que se /envíen todos los paquetes...")
            continue
        
        # Mando señal a los threads para que terminen
        print("se terminaron de agarrar los paquetes")
        self._stop_event.set()


        # if self._socket is not None:
        #     self._socket.close()


    def packets_pending(self) -> bool:
        return self._sender.packets_pending()            

    def get_event(self) -> Event:
        return self._stop_event