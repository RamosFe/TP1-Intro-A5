import argparse


def parse_arguments(command):
    """
    Parse command line arguments based on the given command.

    Args:
        command (str): The command to determine the argument parsing logic.

    Returns:
        argparse.Namespace: An object containing the parsed command line arguments.
    """
    parser = None
    if command == "upload":
        parser = parse_arguments_upload()
    elif command == "download":
        parser = parse_arguments_download()
    else: 
        parser = parse_arguments_ls()
    args = parser.parse_args()
    
    return args


def parse_arguments_upload():
    """
    Parse command line arguments for the "upload" command.

    Returns:
        argparse.ArgumentParser: An ArgumentParser object configured for "upload" command arguments.
    """
    parser = argparse.ArgumentParser(description="Upload")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="increase output verbosity"
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="decrease output verbosity"
    )
    parser.add_argument("-H", "--host", type=str, help="server IP address")
    parser.add_argument("-p", "--port", type=int, help="server port")
    parser.add_argument("-s", "--src", type=str, help="source file path")
    parser.add_argument("-n", "--name", type=str, help="file name")
    return parser


def parse_arguments_ls():
    parser = argparse.ArgumentParser(description="ls")
    parser.add_argument("-H", "--host", type=str, help="server IP address")
    parser.add_argument("-p", "--port", type=int, help="server port")
    return parser


def parse_arguments_download():
    """
    Parse command line arguments for the "download" command.

    Returns:
        argparse.ArgumentParser: An ArgumentParser object configured for "download" command arguments.
    """
    parser = argparse.ArgumentParser(description="Download")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="increase output verbosity"
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="decrease output verbosity"
    )
    parser.add_argument("-H", "--host", type=str, help="server IP address")
    parser.add_argument("-p", "--port", type=int, help="server port")
    parser.add_argument("-d", "--dst", type=str, help="destination file path")
    parser.add_argument("-n", "--name", type=str, help="file name")
    return parser
