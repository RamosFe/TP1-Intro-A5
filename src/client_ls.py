


import os
import lib.client_lib.parser as parser
import lib.client_lib.utils as parser_utils
from lib.commands import Command, MessageOption
from lib.handshake import ThreeWayHandShake
from lib.rdt.rdt_sw_socket import RdtSWSocketClient
from lib.constants import LIST_FILES_FINISH,HARDCODED_BUFFER_SIZE

def main(addr: tuple[str, int]):
    """
    Main function to list files on the server.

    Args:
        addr (tuple[str, int]): The address of the server.

    Note:
        This function sends a command to the server to list files.
        It then receives and prints the server's response until the server signals the end of the listing process.
    """
    client_socket = RdtSWSocketClient()  # Initialize the client socket
    command = Command(MessageOption.LIST_FILES, None, 0)  # Create a command to list files
    
    while True:
        print("Sending command")  # Print status message
        client_socket.send_with_internal_socket(command.to_str().encode(), addr)  # Send the command to the server
        
        response = client_socket.recv(HARDCODED_BUFFER_SIZE)  # Receive response from the server
        
        if response is None:  # If no response received, continue loop
            continue
        
        if LIST_FILES_FINISH in response.decode():  # If the server signals the end of listing
            break
        else:
            print(response.decode())  # Print the received response

if __name__ == '__main__':
    args = parser.parse_arguments("ls")  # Parse command line arguments
    if not parser_utils.verify_params(args, "ls"):  # Verify if required arguments are provided
        print("❌ Error: missing required argument(s) ❌")  # Print error message if arguments are missing
        args.print_help()  # Print help message for command
    
    else:
        main((args.host, args.port))  # Call the main function with server address
