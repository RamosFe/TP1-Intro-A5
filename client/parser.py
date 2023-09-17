import argparse

def parse_arguments():
    
    parser = argparse.ArgumentParser(description='FileTransfer')
    subparsers = parser.add_subparsers(dest='command')

    upload_parser = subparsers.add_parser('upload')
    upload_parser.add_argument('-v', '--verbose', action='store_true', help='increase output verbosity')
    upload_parser.add_argument('-q', '--quiet', action='store_true', help='decrease output verbosity')
    upload_parser.add_argument('-H','--host', type=str, help='server IP address')
    upload_parser.add_argument('-p', '--port', type=int, help='server port')
    upload_parser.add_argument('-s','--src', type=str, help='source file path')
    upload_parser.add_argument('-n', '--name', type=str, help='file name')

    download_parser = subparsers.add_parser('download')
    download_parser.add_argument('-v', '--verbose', action='store_true', help='increase output verbosity')
    download_parser.add_argument('-q', '--quiet', action='store_true', help='decrease output verbosity')
    download_parser.add_argument('-H','--host', type=str, help='server IP address')
    download_parser.add_argument('-p', '--port', type=int, help='server port')
    download_parser.add_argument('-d','--dst', type=str, help='destination file path')
    download_parser.add_argument('-n', '--name', type=str, help='file name')

    # TODO complete a gral help message abou the client

    args = parser.parse_args()

    # if args.help:
    #     parser.print_help()
    #     quit()

    return args
