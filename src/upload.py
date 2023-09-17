#!/usr/bin/env python3

import os
import socket
from src.lib import parser as ps
from lib.constants import BUFFER_SIZE, CHUNK_SIZE


def verify_params(args):
    if not args.host or not args.port:
        return False
    if args.command == 'upload' and (not args.src or not args.name):
        return False
    if args.command == 'download' and (not args.dst or not args.name):
        return False
    return True


def upload_file(socket, path, name):
    try:
        with open(path, 'rb') as file:
            file_size = os.path.getsize(path)
            socket.send(
                f'UPLOAD {name} {file_size}'.encode())  # TODO check on server side if another file has the same name, also check if the file doesn't has more than the max size
            print(f'Uploading {name} ({file_size} bytes)')

            response = socket.recv(BUFFER_SIZE).decode()
            if response != 'OK':
                print(f'Error: {response}')
                return
            print('Server ready to receive file')

            for chunk in iter(lambda: file.read(CHUNK_SIZE), b''):
                # input('Press enter to send the next chunk')
                socket.send(chunk)
            print('File sent')

            socket.send(b'UPLOAD EOF')
            print('EOF sent')

    except FileNotFoundError:
        print(f'File not found: {path}')
        return
    except Exception as e:  # TODO specify exception and handle it
        print(f'Error: {e}')
        return


# def download_file(socket, path, name):

#     try :
#         socket.send(f'DOWNLOAD {name}'.encode())
#         response = socket.recv(cte.BUFFER_SIZE).decode()
#         # TODO Chequear el file size/ error posible que nos podrian tirar


#     except Exception as e:
#         print(f"Error: {e}")
#         return
#     #servidor filesize

def main():
    args = ps.parse_arguments()

    if not verify_params(args):
        print('Error: missing required argument(s)')
        ps.parse_arguments().print_help()
        return

    address = (args.host, args.port)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect(address)
    except ConnectionRefusedError:
        print("Connection refused. Make sure the server is running.")
        return
    except TimeoutError:
        print("Connection timed out. Check the host and port.")
        return
    except BrokenPipeError:
        print("Connection closed. Reconnect and try again.")
        return
    except Exception as e:  # TODO specify exception and handle it
        print(f'Error: {e}')
        return

    if args.command == 'upload':
        print(f'Uploading {args.src} to {args.host}:{args.port} as {args.name}')
        upload_file(client_socket, args.src, args.name)

    elif args.command == 'download':
        print(f'Downloading {args.name} from {args.host}:{args.port} to {args.dst}')

    client_socket.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nClient stopped by the user")
        print("Bye! See you next time ;)")
        exit(0)
