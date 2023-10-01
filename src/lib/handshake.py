import queue
from lib import commands
from lib.commands import CommandResponse
from lib.rdt.rdt_sw_socket import TimeOutErrors

from lib.rdt.rdt_sw_socket import RdtSWSocketClient
from lib.constants import HARDCODED_BUFFER_SIZE, HARDCODED_MAX_TIMEOUT_TRIES, HARDCODED_TIMEOUT, HARDCODED_TIMEOUT_FOR_RECEIVING_INPUT


class ThreeWayHandShake:

    def __init__(self, socket: RdtSWSocketClient):
        self.socket = socket
        self.time_out_errors = TimeOutErrors()

    def send(self, response, addr):
        
        print("--DEBUG-- sending data : ", response)
        # Mientras no pase el numero de intentos para mandar el paquete definido por el HARDCODED_MAX_TIMEOUT_PACKET, labura

        self.socket.set_timeout(self.time_out_errors.get_timeout())

        while not self.time_out_errors.max_tries_exceeded():
            try:
                print("--DEBUG-- sending from send")
                self.socket.send_with_internal_socket(response.encode(), addr)

                #Recibimos el Ok sisi del lado del cliente
                response, addr = self.socket.recv_with_internal_socket(HARDCODED_BUFFER_SIZE)
                print(f"--DEBUG-- response received: {response}")
                return response
            
            except TimeoutError:
                print("--DEBUG-- error from timeout try number ", self.time_out_errors.get_tries())
                self.time_out_errors.increase_try()
                continue
        raise TimeoutError
 

    def send_with_queue_upload(self,data: CommandResponse,addr,channel: queue):
        print(f"--DEBUG-- sending data : {data}, addr : {addr}")
        self.socket.send_with_internal_socket(data.encode(), addr)

        while not self.time_out_errors.max_tries_exceeded():
            # print("--DEBUG-- waiting for response")
            if self.time_out_errors.get_tries() == HARDCODED_MAX_TIMEOUT_TRIES - 1:
                response,addr = channel.get(block = True, timeout = HARDCODED_TIMEOUT_FOR_RECEIVING_INPUT)
            else:
                response,addr = channel.get(block = True)
            # print("--DEBUG-- data received: ", response)
            if self.is_not_ok(response.decode()):
                self.socket.send_with_internal_socket(data.encode(), addr)
                self.time_out_errors.increase_try()
            else:
                return response

    def is_not_ok(self,data):
        return data != "OK" and data != "ERR Download canceled"

    def send_download(self,data:CommandResponse,addr,first_handshake: bool):
        # print("--DEBUG-- sending data : ", data)
        self.socket.send_with_internal_socket(data.encode(), addr)
        self.socket.set_timeout(HARDCODED_TIMEOUT)
        while not self.time_out_errors.max_tries_exceeded():
            try:
                response, addr = self.socket.recv_with_internal_socket(HARDCODED_BUFFER_SIZE)
                # print("--DEBUG-- response received: ", response)
                try:
                    decoded_response = response.decode() # va a ser data o filesize 
                    if first_handshake:
                        return response
                    if self.data_is_command(decoded_response):
                        self.socket.send_with_internal_socket(data.encode(), addr)
                        self.time_out_errors.increase_try()
                        continue
                    return response.encode(),addr
                
                except Exception as  e:
                    print("hubo una excepcion del try:",e)
                    return response,addr

            except TimeoutError:
                print("--DEBUG-- error from timeout try number ", self.time_out_errors.get_tries())
                self.time_out_errors.increase_try()
                self.socket.send_with_internal_socket(data.encode(), addr)
                continue
        raise TimeoutError

              





    def send_with_queue(self,response: CommandResponse, addr,channel: queue):

        print("--DEBUG-- sending data : ", response)
        # Mientras no pase el numero de intentos para mandar el paquete definido por el HARDCODED_MAX_TIMEOUT_PACKET, labura

        self.socket.set_timeout(HARDCODED_TIMEOUT)
        while not self.time_out_errors.max_tries_exceeded():
            try:
                # print("--DEBUG-- sending frp, semd with queue")
                self.socket.send_with_internal_socket(response.encode(), addr)
                # print("--DEBUG-- waiting for response")
                while self.time_out_errors.time_to_receive_data():
                    if not channel.empty():
                            data,addr = channel.get()
                            # print("--DEBUG-- data received: ...")
                            try:
                                if self.data_is_command(data.decode()):
                                    print(f"--DEBUG-- data was {data.decode()}")
                                    print(f"data was {data.decode()}")
                                    self.socket.send_with_internal_socket(response.encode(), addr)
                                    continue
                                else:
                                    print("--DEBUG-- data was in fact data")
                                    channel.put((data,addr))
                                    return
                            except Exception as e:
                                channel.put((data,addr))
                                print(f"putting the data back to channel {e}")

                                return                        
                raise TimeoutError


            except TimeoutError:
                print("--DEBUG-- error from timeout try number ", self.time_out_errors.get_tries())
                self.time_out_errors.increase_try()
                continue

            except Exception as e:
                print(f"e!!! {e}")
                raise TimeoutError
        raise TimeoutError

    def data_is_command(self,data):
        print(f"data es {data}")
        data = commands.Command.from_str(data)
        return data.option == commands.MessageOption.UPLOAD or data.option == commands.MessageOption.DOWNLOAD


