

import socket
import threading
from lib.constants import HARDCODED_BUFFER_SIZE_SR, HARDCODED_TIMEOUT

from lib.rdt.rdt_sw_socket import TimeOutErrors


def verify_params(args, command: str):
    """
    Verify that the required parameters for the specified command are provided.

    Args:
        args (argparse.Namespace): Parsed command line arguments.
        command (str): The command to verify parameters for.

    Returns:
        bool: True if all required parameters are provided, False otherwise.
    """
    if not args.host or not args.port:
        return False
    if command == "upload" and (not args.src or not args.name):
        return False
    if command == "download" and (not args.dst or not args.name):
        return False
    return True




def poll_socket(sock: socket.socket, data_queue,event,stop_rdt_event: threading.Event):

    time_out_errors = TimeOutErrors()
    sock.settimeout(HARDCODED_TIMEOUT)
    while not time_out_errors.max_tries_exceeded():
        if event.is_set() or stop_rdt_event.is_set():
            print("--DEBUG-- stoping poll socket")
            sock.settimeout(None)
            break
        try:        
            # print("--DEBUG-- waiting for response")
            data,_ = sock.recvfrom(HARDCODED_BUFFER_SIZE_SR)  
            # print("--DEBUG-- data received: ", data)              
            data_queue.put(data)
            time_out_errors.reset_tries()
        except TimeoutError:
            time_out_errors.increase_try()
            continue
    
    if time_out_errors.max_tries_exceeded():
        print("setting event!!!")
        stop_rdt_event.set()
        event.set()

