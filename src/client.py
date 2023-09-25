from lib.rdt.rdt_sw_socket import RdtSWSocketClient

socket = RdtSWSocketClient()
data = 'roberto'
socket.sendto(data, ("127.0.0.1", 6000))