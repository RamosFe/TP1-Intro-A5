from collections import *

class ReceiverWindow:
    window = None
    base_seq = None
    window_size = None
    received = None

    def __init__(self, window_size):
        self.window = OrderedDict()
        self.window_size = window_size
        self.base_seq = 1

    def add_packet(self, packet) -> bool :    
        if self.window_size + self.base_seq < packet.seq_num:
            return False
        
        self.window[packet.seq_num] = packet
        return True
    
    def get_ordered_packets(self) -> list:
        packets = []

        # siempre que el primer paquete de la lista sea el que esperamos,
        # lo sacamos de la lista y lo agregamos a la lista de paquetes
        # a devolver al user       
        while self.base_seq in self.window:
            packet = self.window[self.base_seq]
            packets.append(packet)
            del self.window[self.base_seq]
            self.base_seq += 1
        return packets


    def already_received(self, seq_num) -> bool:
        return seq_num < self.base_seq or seq_num in self.window

        
