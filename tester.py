import queue   
import threading
from  selective_repeat import SelectiveRepeatRDT
import socket 
from packet import *


WINDOW_SIZE = 4


'''Mock server receiving packets and sending ACKs'''
def server_receive_packets():
    # Listen for incoming packets  in port 7070 and send ACKs    
    UDP_PORT = 7070
    ignore_pkt = True
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("localhost", UDP_PORT))

    # data_queue = queue.Queue()
    # msg_queue = queue.Queue()
    # selective_repeat = SelectiveRepeatRDT(WINDOW_SIZE, data_queue, msg_queue, socket,("localhost", UDP_PORT) )
    while True:
        data,addr = sock.recvfrom(1024)        
        #
        packet = Packet.from_bytes(data)
        print(f"la data que llego es {packet.get_data()}")
        # data_queue.put(data)
        
        seq_num = int.from_bytes(data[:4], byteorder='big')
        ack_packet = Packet(seq_num, b"ACK")
        with open("server_log.txt", "a") as f:
            f.write(f"sequence number received:{seq_num}\n")
        sock.sendto(ack_packet.into_bytes(),addr) 

        # packets = selective_repeat.get_packets()            
        # for packet in packets:
        #     with open("server_log.txt", "a") as f:
        #         f.write(f"Received packet: {packet.seq_num}\n")
        


def main():
    
    # Also create if it not exists
    
    # Truncate a file with the name sercver_log.txt
    with open("server_log.txt", "w") as f:
        f.write("")

    with open("client_log.txt", "w") as f:
        f.write("")


    server = threading.Thread(target=server_receive_packets)
    server.start()
  
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Como cliente me quiero comunicar con el localhost 7070
    addr = ("localhost", 7070)
    # PRIMER DATA UPLOAD o DOWNLOAD
    data_queue = queue.Queue()
    
    protocol = SelectiveRepeatRDT(WINDOW_SIZE, data_queue,sock, addr)

    protocol.send_message("Hola servidor!".encode())

    msg = protocol.receive_message()
    
    print(msg)

    




    

    # END: 1a2b3c4d5e6f

main()