import os
import socket
from threading import Event

import threading
import queue
from lib.sr_rdt.selective_repeat import SelectiveRepeatRDT
from lib.fs.fs_downloader_client import FileSystemDownloaderClient
from lib.client_lib import parser, utils as parser_utils
from lib.constants import HARDCODED_CHUNK_SIZE, HARDCODED_BUFFER_SIZE_SR, HARDCODED_TIMEOUT,WINDOW_SIZE
from lib.commands import Command, CommandResponse, MessageOption
from lib.handshake import ThreeWayHandShake

from lib.rdt.rdt_sw_socket import RdtSWSocket, RdtSWSocketClient, TimeOutErrors


def main():
    """
    Entry point of the download client application.

    This function parses command-line arguments, verifies them, and initiates the file download process.

    Returns:
        None
    """
    try:
            
        args = parser.parse_arguments("download")
        
        selective_repeat = args.selective_repeat
        if not parser_utils.verify_params(args, "download"):
            print("❌ Error: missing required argument(s) ❌")
            args.print_help()
            return

        if os.path.exists(args.dst) and os.path.isdir(args.dst):
            print(f"❌ Error: {args.dst} is a directory ❌")
            return

        try:
            if selective_repeat:
                event = Event()
                server_addr = ("127.0.0.1", 6000)
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                data_queue = queue.Queue()  
                protocol = SelectiveRepeatRDT(WINDOW_SIZE, data_queue,sock, server_addr)
                threading.Thread(target=parser_utils.poll_socket, args=(sock, data_queue,event,protocol.get_event())).start()
                
                print(f"💾 📥 Downloading {args.name} from {args.host}:{args.port} to {args.dst}")
                download_file(None, protocol, args.dst, args.name, args.verbose, args.host, args.port,event)
                protocol.close_connection()
            else:
                client_socket = RdtSWSocketClient()
                print(f"💾 📥 Downloading {args.name} from {args.host}:{args.port} to {args.dst}")
                download_file(client_socket,None, args.dst, args.name, args.verbose, args.host, args.port,None)
                client_socket.close()
        except TimeoutError:
            close_connections(client_socket,protocol,event)
            print("❌ Connection Timeout Error ❌")
            return

        print("Bye! See you next time 😉")
        quit()
    except KeyboardInterrupt:
        print("Ctrl c, Bye! See you next time 😉")
        quit()



def download_file(socketSW: RdtSWSocketClient,socketSR, dest: str, name: str, verbose: bool, host: str, port: int, event):
    """
    Download a file from a server using a UDP socket connection.

    Args:
        connection (socket.socket): The socket connection to the server.
        dest (str): The destination path where the file will be saved.
        name (str): The name of the file to be downloaded.
        verbose (bool): Whether to print verbose output.
        host (str): The hostname or IP address of the server.
        port (int): The port number for the server.

    Returns:
        None
    """
    fs_handler = FileSystemDownloaderClient("./", HARDCODED_CHUNK_SIZE)
    if fs_handler.file_exists(filename=name):
        print(f"❌ File {name} already exists ❌")
        return

    command = Command(MessageOption.DOWNLOAD, name, 0)
    try: 
        if socketSW is not None:
            three_way_handshake = ThreeWayHandShake(socketSW)
            response = three_way_handshake.send_download(command.to_str(),(host,port),True).decode()
        else:
            socketSR.send_message(command.to_str().encode())
            response = socketSR.receive_message().decode()
    except TimeoutError:
        print("❌ Request not answered ❌")
        return

    if verbose:
        print(f"-> Sending request to server to download file {name}")

    command = CommandResponse(response)
    print("-> Server response: ", response)
    if command.is_error():
        print(f"❌ Request rejected -> {command._msg} ❌") 
        quit()

    if verbose:
        print("✔ Request accepted ✔")

    size = command.size()

    user_input = input(f"Download file {name} with size {size} bytes? [y/n]: ")
    if user_input.lower() not in ("y", "yes"):
        print("❌ Download canceled ❌")
        response = CommandResponse.err_response("ERR Download canceled").to_str()
        if socketSW is not None:
            socketSW._internal_socket.sendto(response.encode(), (host, port)) 
        else:
            socketSR.send_message(response.encode())
        return

    response = CommandResponse.ok_response().to_str()
    if socketSW is not None:

        try:
            first_data,addr = three_way_handshake.send_download(response,(host,port),False)

        except TimeoutError:
            print("❌ Connection lost due to multiple tries ❌")
            return 
    else:
        socketSR.send_message(response.encode())
    if verbose:
        print(f"-> Downloading file {name} with name {dest}")

    try:

        if socketSW is not None:
            fs_handler.download_file(socketSW,socketSR, dest, size, Event(),first_data,addr)
        else:
            fs_handler.download_file(socketSW,socketSR, dest, size, Event(), None, None)
    except TimeoutError:
        print("❌ Connection lost due to multiple tries ❌")
        return


    if verbose:
        print(f"✔ File {name} downloaded successfully ✔")



def close_connections(socketSW: RdtSWSocketClient,socketSR,event):
    if socketSW is not None:
        socketSW.close()
    else:
        event.set()
        socketSR.close_connection()


if __name__ == "__main__":
    main()
