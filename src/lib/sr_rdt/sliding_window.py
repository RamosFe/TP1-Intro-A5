import socket
import threading
import time

TIME_WAIT = 1
TOP_TIMEOUTS = 5

# TODO: Agregar addres de destino
class SlidingWindow:
    def __init__(self, window_size, socket, addr):
        self.window_size = window_size
        self.buffer = []        
        self.base_seq_num = 1
        self.socket = socket
        self.addr = addr

    def add_packet(self, packet):
        # Si hay espacio en la ventana
        if len(self.buffer) < self.window_size:
            # Creo timer de ese paquete
            packet.timer = threading.Timer(TIME_WAIT, self.timeout, [packet])
            packet.timer.start()
            # Agrego el paquete al buffer
            self.buffer.append(packet)
            
            return True
        with open("client_log.txt", "a") as f:
            f.write(f"Cannot add Pkt:{packet.seq_num} window is full \n")
        
        return False


    def get_packet(self, seq_num):
        for packet in self.buffer:
            if packet.seq_num == seq_num:
                return packet
        return None

    def timeout(self, packet):
        print(f"Timeout for packet {packet.seq_num}")
        if self.base_seq_num <= packet.seq_num < self.base_seq_num + self.window_size:
            if packet.timeouts >= TOP_TIMEOUTS:
                with open("client_log.txt", "a") as f:
                    f.write(f"Pkt:{packet.seq_num} has timeouted {TOP_TIMEOUTS} times\n")
                # TODO bye conexión
                pass
            else:
                with open("client_log.txt", "a") as f:
                    f.write(f"Pkt:{packet.seq_num} has timeouted. Resending..\n")
                self.socket.sendto(packet.into_bytes(), self.addr)
                packet.timer = threading.Timer(TIME_WAIT, self.timeout, [packet])
                packet.timer.start()
                packet.timeouts += 1

            
    def receive_ack(self, ack_num):
        # Valido que estoy dentro del rango de la window        
        if self.base_seq_num <= ack_num < self.base_seq_num + self.window_size:
            packet = self.get_packet(ack_num)

            # Si no existe el paquete devuelvo
            if not packet:
                return

            # Si existe cancelo timeout 
            packet.timer.cancel()
            packet.timer = None

            # Si es la base de la ventana, muevo la ventana
            if ack_num == self.base_seq_num:                        
                self.buffer.pop(0)
                self.base_seq_num += 1
                while len(self.buffer) > 0:                     
                    next_packet = self.buffer[0]
                    # TODO Validar cuando next_packet es None
                    # Si no lo recibi, por ende tiene timer, paro
                    if not next_packet or next_packet.timer is not None:
                        break
                    # Sino lo elimino del buffer y sigo con el siguiente
                    self.buffer.pop(0)
                    self.base_seq_num += 1
                    
    def is_empty(self):
        return len(self.buffer) == 0


    def len_buf(self):
        return len(self.buffer)

    def return_buf(self):
        return self.buffer  