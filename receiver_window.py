

class ReceiverWindow:
    window = None
    base_seq = None

    def __init__(self, window_size):
        self.window = []
        self.window_size = window_size
        self.base_seq = 1

    def add_packet(self, packet) -> bool :     
        if self.window_size + self.base_seq > packet.seq_num:
            return False
        

        self.window.append(packet) 
        #print(f"Window {self.window}")
        return True
    
    def get_ordered_packets(self) -> list:
        self.window.sort(key=lambda packet: packet.seq_num)
        
        packets = []

        # siempre que el primer paquete de la lista sea el que esperamos,
        # lo sacamos de la lista y lo agregamos a la lista de paquetes
        # a devolver al user        
        while len(self.window) > 0:                        
            packet = self.window[0]
            print(packet.data)
            print(f"{packet.seq_num} == {self.base_seq}")
            if packet.seq_num == self.base_seq:
                self.window.pop(0)
                self.base_seq += 1
                packets.append(packet)
            else:
                break
        print(f"packets {packets}")
        return packets
