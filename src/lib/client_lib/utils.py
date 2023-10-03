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


def poll_socket(
    sock: socket.socket, data_queue, event, stop_rdt_event: threading.Event
):
    """
    Polls a socket for incoming data and puts it in a queue.

    Args:
        sock (socket.socket): The socket to poll.
        data_queue (Queue): A queue to store the received data.
        event (threading.Event): An event for synchronization.
        stop_rdt_event (threading.Event): An event to signal stopping 
        the process from another thread.

    Returns:
        None
    """
    # Create an instance of TimeOutErrors
    time_out_errors = TimeOutErrors()

    # Set socket timeout to a hardcoded value
    sock.settimeout(HARDCODED_TIMEOUT)

    # Continue polling until max_tries_exceeded or event is set
    while not time_out_errors.max_tries_exceeded():

        # Check if event of sinchronization is set or stop_rdt_event is set
        if event.is_set() or stop_rdt_event.is_set():
            sock.settimeout(None)
            break
        try:
            # Receive data from the socket
            data, _ = sock.recvfrom(HARDCODED_BUFFER_SIZE_SR)

            # Put received data into the queue for later process
            data_queue.put(data)

            # Reset the number of tries as data was received successfully
            time_out_errors.reset_tries()
        except TimeoutError:
            # Handle timeout error
            time_out_errors.increase_try()
            continue

    # If max_tries_exceeded, set events to signal stopping
    if time_out_errors.max_tries_exceeded():
        stop_rdt_event.set()
        event.set()
