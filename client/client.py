import socket
from config import SERVER_HOST, SERVER_PORT
from utils import bcolors, ConnectionType
import json


class Header:
    def __init__(self, type: str) -> None:
        self.type = type
        

class Client:
    def __init__(self, server_host: str = SERVER_HOST, server_port: int = SERVER_PORT, type = 'subscriber') -> None:
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.type = type
        self.header = Header(type)
        
    def start(self) -> None:
        try:
            self.client_socket.connect((self.server_host, self.server_port))
            print(f"{bcolors.OKGREEN}Connected to server at {self.server_host}:{self.server_port}{bcolors.ENDC}")
            
            print(self.type)
            self.send_header()
            if self.type == 'subscriber':
                self.receive_message()

            else:    
                while True:
                    try:
                        message = input(f"{bcolors.OKBLUE}Enter message to send (or '/terminate' to quit): {bcolors.ENDC}")
                        if message.lower() == '/terminate':
                            break
                        self.send_message(message)
                    except Exception as e:
                        print(f"{bcolors.FAIL}Error during message input or sending: {e}{bcolors.ENDC}")
        except KeyboardInterrupt:
            print("Client stopped by user")
        except Exception as e:
            print(f"{bcolors.FAIL}Failed to connect to server: {e}{bcolors.ENDC}")
        finally:
            self.client_socket.close()
            print(f"{bcolors.WARNING}Connection closed{bcolors.ENDC}")
            
    def send_message(self, message: str) -> None:
        try:
            self.client_socket.sendall(message.encode())
            data = self.client_socket.recv(4096)
            
            if not data:  # If no data is received, the server has closed the connection
                print(f"{bcolors.WARNING}Server closed the connection{bcolors.ENDC}")
                self.client_socket.close()
                exit(1)
            # print(f"{bcolors.OKCYAN}Received from server: {data.decode()}{bcolors.ENDC}")
            if data.decode() != "200":
                print(f"{bcolors.FAIL}Error: {data.decode()}{bcolors.ENDC}")
                
        except Exception as e:
            print(f"{bcolors.FAIL}Error during message sending/receiving: {e}{bcolors.ENDC}")
            self.client_socket.close()


    def receive_message(self) -> None:
        try:
            while True:
                data = self.client_socket.recv(4096)
                if not data:
                    break
                print(f"Received from server: {data.decode()}")
        except Exception as e:
            print(f"{bcolors.FAIL}Error during message receiving: {e}{bcolors.ENDC}")
            self.client_socket.close()
            exit(1)
        finally:
            self.client_socket.close()
            print(f"{bcolors.WARNING}Connection closed{bcolors.ENDC}")


    def send_header(self) -> None:
        # try:
        #     self.client_socket.sendall(json.dumps(self.header.__dict__).encode())
        # except Exception as e:
        #     print(f"{bcolors.FAIL}Error during header sending: {e}{bcolors.ENDC}")
        #     self.client_socket.close()
        #     exit(1)
        # finally:
        #     self.client_socket.close()
        #     print(f"{bcolors.WARNING}Connection closed{bcolors.ENDC}")
        self.client_socket.sendall(f"/{self.type}".encode())