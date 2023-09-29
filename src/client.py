from lib.rdt.rdt_sw_socket import RdtSWSocketClient
from lib.constants import HARDCODED_BUFFER_SIZE

addr = ("127.0.0.1", 6000)

socket = RdtSWSocketClient()
socket._internal_socket.sendto('UPLOAD:foto.webp:38000'.encode(), addr)
datita_de_la_buena = socket._internal_socket.recv(HARDCODED_BUFFER_SIZE)
print(f"Para el OK me llego f{datita_de_la_buena.decode()}")

print("HOLIS")
with open('foto.webp', 'rb') as file:
    image_data = file.read()
    # print(image_data)
    socket.sendto(image_data, addr)

