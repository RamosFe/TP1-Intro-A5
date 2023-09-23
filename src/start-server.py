import queue
import socket
from threading import Thread, Event
from typing import List
from src.rdt_stop_and_wait import RdtWSSocket

from src.lib.server.handler import handler
from src.lib.server.sending_handler import sender
from src.lib.constants import CHUNK_SIZE

HARDCODED_HOST = "127.0.0.1"
HARDCODED_PORT = 6000
HARDCODED_MOUNT_PATH = "./server_files/"


def main(host: str, port: int, max_chunk_size: int, mount_path: str):
    exit_signal_event = Event()

    server_socket = RdtWSSocket()

    server_socket.bind(host, port)

    print("-> Waiting connections")
    clients: List(Thread) = list()
    channels = dict()
    channel_to_sender = queue.Queue()    #form of data received: (data,addr) 

    sender_thread = Thread(
                    target=sender,
                    args= [channel_to_sender],
                )
    sender_thread.start()

    while True: 
        try:
            print("wipi")
            data, addr = server_socket.recv() 

            if addr not in channels.keys():
                # TODO establish handshake with addr

                channel_from_client = queue.Queue()    #threads reciven info de este channel
                channels[addr] = channel_from_client

                channel_from_client.put(data)
                
                new_client = Thread(
                    target=handler,
                    args=(channel_from_client, channel_to_sender, addr, max_chunk_size, mount_path, exit_signal_event),
                )
                clients.append(new_client)
                new_client.start()
            else:
                channel = channels[addr]
                channel.put(data)

        except KeyboardInterrupt:
            print("CTRL-C")
            exit_signal_event.set()

            for client in clients:
                client.join()
            server_socket.close()
            sender_thread.join()
            break
        except Exception as e:
            print(f"2😨 An exception has occurred, please try again -> {e}😨")
            exit_signal_event.set()

            for client in clients:
                client.join()
            server_socket.close()
            sender_thread.join()
            break


if __name__ == "__main__":
    main(HARDCODED_HOST, HARDCODED_PORT, CHUNK_SIZE, HARDCODED_MOUNT_PATH)
