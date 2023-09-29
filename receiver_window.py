class ReceiverWindow:
    window = None

    def __init__(self):
        self.window = {}
    
    def add_packet(self, packet) -> []: #devuelve una lista de paquetes en orden
        src = packet.src()

        # me fijo en el set de mensajes pendientes de ese src
        self.window[src] = self.window.get(src, [set(), 0])
        base_seq_num = self.window[src][1]
        
        # si es un paquete viejo, no lo agrega
        # probablemente se perdió el ack que mandamos
        # y nos lo volvieron a mandar
        if packet.seq_num < base_seq_num:
            # EN ESTE CASO HAY QUE VOLVER A MANDAR EL ACK
            return []
        
        # si es un paquete con el seq que esperamos,
        # vamos a devolver ese y todos los que destrabe
        if packet.seq_num == base_seq_num:
            self.window[src][1] += 1
            packets = [packet] + self._get_ordered_packets(src)
            return packets
        
        # si es un paquete que no esperamos, lo agregamos
        # al set de paquetes pendientes y esperamos
        self.window.append(packet)
        return []
    
    def _get_ordered_packets(self, src) -> []:
        # agarro los paquetes pendientes enviados por el src
        pending_packets = self.window[src][0]
        pending_packets.sort(key=lambda packet: packet.seq_num)
        packets = []

        # siempre que el primer paquete de la lista sea el que esperamos,
        # lo sacamos de la lista y lo agregamos a la lista de paquetes
        # a devolver al user
        while len(pending_packets) > 0:
            packet = pending_packets[0]
            if packet.seq_num == self.window[src][1]:
                pending_packets.pop(0)
                self.window[src][1] += 1
                packets.append(packet)
            else:
                break
        return packets
