
class Packet:
    def __init__(self, seq_num, data):
        self.seq_num = seq_num
        self.data = data
        self.timer = None
        self.timeouts = 0
    
    def into_bytes(self):
        return self.seq_num.to_bytes(4, byteorder='big') + self.data
    
    @staticmethod
    def from_bytes(bytes):
        seq_num = int.from_bytes(bytes[:4], byteorder='big')
        data = bytes[4:]
        return Packet(seq_num, data)

    #TODO:REFACTORIZAR LA DATA TENDRIA QUE TENER EL SEQUENCE NUMBER
    def is_ack(self):
        return self.data == b"ACK"  
    
    def get_data (self):
        return self.data