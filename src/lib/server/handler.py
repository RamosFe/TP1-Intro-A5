import socket
from threading import Event
from src.rdt_stop_and_wait import RdtWSSocket
from src.lib.commands import Command, CommandResponse, MessageOption
from src.lib.server.download import download_file
from src.lib.server.upload import upload_file
from src.lib.fs.fs_downloader import FileSystemDownloader
from queue import Queue

# channel, channel_receive, addr, mount_path, exit_signal_event
def handler(channel_from_client: Queue,channel_to_sender : Queue ,addr: str, max_chunk_size: int, mount_path: str, exit_signal: Event):
    # try :
        print("handler")
        data = channel_from_client.get()[0].replace('\x00', '') # TODO ver si hay que arreglarlo por otro lado
        print(data)
        command = Command.from_str(data)
        if command.option == MessageOption.UPLOAD:
            return download_file(channel_from_client, channel_to_sender, addr, max_chunk_size, mount_path, exit_signal,command)        
        elif command.option == MessageOption.DOWNLOAD:
            return upload_file(channel_from_client, channel_to_sender, addr, max_chunk_size, mount_path, exit_signal,command)
    # except Exception as e:
    #     print("sos una verga aprende a programar")
