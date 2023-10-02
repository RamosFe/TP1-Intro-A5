import os
import socket
import threading
from lib.sr_rdt.selective_repeat import SelectiveRepeatRDT

import  queue   
from typing import Tuple

from lib.commands import Command, MessageOption, CommandResponse
from lib.fs.fs_uploader_client import FileSystemUploaderClient
from lib.client_lib import utils as parser_utils
from lib.client_lib import parser
from lib.constants import HARDCODED_BUFFER_SIZE, HARDCODED_CHUNK_SIZE, HARDCODED_TIMEOUT, UPLOAD_FINISH_MSG, HARCODED_BUFFER_SIZE_FOR_FILE, WINDOW_SIZE
from lib.rdt.rdt_sw_socket import RdtSWSocketClient
from lib.rdt.rdt_sw_socket import RdtSWSocket
from lib.handshake import ThreeWayHandShake

def poll_socket(sock: socket.socket, data_queue,event):
    sock.settimeout(HARDCODED_TIMEOUT)
    while True:
        if event.is_set():
            sock.settimeout(None)
            break
        try:
            data,_ = sock.recvfrom(1024)                
            data_queue.put(data)
        except TimeoutError:
            continue



def main(name: str, path: str, addr: Tuple[str, int], verbose: bool):
    """
    Main function to upload a file to a server.

    Args:
        name (str): The name of the file to be uploaded.
        path (str): The path to the file on the local system.
        addr (Tuple[str, int]): A tuple containing the server's address (hostname or IP) and port.
        verbose (bool): Whether to print verbose output.

    Returns:
        None
    """
    selective_repeat = True
    # Creates the upload handler
    fs_handler = FileSystemUploaderClient(HARCODED_BUFFER_SIZE_FOR_FILE)
    # Get the file size
    file_size = fs_handler.get_file_size(path=path)

    if selective_repeat:
        server_addr = ("127.0.0.1", 6000)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        stop_event = threading.Event()
        
        data_queue = queue.Queue()  
        client_socket = SelectiveRepeatRDT(WINDOW_SIZE, data_queue,sock, server_addr)
        threading.Thread(target=poll_socket, args=(sock, data_queue,stop_event)).start()
        # Creates the client socket
    else:
        client_socket = RdtSWSocketClient()
    # Creates the upload command and sends it
    command = Command(MessageOption.UPLOAD, name, file_size)

    if verbose:
        print(f"-> Sending request to server to upload file {name} with size {file_size} bytes")
    
    if selective_repeat:
        client_socket.send_message(command.to_str().encode())
        response = client_socket.receive_message().decode()
    else:
        try:
            #Creates ThreeWayHandShake
            three_way_handshake = ThreeWayHandShake(client_socket)

            response = three_way_handshake.send(command.to_str(),addr).decode()
            # Log the command if verbose

        except TimeoutError:
            print("❌ Error: server did not respond to upload request ❌")
            return
        
    response_command = CommandResponse(response)
    # If error, return
    if response_command.is_error():
        print(f"❌ Request rejected -> {response_command._msg} ❌")
        quit()

    if verbose:
        print("✔ Request accepted ✔")

    # Else, send the file using the uploader
    try:
        if selective_repeat:
            fs_handler.upload_file(None,client_socket, addr, path, name, verbose)
        else:
            fs_handler.upload_file(client_socket,None, addr, path, name, verbose)

    except TimeoutError:
        print("❌ Error: Connecction error, maximun times tried ❌")
        return

    if verbose:
        print(f"✔ File {name} uploaded successfully ✔")

    try:
        if selective_repeat: 
            client_socket.send_message(UPLOAD_FINISH_MSG.encode())
            client_socket.close_connection()
            stop_event.set()
            return 
        else:
            client_socket.sendto(UPLOAD_FINISH_MSG.encode(), addr)
    except TimeoutError:
        print("❌ Error: server did not respond to upload finish message ❌")


if __name__ == "__main__":
    args = parser.parse_arguments("upload")
    if not parser_utils.verify_params(args, "upload"):
        print("❌ Error: missing required argument(s) ❌")
        args.print_help()
    elif not (os.path.exists(args.src) and os.path.isfile(args.src)):
        print(f"❌ Error: file {args.src} does not exist ❌")
    else:
        main(args.name, args.src, (args.host, args.port), args.verbose)
