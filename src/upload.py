from src.lib.client import parser as ps
from src.lib.client import utils as ut
import os


def main():
    args = ps.parse_arguments("upload")

    if not ut.verify_params(args, "upload"):
        print("❌ Error: missing required argument(s) ❌")
        args.print_help()
        return

    if not (os.path.exists(args.src) and os.path.isfile(args.src)):
        print(f"❌ Error: file {args.src} does not exists ❌")
        return

    client_socket = ut.connect(args)
    if client_socket is None:
        return

    print(f"☁️ 📤 Uploading {args.src} to {args.host}:{args.port} as {args.name}")
    ut.upload_file(client_socket, args.src, args.name, args.verbose)

    client_socket.close()
    print("Bye! See you next time 😉")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nClient stopped by the user")
        print("Bye! See you next time 😉")
        exit(0)
    except Exception as e:
        print(f"3 😨 An exception has occurred, please try again -> {e}😨")
        exit(1)
