import os
from threading import Event
from lib.rdt.rdt_sw_socket import RdtSWSocketClient 

from lib.constants import LIST_FILES_FINISH


class FileSystemLister:
    def __init__(self,mount_path: str):
        self._mount_path = mount_path

    def list_files(self, channel,socket: RdtSWSocketClient,addr,exit_signal: Event):
        try:
            entries = '\n'.join(os.listdir(self._mount_path))
            while not exit_signal.is_set():
                socket.sendto_with_queue(entries.encode(),addr,channel)
                socket.sendto_with_queue(LIST_FILES_FINISH,addr,channel)
                break
        
        except Exception as e:
            print(f'Error: {e}')
            raise e
