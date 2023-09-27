

from lib.rdt.rdt_sw_socket import RdtSWSocketClient
from lib.constants import HARDCODED_BUFFER_SIZE

socket_server = RdtSWSocketClient()
socket_server.bind(('localhost', 6000))


with open('prueba_1.webp', 'wb') as file:
    while True:
        data = socket_server.recv(HARDCODED_BUFFER_SIZE)
        print(data)
        file.write(data)
    
