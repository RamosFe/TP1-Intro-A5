import os
import socket
from lib.fs.fs_list_files import FileSystemLister
from lib.rdt.rdt_sw_socket import RdtSWSocketClient
from threading import Event




def list_files_server(channel,connection: RdtSWSocketClient,addr: str,  mount_path: str, exit_signal : Event):
    fs_handler = FileSystemLister(mount_path)
    fs_handler.list_files(channel,connection, addr,  exit_signal)
    