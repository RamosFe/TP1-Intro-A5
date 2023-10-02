import queue
import socket
from threading import Thread, Event
from typing import List, Dict, Tuple
from lib.sr_rdt.selective_repeat import SelectiveRepeatRDT
from lib.server_lib.downloader import download_file
from lib.server_lib.uploader import upload_file
from lib.commands import Command, MessageOption
from lib.constants import (
    HARDCODED_HOST,
    HARDCODED_PORT,
    HARDCODED_BUFFER_SIZE,
    HARDCODED_TIMEOUT,
    HARDCODED_MOUNT_PATH,
)
WINDOW_SIZE = 50
from lib.rdt.rdt_sw_socket import RdtSWSocket, RdtSWSocketClient
from lib.rdt.socket_interface import SocketInterface


def handler(channel: queue.Queue, addr, exit_signal: Event, protocol):
    """
    Handles incoming messages from clients and delegates the appropriate action.

    Args:
        channel (queue.Queue): A queue for receiving messages from the client.
        addr (Tuple[str, int]): A tuple containing the client's address (hostname or IP) and port.
        exit_signal (Event): An event signaling the termination of the handler.

    Returns:
        None
    """    
    #socket_to_client = RdtSWSocketClient()
    while not exit_signal.is_set(): # TODO Si nos da error lo borramos        
        #data = channel.get(block=True)
        data = protocol.receive_message()        
        data = data.decode()
        command = Command.from_str(data)
        if command.option == MessageOption.UPLOAD:
            return download_file(
                channel,
                None,
                addr,
                protocol,
                HARDCODED_MOUNT_PATH,
                exit_signal,
                command,
            )
        elif command.option == MessageOption.DOWNLOAD:
            return upload_file(
                channel,
                None,
                addr,
                protocol,
                HARDCODED_MOUNT_PATH,
                exit_signal,
                command,
            )

def main(host, port):
    """
    Main function to start the server and handle incoming client requests.

    Args:
        host (str): The hostname or IP address the server should bind to.
        port (int): The port number the server should listen on.

    Returns:
        None
    """
    exit_signal_event = Event()

    # server_socket = RdtSWSocketClient()
    # server_socket.bind((host, port))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 6000))  
      

    # State variables
    clients: List[Thread] = list()
    channels: Dict[Tuple[str, int], queue.Queue] = dict()

    # Main loop
    while True:
        # try:
            # data, addr = server_socket._internal_socket.recvfrom(HARDCODED_BUFFER_SIZE)
            data, addr = sock.recvfrom(HARDCODED_BUFFER_SIZE)            
            # If it is a new client
            if addr not in channels:
                # Creates the channel for the new client
                client_channel = queue.Queue()
                channels[addr] = client_channel
                protocol = SelectiveRepeatRDT(WINDOW_SIZE, client_channel,sock, addr)
                # Sends data to the new client
                
                client_channel.put(data)
                new_client = Thread(
                    target=handler, args=(client_channel, addr, exit_signal_event,protocol)
                )
                clients.append(new_client)
                new_client.start()                
            else:
                # Send to the respective thread
                channels[addr].put(data)
                # print(f" data del channel: {channels[addr].get()}")

        # except KeyboardInterrupt:
        #     print("\nClosing server")
        #     close_server(exit_signal_event, clients, sock)
        #     break

        # except Exception as e:
        #     print(f"😨 An exception has occurred, please try again -> {e}😨")
        #     close_server(exit_signal_event, clients, sock)
        #     break


def close_server(
    exit_signal_event: Event, clients: List[Thread], server_socket
):
    """
    Closes the server gracefully.

    Args:
        exit_signal_event (Event): An event to signal the termination of the handler threads.
        clients (List[Thread]): A list of active client handler threads.
        server_socket (socket.socket): The server socket to close.

    Returns:
        None
    """
    exit_signal_event.set()
    for client in clients:
        client.join()
    server_socket.close()


if __name__ == "__main__":
    main(HARDCODED_HOST, HARDCODED_PORT)