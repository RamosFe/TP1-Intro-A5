import queue   
import threading
from  selective_repeat import SelectiveRepeatRDT
import socket 
from packet import *

WINDOW_SIZE = 128


'''Mock server receiving packets and sending ACKs'''
def server_receive_packets():
    # Listen for incoming packets  in port 7070 and send ACKs    
    UDP_PORT = 7070
    ignore_pkt = True
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("localhost", UDP_PORT))
    data,addr = sock.recvfrom(1024)        
    data_queue = queue.Queue()    
    protocol = SelectiveRepeatRDT(WINDOW_SIZE, data_queue,sock, addr)
    data_queue.put(data)
    poll = threading.Thread(target=poll_socket, args=(sock, data_queue))
    poll.start()   

    
    
    ## protocolo de servidor
    with open("llego.jpeg","wb") as file: 
        byte = 0
        escrito = 0 
        while True:
            chunk = protocol.receive_message()
            byte += len(chunk)
            escrito += file.write(chunk)
            print(f"byte: {byte} filesize: {escrito}")
            if escrito == 105867:
                 break
        
    

def main():
    
    # Also create if it not exists
    
    # Truncate a file with the name sercver_log.txt
    with open("server_log.txt", "w") as f:
        f.write("")

    with open("client_log.txt", "w") as f:
        f.write("")

    with open("server_protocol_log.txt", "w") as f:
        f.write("")

    with open("client_protocol_log.txt", "w") as f:
        f.write("")

    server = threading.Thread(target=server_receive_packets)
    server.start()
  
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Como cliente me quiero comunicar con el localhost 7070
    addr = ("localhost", 7070)
    # PRIMER DATA UPLOAD o DOWNLOAD
    data_queue = queue.Queue()
    
    protocol = SelectiveRepeatRDT(WINDOW_SIZE, data_queue,sock, addr) 

    # byte_array = bytearray(2560)
    # protocol.send_message(byte_array)
    # byte_array = bytearray(2560)
    # protocol.send_message(byte_array)
    with open("imagen.jpeg","rb") as file: 
        while True:
            chunk = file.read(1024)
            if not chunk:
                break
            protocol.send_message(chunk)
    
    poll = threading.Thread(target=poll_socket2, args=(sock, data_queue))
    poll.start()   

     
    msg_bytes = protocol.receive_message()    
    
    with open("client_protocol_log.txt", "a") as f:
                    f.write(f"{msg_bytes.decode()}\n")    
    
    
    #spawn a thread to receive packets from the server
    # and put them in the data_queue
    # 1a2b3c4d5e6f

    # END: 1a2b3c4d5e6f

def poll_socket(sock, data_queue):
    contador = 0
    while True:
        data,_ = sock.recvfrom(1024)        
        contador += len(data)
        data_queue.put(data)
        

def poll_socket2(sock, data_queue):
    while True:
        data,_ = sock.recvfrom(1024)        
        #print(f"data: {data}")
        data_queue.put(data)        

#main()