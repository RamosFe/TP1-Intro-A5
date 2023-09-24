from threading import Thread, Event
from typing import List, Dict, Tuple
from lib.server.downloader import download_file
from lib.server.uploader import upload_file
from lib.commands import Command, MessageOption
import queue
import socket

from lib.constants import (
    HARDCODED_HOST,
    HARDCODED_PORT,
    HARDCODED_BUFFER_SIZE,
    HARDCODED_TIMEOUT,
    HARDCODED_MOUNT_PATH,
)


def handler(channel: queue.Queue, addr: tuple[str, int], exit_signal: Event):
    socket_to_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not exit_signal.is_set():
        data = channel.get(block=True, timeout=HARDCODED_TIMEOUT).decode()
        command = Command.from_str(data)
        if command.option == MessageOption.UPLOAD:
            return download_file(
                channel,
                socket_to_client,
                addr,
                HARDCODED_MOUNT_PATH,
                exit_signal,
                command,
            )
        elif command.option == MessageOption.DOWNLOAD:
            return upload_file(
                channel,
                socket_to_client,
                addr,
                HARDCODED_MOUNT_PATH,
                exit_signal,
                command,
            )
        # except Exception as e:


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
