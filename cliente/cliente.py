
import argparse

SERVER_PORT = 3030
help_command_source = "help_command.txt"


# def help_command(args):
#     with open('help_command_source', 'r') as file:
#         print(file.read())



def parse_arguments():
    parser = argparse.ArgumentParser(description='<command description>')
    subparsers = parser.add_subparsers(dest='command')

    upload_parser = subparsers.add_parser('upload')

    upload_parser.add_argument('-h', '--help', action='help', help='show this help message and exit')
    upload_parser.add_argument('-v', '--verbose', action='store_true', help='increase output verbosity')
    upload_parser.add_argument('-q', '--quiet', action='store_true', help='decrease output verbosity')
    upload_parser.add_argument('-H', '--host', type=str, help='server IP address')
    upload_parser.add_argument('-p', '--port', type=int, help='server port')
    upload_parser.add_argument('-s', '--src', type=str, help='source file path')
    upload_parser.add_argument('-n', '--name', type=str, help='file name')

    download_parser = subparsers.add_parser('download')
    download_parser.add_argument('-h', '--help', action='help', help='show this help message and exit')
    download_parser.add_argument('-v', '--verbose', action='store_true', help='increase output verbosity')
    download_parser.add_argument('-q', '--quiet', action='store_true', help='decrease output verbosity')
    download_parser.add_argument('-H', '--host', type=str, help='server IP address')
    download_parser.add_argument('-p', '--port', type=int, help='server port')
    download_parser.add_argument('-d', '--dst', type=str, help='destination file path')
    download_parser.add_argument('-n', '--name', type=str, help='file name')

    args = parser.parse_args()
    return args


#########

def main():
    args = parse_arguments()
    if args.command == 'upload':
        if not args.host or not args.port or not args.src or not args.name:
            print('Error: missing required argument(s)')
            parse_arguments().print_help()
            return

        # Handle upload command
        print(f'Uploading {args.src} to {args.host}:{args.port} with name {args.name}')
        
    elif args.command == 'download':
        if not args.host or not args.port or not args.dst or not args.name:
            print('Error: missing required argument(s)')
            parse_arguments().print_help()
            return

        # Handle download command
        print(f'Downloading {args.name} from {args.host}:{args.port} to {args.dst}')
    
    if args.help:
        parse_arguments().print_help()

main()
