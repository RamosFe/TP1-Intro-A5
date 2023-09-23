from queue import Queue
from src.rdt_stop_and_wait import RdtWSSocket

def sender(channel_receive: Queue):
    server_socket = RdtWSSocket()
    while True:
        if not channel_receive.empty():
            # try:
                (data, addr) = channel_receive.get(block= False, timeout = None)   # the data is received as (data,addr)   (ip,port)
                server_socket.send(data, addr)
            # except Exception as e:
            #     print(f"There has been an exception as {e}")