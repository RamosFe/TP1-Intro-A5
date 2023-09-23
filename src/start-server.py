import os
import socket
from threading import Thread, Event
from typing import List

from src.lib.server.handler import handler
from src.lib.constants import CHUNK_SIZE
from src.lib.server import parser as ps


def main(host: str, port: int, max_chunk_size: int, mount_path: str):
    exit_signal_event = Event()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((host, port))
    server_socket.listen()

    print("-> Waiting connections")
    clients: List[Thread] = []
    while True:
        try:
            conn, addr = server_socket.accept()
            new_client = Thread(target=handler, args=(conn, addr, max_chunk_size, mount_path, exit_signal_event))
            clients.append(new_client)
            new_client.start()
        except KeyboardInterrupt:
            print("CTRL-C")
            exit_signal_event.set()

            for client in clients:
                client.join()
            server_socket.close()
            break
        except Exception as e:
            print('😨 An exception occurred, sorry 😨')
            exit_signal_event.set()

            for client in clients:
                client.join()
            server_socket.close()
            break


if __name__ == '__main__':
    args = ps.parse_arguments()
    if not args.host or not args.port or not args.storage:
        print('❌ Error: missing required argument(s) ❌')
        args.print_help()
        exit(1)
    if not os.path.exists(args.storage) or not os.path.isdir(args.storage):
        print(f'❌ Error: {args.storage} is not a directory ❌')
        exit(1)
    main(args.host, args.port, CHUNK_SIZE, args.storage)
