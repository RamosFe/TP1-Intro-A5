import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="Start server")
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="increase output verbosity"
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="decrease output verbosity"
    )
    parser.add_argument("-H", "--host", type=str, help="service IP address")
    parser.add_argument("-p", "--port", type=int, help="service port")
    parser.add_argument("-s", "--storage", type=str,
                        help="storage directory path")
    parser.add_argument(
        "-r", "--selective_repeat", action="store_true",
        help="selective repeat"
    )
    return parser.parse_args()
