from lib.rdt.rdt_sw_socket import RdtSWSocketClient

socket = RdtSWSocketClient()
data = 'roberto'
print("HOLIS")
with open('foto.webp', 'rb') as file:
    image_data = file.read()
    # print(image_data)
    socket.sendto(image_data, ("127.0.0.1", 6000))

