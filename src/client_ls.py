


import os
import lib.client_lib.parser as parser
import lib.client_lib.utils as parser_utils
from lib.commands import Command, MessageOption
from lib.handshake import ThreeWayHandShake
from lib.rdt.rdt_sw_socket import RdtSWSocketClient
from lib.constants import LIST_FILES_FINISH,HARDCODED_BUFFER_SIZE

def main(addr : tuple[str, int]):

    client_socket = RdtSWSocketClient()
    # handshake = ThreeWayHandShake(client_socket)
    command = Command(MessageOption.LIST_FILES, None, 0)
    print("Sending request to server to list files")
    client_socket.send_with_internal_socket(command.to_str().encode(), addr)

    while True:
        response = client_socket.recv(HARDCODED_BUFFER_SIZE)
        print("response",response)
        if response is None:
            continue
        if LIST_FILES_FINISH in response.decode():
            break
        else:
            print(response.decode())






if __name__ == '__main__':
    args = parser.parse_arguments("ls")
    if not parser_utils.verify_params(args, "ls"):
        print("❌ Error: missing required argument(s) ❌")
        args.print_help()
    else:
        main((args.host, args.port))
