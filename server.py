from selective_repeat import SelectiveRepeatRDT
from tester import WINDOW_SIZE
from commands import Command, CommandResponse, MessageOption
import socket
import threading
import  queue   


WINDOW_SIZE = 128
UDP_PORT = 7070


class server:    
    _socket = None

    def __init__(self):        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("localhost", UDP_PORT))
        self._socket = sock
        threading.Thread(target=self.poll_socket).start()


    def poll_socket(self):    
        connections = {}
        while True:
            data,addr = self._socket.recvfrom(1024)                
            if addr not in connections:
                data_queue = queue.Queue()
                protocol = SelectiveRepeatRDT(WINDOW_SIZE, data_queue,self._socket, addr)
                threading.Thread(target=handle_protocol, args=(protocol)).start()
                data_queue.put(data)
                connections[addr] = data_queue
            else:
                connections[addr].put(data)
        


def handle_protocol(protocol):
    bytes_message = protocol.receive_message()        
    command = Command.from_str(bytes_message.decode())
    
    if command.option == MessageOption.UPLOAD:
        
        pass
    elif command.option == MessageOption.DOWNLOAD:
        
        pass
    else:
        response = CommandResponse.err_response("Invalid command option.")    
        protocol.send_message(response.to_str().encode())
    









