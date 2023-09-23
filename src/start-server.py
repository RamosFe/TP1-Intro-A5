import os
import socket
from threading import Thread, Event
from typing import List

from src.lib.server.handler import handler
from src.lib.constants import CHUNK_SIZE
from src.lib.server import parser as ps

def close_server(exit_event: Event, server_socket: socket.socket, clients: List[Thread]):
    exit_event.set()
    [client.join() for client in clients]
    server_socket.close()

def main():
    args = ps.parse_arguments()
    if not args.host or not args.port or not args.storage:
        print('❌ Error: missing required argument(s) ❌')
        args.print_help()
        exit(1)
    if not os.path.exists(args.storage) or not os.path.isdir(args.storage):
        print(f'❌ Error: {args.storage} is not a directory ❌')
        exit(1)

    exit_signal_event = Event()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((args.host, args.port))
    server_socket.listen()

    print("Waiting connections")
    clients: List[Thread] = []
    while True:
        try:
            conn, addr = server_socket.accept()
            new_client = Thread(target=handler, args=(conn, addr, CHUNK_SIZE, args.storage, exit_signal_event, args.verbose))
            clients.append(new_client)
            new_client.start()
        except KeyboardInterrupt:
            print("\nServer stopped by the user, exiting...")
            close_server(exit_signal_event, server_socket, clients)
            print("Server closed, bye 👋")
            break
        except Exception as e:
            print('😨 An exception occurred, sorry 😨')
            close_server(exit_signal_event, server_socket, clients)
            break


if __name__ == '__main__':
    main()
