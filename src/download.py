from src.lib.client import parser as ps
from src.lib.client import utils as ut
import os

def main():
    args = ps.parse_arguments('download')

    if not ut.verify_params(args, 'download'):
        print('❌ Error: missing required argument(s) ❌')
        args.print_help()
        return
    
    if os.path.exists(args.dst) and os.path.isdir(args.dst):
        print(f'❌ Error: {args.dst} is a directory ❌')
        return

    client_socket = ut.connect(args)
    if client_socket is None:
        return
    
    print(f'💾 📥 Downloading {args.name} from {args.host}:{args.port} to {args.dst}')  ## TODO 
    ut.download_file(client_socket, args.dst, args.name, args.verbose)
    
    client_socket.close()
    print("Bye! See you next time 😉")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nClient stopped by the user")
        print("Bye! See you next time 😉")
        exit(0)
    except Exception as e:
        print(f'😨 An exception occurred, please try again 😨')
        exit(1)