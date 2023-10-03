import os
from threading import Event
from lib.rdt.rdt_sw_socket import RdtSWSocketClient

from lib.constants import LIST_FILES_FINISH


class FileSystemLister:
    """
    A class for listing files in a specified directory and sending the list 
    over a network socket.
    """

    def __init__(self, mount_path: str):
        """
        Initialize the FileSystemLister with a specified mount path.

        Args:
            mount_path (str): The path to the directory whose files 
            will be listed.
        """
        self._mount_path = mount_path

    def list_files(self, channel, socket: RdtSWSocketClient, addr,
                   exit_signal: Event):
        """
        List the files in the specified directory and send the list over a
        network socket.

        Args:
            channel: The communication channel for sending data.
            socket (RdtSWSocketClient): The socket object for sending data.
            addr: The address to which data will be sent.
            exit_signal (Event): An event that can be used to signal the
            exit of the file listing process.
        """
        try:
            entries = "\n".join(os.listdir(self._mount_path))
            while not exit_signal.is_set():
                # Send the entries
                socket.sendto_with_queue(entries.encode(), addr, channel)

                # Send a finish signal to indicate the end of the list
                socket.sendto_with_queue(LIST_FILES_FINISH, addr, channel)

                # Break out of the loop after sending the entries once
                break
        except Exception as e:
            raise e
