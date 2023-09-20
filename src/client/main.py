#!/usr/bin/env python3

import socket

from src.client import parser as ps
from src.lib.controllers.upload import upload_file
from src.lib.controllers.download import download_file


def verify_params(args):
    if not args.host or not args.port:
        return False
    if args.command == 'upload' and (not args.src or not args.name):
        return False
    if args.command == 'download' and (not args.dst or not args.name):
        return False
    return True


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

    if args.verbose:
        print(f'Successfully connected to {args.host}:{args.port}')

    if args.command == 'upload':
        print(f'Uploading {args.src} to {args.host}:{args.port} as {args.name}')
        upload_file(client_socket, args.src, args.name, args.verbose, False)

    elif args.command == 'download':
        print(f'Downloading {args.name} from {args.host}:{args.port} to {args.dst}')  ## TODO 
        download_file(client_socket, args.dst, args.name, args.verbose, False)

    client_socket.close()
    print("Bye! See you next time ;)")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nClient stopped by the user")
        print("Bye! See you next time ;)")
        exit(0)
