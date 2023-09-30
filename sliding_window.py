import socket
import threading
import time

TIME_WAIT = 0.2
TOP_TIMEOUTS = 5

class SlidingWindow:
    def __init__(self, window_size, socket):
        self.window_size = window_size
        self.buffer = []
        # self.next_seq_num = 0
        self.base_seq_num = 1
        self.socket = socket

    def add_packet(self, packet):
        
        if len(self.buffer) < self.window_size:
            packet.timer = threading.Timer(TIME_WAIT, self.timeout, [packet])
            packet.timer.start()
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
        if self.base_seq_num <= packet.seq_num < self.base_seq_num + self.window_size:
            if packet.timeouts >= TOP_TIMEOUTS:
                with open("client_log.txt", "a") as f:
                    f.write(f"Pkt:{packet.seq_num} has timeouted {TOP_TIMEOUTS} times\n")
                # TODO bye conexión
                pass
            else:
                with open("client_log.txt", "a") as f:
                    f.write(f"Pkt:{packet.seq_num} has timeouted. Resending..\n")
                self.socket.sendto(packet.into_bytes(), ("localhost", 7070))
                packet.timer = threading.Timer(TIME_WAIT, self.timeout, [packet])
                packet.timer.start()
                packet.timeouts += 1

            
    def receive_ack(self, ack_num):        
        if self.base_seq_num <= ack_num < self.base_seq_num + self.window_size:
            packet = self.get_packet(ack_num)
            if not packet:
                return
            packet.timer.cancel()
            packet.timer = None
            if ack_num == self.base_seq_num:                        
                self.buffer.pop(0)
                self.base_seq_num += 1
                while len(self.buffer) > 0:                     
                    next_packet = self.buffer[0]
                    if not next_packet or next_packet.timer is not None:
                        break
                    self.buffer.pop(0)
                    self.base_seq_num += 1

            