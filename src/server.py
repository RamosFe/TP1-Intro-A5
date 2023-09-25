

from lib.rdt.rdt_sw_socket import RdtSWSocketClient
from lib.constants import HARDCODED_BUFFER_SIZE

socket_server = RdtSWSocketClient()
socket_server.bind(('localhost', 6000))
while True:
    data = socket_server.recv(HARDCODED_BUFFER_SIZE)
    print(f"Data: {data.decode()}")