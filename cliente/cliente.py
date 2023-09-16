import parser as ps

import socket

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
    
    # if args.command == 'upload':
    #     print(f'Uploading {args.src} to {args.host}:{args.port} with name {args.name}')
        
    # elif args.command == 'download':
    #     print(f'Downloading {args.name} from {args.host}:{args.port} to {args.dst}')

    address = (f"{args.host}:{args.port}")
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
    except Exception as e: # TODO specify exception and handle it
        print(f'Error: {e}')
        return

    # send data to the server
    message = 'Hello, server!'
    client_socket.sendall(message.encode())
    
    # receive data from the server
    data = client_socket.recv(1024)
    print(f'Received data: {data.decode()}')

    # close the socket
    client_socket.close()

main()
