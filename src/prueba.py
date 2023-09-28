



ack = int(1)


print(ack.to_bytes(1, byteorder='big'))

ack_ = ack.to_bytes(1, byteorder='big')

integer_from_bytes = int.from_bytes(ack_, byteorder='big')

print(integer_from_bytes)


