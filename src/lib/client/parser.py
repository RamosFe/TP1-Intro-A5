import argparse


def parse_arguments(command):
    parser = None
    if command == 'upload':
        parser = parse_arguments_upload()
    else:
        parser = parse_arguments_download()
    return parser.parse_args()

def parse_arguments_upload():
    parser = argparse.ArgumentParser(description='Upload')
    parser.add_argument('-v', '--verbose', action='store_true', help='increase output verbosity')
    parser.add_argument('-q', '--quiet', action='store_true', help='decrease output verbosity')
    parser.add_argument('-H', '--host', type=str, help='server IP address')
    parser.add_argument('-p', '--port', type=int, help='server port')
    parser.add_argument('-s', '--src', type=str, help='source file path')
    parser.add_argument('-n', '--name', type=str, help='file name')
    return parser

def parse_arguments_download():
    parser = argparse.ArgumentParser(description='Download')
    parser.add_argument('-v', '--verbose', action='store_true', help='increase output verbosity')
    parser.add_argument('-q', '--quiet', action='store_true', help='decrease output verbosity')
    parser.add_argument('-H', '--host', type=str, help='server IP address')
    parser.add_argument('-p', '--port', type=int, help='server port')
    parser.add_argument('-d', '--dst', type=str, help='destination file path')
    parser.add_argument('-n', '--name', type=str, help='file name')
    return parser

