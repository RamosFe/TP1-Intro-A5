import queue   
import threading
from receiver_window import ReceiverWindow
from sliding_window import SlidingWindow
import socket 
from packet import *


WINDOW_SIZE = 4


def send_packets(packets,socket,ack_queue: queue.Queue):
    # Create a sliding window with a size of WINDOW_SIZE
    window = SlidingWindow(WINDOW_SIZE,socket=socket)

    # Send each packet in the list
    for packet in packets:
        # Wait until there is space in the window
        while not window.add_packet(packet):
            # If there is no space, receive an ACK and move the window base forward
            # TODO bloquear hasta que haya un ACK.? fijase si esta lockeando o no.
            while not ack_queue.empty():            
                ack_num = ack_queue.get()
                with open("client_log.txt", "a") as f:
                    f.write(f"Received ack: {ack_num}\n")
                
                window.receive_ack(ack_num)

        # If there is space, send the packet and start its timer
        # TODO mandar paquete
        #print(f"Sended packet: {packet.seq_num}")
        socket.sendto(packet.into_bytes(), ("localhost", 7070))
        while not ack_queue.empty():            
            ack_num = ack_queue.get()
            with open("client_log.txt", "a") as f:
                f.write(f"Received ack: {ack_num}\n")
                
            window.receive_ack(ack_num)
        
    with open("client_log.txt", "a") as f:
        f.write(f"sali de mandar paquetes con len: {len(window.buffer)}\n")
    # Wait for ACKs for any remaining packets in the window
    while len(window.buffer) > 0:
        #ack_nums = receive_ack(socket=socket)
        while not ack_queue.empty():     
            ack_num = ack_queue.get()       
            with open("client_log.txt", "a") as f:
                    f.write(f"Received ack: {ack_num}\n")
            window.receive_ack(ack_num)



'''Mock server receiving packets and sending ACKs'''
def server_receive_packets():
    # Listen for incoming packets  in port 7070 and send ACKs    
    UDP_PORT = 7070
    ignore_pkt = True
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("localhost", UDP_PORT))

    recv_window = ReceiverWindow()

    while True:
        print("Waiting for packets...")
        data, addr = sock.recvfrom(1024)        
        seq_num = int.from_bytes(data[:4], byteorder='big')
        ack_packet = Packet(seq_num, b"ACK")

        if seq_num == 4 and ignore_pkt:
            ignore_pkt = False
            continue                              
        
        # Log the above print to the server_log.txt file
        packets = recv_window.add_packet(Packet(seq_num, data[:4]),addr) 
        for packet in packets:
            with open("server_log.txt", "a") as f:
                f.write(f"Received packet: {packet.seq_num}\n")
        
        print(f"lista: {recv_window.get_list_addr(addr)}")

def client_receive_packets(socket, queue: queue.Queue):
    while True:
        data, _ = socket.recvfrom(1024)        
        seq_num = int.from_bytes(data[:4], byteorder='big')                
        queue.put(seq_num)
        



def main():
    
    # Also create if it not exists
    
    # Truncate a file with the name sercver_log.txt
    with open("server_log.txt", "w") as f:
        f.write("")

    with open("client_log.txt", "w") as f:
        f.write("")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Create a thread safe queue to store received ACKs
    ack_queue = queue.Queue()

    
    packets = [
        Packet(0, b"packet0"),
        Packet(1, b"packet1"),
        Packet(2, b"packet2"),
        Packet(3, b"packet3"),
        Packet(4, b"packet4"),
        Packet(5, b"packet5"),
        Packet(6, b"packet6"),
        Packet(7, b"packet7"),
    ]
    
    # Start a thread to receive packets and send ACKs
    receive_thread = threading.Thread(target=server_receive_packets)
    receive_thread.start()
    
    send_thread = threading.Thread(target=send_packets, args=(packets,sock,ack_queue))
    send_thread.start()


    client_receive_packets(sock, ack_queue)

    # END: 1a2b3c4d5e6f

main()