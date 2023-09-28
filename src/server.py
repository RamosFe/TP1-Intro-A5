

from lib.rdt.rdt_sw_socket import RdtSWSocketClient
from lib.constants import HARDCODED_BUFFER_SIZE
import queue

socket_server = RdtSWSocketClient()
socket_server.bind(('localhost', 6000))
super_channel = queue.Queue()

super_channel.put(socket_server._internal_socket.recvfrom(HARDCODED_BUFFER_SIZE))
command, addr = socket_server.recvfrom_with_queue(super_channel)
print(f"Recibi el comando f{command.decode()}")
socket_server._internal_socket.sendto('OK'.encode(), addr)

print("ABRI EL ARCHIVO")

with open('prueba_1.webp', 'wb') as file:
    while True:
        super_channel.put(socket_server._internal_socket.recvfrom(HARDCODED_BUFFER_SIZE))
        data = socket_server.recv_with_queue(super_channel)
        if data is None:
            continue
        file.write(data)
    
