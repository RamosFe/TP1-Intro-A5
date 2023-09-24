from threading import Thread, Event
from typing import List, Dict, Tuple
import queue
import socket

from lib.constants import (
    HARDCODED_HOST,
    HARDCODED_PORT,
    HARDCODED_BUFFER_SIZE,
    HARDCODED_TIMEOUT,
)


def handler(channel: queue.Queue, addr: tuple[str, int], exit_signal: Event):
    while not exit_signal.is_set():
        try:
            data = channel.get(block=True, timeout=HARDCODED_TIMEOUT).decode()

            socket_to_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print(f"Data from {addr} received correctly {data}")
            socket_to_client.sendto("Recibido".encode(), addr)

        except queue.Empty as e:
            if exit_signal.is_set():
                print("Closing server due to signal")
                return
            else:
                raise e


def main(host, port):
    exit_signal_event = Event()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    # State variables
    clients: List[Thread] = list()
    channels: Dict[Tuple[str, int], queue.Queue] = dict()

    # Main loop
    while True:
        try:
            data, addr = server_socket.recvfrom(HARDCODED_BUFFER_SIZE)

            # If it is a new client
            if addr not in channels:
                # Creates the channel for the new client
                client_channel = queue.Queue()
                channels[addr] = client_channel

                # Sends data to the new client
                client_channel.put(data)

                new_client = Thread(
                    target=handler, args=(client_channel, addr, exit_signal_event)
                )
                clients.append(new_client)
                new_client.start()
            else:
                # Send to the respective thread
                channels[addr].put(data)

        except KeyboardInterrupt:
            print("\nClosing server")
            close_server(exit_signal_event, clients, server_socket)
            break

        except Exception as e:
            print(f"😨 An exception has occurred, please try again -> {e}😨")
            close_server(exit_signal_event, clients, server_socket)
            break


def close_server(
    exit_signal_event: Event, clients: List[Thread], server_socket: socket.socket
):
    exit_signal_event.set()
    for client in clients:
        client.join()
    server_socket.close()


if __name__ == "__main__":
    main(HARDCODED_HOST, HARDCODED_PORT)
