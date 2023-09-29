
class Packet:
    def __init__(self, seq_num, data):
        self.seq_num = seq_num
        self.data = data
        self.timer = None
        self.timeouts = 0
    
    def into_bytes(self):
        return self.seq_num.to_bytes(4, byteorder='big') + self.data
    
    def from_bytes(self, bytes):
        self.seq_num = int.from_bytes(bytes[:4], byteorder='big')
        self.data = bytes[4:]

    def is_ack(self):
        return self.data == b"ACK"  