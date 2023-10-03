import queue
from lib import commands
from lib.commands import CommandResponse
from lib.rdt.rdt_sw_socket import TimeOutErrors

from lib.rdt.rdt_sw_socket import RdtSWSocketClient
from lib.constants import HARDCODED_BUFFER_SIZE, HARDCODED_MAX_TIMEOUT_TRIES, HARDCODED_TIMEOUT, HARDCODED_TIMEOUT_FOR_RECEIVING_INPUT

class ThreeWayHandShake:

    def __init__(self, socket: RdtSWSocketClient):
        """
        Initialize a ThreeWayHandShake instance.

        Args:
            socket (RdtSWSocketClient): The socket object for communication.
        """
        self.socket = socket  # Store the socket object
        self.time_out_errors = TimeOutErrors()  # Initialize timeout error handling

    def send(self, response, addr):
        """
        Send a message and receive a response.

        Args:
            response (str): The message to send.
            addr: The address to send to.

        Returns:
            str: The response received.
        """
        # Set timeout for socket operations
        self.socket.set_timeout(self.time_out_errors.get_timeout())

        while not self.time_out_errors.max_tries_exceeded():
            try:
                self.socket.send_with_internal_socket(response.encode(), addr)  # Send the message

                # Receive the response from the client
                response, addr = self.socket.recv_with_internal_socket(HARDCODED_BUFFER_SIZE)
                return response  # Return the response
            
            except TimeoutError:
                self.time_out_errors.increase_try()  # Handle timeout error
                continue
        raise TimeoutError  # Raise a timeout error if max tries are exceeded

    def send_with_queue_upload(self, data: CommandResponse, addr, channel: queue):
        """
        Send a message with a queue for upload operations.

        Args:
            data (CommandResponse): The data to send.
            addr: The address to send to.
            channel (queue): The queue for handling responses.

        Returns:
            str: The response received.
        """
        self.socket.send_with_internal_socket(data.encode(), addr)  # Send the data

        while not self.time_out_errors.max_tries_exceeded():
            if self.time_out_errors.get_tries() == HARDCODED_MAX_TIMEOUT_TRIES - 1:
                response, addr = channel.get(block=True, timeout=HARDCODED_TIMEOUT_FOR_RECEIVING_INPUT)
            else:
                response, addr = channel.get(block=True)
            if self.is_not_ok(response.decode()):
                self.socket.send_with_internal_socket(data.encode(), addr)  # Resend the data
                self.time_out_errors.increase_try()  # Increase the try count
            else:
                return response  # Return the response

    def is_not_ok(self, data):
        """
        Check if the response is not 'OK'.

        Args:
            data (str): The response.

        Returns:
            bool: True if the response is not 'OK', False otherwise.
        """
        return data != "OK" and data != "ERR Download canceled"

    def send_download(self, data: CommandResponse, addr, first_handshake: bool):
        """
        Send download command.

        Args:
            data (CommandResponse): The command to send.
            addr: The address to send to.
            first_handshake (bool): Flag indicating the first handshake.

        Returns:
            tuple: The response and address.
        """
        self.socket.send_with_internal_socket(data.encode(), addr)  # Send the command
        self.socket.set_timeout(HARDCODED_TIMEOUT)
        while not self.time_out_errors.max_tries_exceeded():
            try:
                response, addr = self.socket.recv_with_internal_socket(HARDCODED_BUFFER_SIZE)
                try:
                    decoded_response = response.decode()  # Decode the response
                    if first_handshake:
                        return response  # Return response for the first handshake
                    if self.data_is_command(decoded_response):
                        self.socket.send_with_internal_socket(data.encode(), addr)  # Resend the command
                        self.time_out_errors.increase_try()  # Increase the try count
                        continue
                    return response.encode(), addr  # Return response and address
                
                except Exception:
                    return response, addr  # Return response and address

            except TimeoutError:
                self.time_out_errors.increase_try()  # Increase the try count
                self.socket.send_with_internal_socket(data.encode(), addr)  # Resend the command
                continue
        raise TimeoutError  # Raise a timeout error if max tries are exceeded

    def send_with_queue(self, response: CommandResponse, addr, channel: queue):
        """
        Send a response with a queue.

        Args:
            response (CommandResponse): The response to send.
            addr: The address to send to.
            channel (queue): The queue for handling responses.

        Returns:
            None
        """
        self.socket.set_timeout(HARDCODED_TIMEOUT)

        # Until there are no more tries left
        while not self.time_out_errors.max_tries_exceeded():
            try:
                self.socket.send_with_internal_socket(response.encode(), addr)  # Send the response
                while self.time_out_errors.time_to_receive_data():
                    if not channel.empty():
                        data, addr = channel.get()
                        try:
                            if self.data_is_command(data.decode()):
                                self.socket.send_with_internal_socket(response.encode(), addr)  # Resend the response
                                continue
                            else:
                                # Data was in fact a string data, so the handshake is complete, we place back the data on the channel
                                channel.put((data, addr))
                                return
                        except Exception as e:
                            #wE tried to decode the data, but as it was bytes, we couldnt decode it, so the handshake is complete, we place back the data on the channel
                            channel.put((data, addr))
                            return
                raise TimeoutError

            except TimeoutError:
                self.time_out_errors.increase_try()  # Increase the try count
                continue

            except Exception:
                raise TimeoutError

        raise TimeoutError

    def data_is_command(self, data):
        """
        Check if the data represents a command.

        Args:
            data (str): The data.

        Returns:
            bool: True if data represents a command, False otherwise.
        """
        data = commands.Command.from_str(data)
        return data.option == commands.MessageOption.UPLOAD or data.option == commands.MessageOption.DOWNLOAD