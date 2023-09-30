

def verify_params(args, command: str):
    """
    Verify that the required parameters for the specified command are provided.

    Args:
        args (argparse.Namespace): Parsed command line arguments.
        command (str): The command to verify parameters for.

    Returns:
        bool: True if all required parameters are provided, False otherwise.
    """
    if not args.host or not args.port:
        return False
    if command == "upload" and (not args.src or not args.name):
        return False
    if command == "download" and (not args.dst or not args.name):
        return False
    return True
