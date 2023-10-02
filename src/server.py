

from threading import Thread
from lib.rdt.rdt_sw_socket import RdtSWSocketClient
from lib.constants import HARDCODED_BUFFER_SIZE
import queue

def handler(super_channel: queue.Queue, socket_server: RdtSWSocketClient):
    with open('prueba_1.webp', 'wb') as file:
        while True:
            data = socket_server.recv_with_queue(super_channel)
            if data is None:
                continue
            file.write(data)
        



def main():

    socket_server = RdtSWSocketClient()
    socket_server.bind(('localhost', 6000))
    super_channel = queue.Queue()


    receive,addr = socket_server._internal_socket.recvfrom(HARDCODED_BUFFER_SIZE)
    socket_server._internal_socket.sendto('OK'.encode(), addr)

    print("ABRI EL ARCHIVO")

    i = 1
    while True:
            super_channel.put(socket_server._internal_socket.recvfrom(HARDCODED_BUFFER_SIZE))
            
            if i == 1:
               
                server_thread = Thread(target=handler, args=(super_channel, socket_server))
                server_thread.start()  # Start the thread
                i+=1
main()


