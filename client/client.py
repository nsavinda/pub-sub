import socket
from config import SERVER_HOST, SERVER_PORT
from utils import bcolors


class Client:
    def __init__(self, server_host: str = SERVER_HOST, server_port: int = SERVER_PORT) -> None:
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        
    def start(self) -> None:
        try:
            self.client_socket.connect((self.server_host,self.server_port))
            print(f"{bcolors.OKGREEN}Connected to server at {self.server_host}:{self.server_port}{bcolors.ENDC}")
            
            while True:
                try:
                    # message = input("Enter message to send (or '/exit' to quit):")
                    message = input(f"{bcolors.OKBLUE}Enter message to send (or '/exit' to quit):{bcolors.ENDC}")
                    if message.lower() == '/exit':
                        break
                    self.send_message(message)
                except Exception as e:
                    # print(f"Error during message input or sending: {e}")
                    print(f"{bcolors.FAIL}Error during message input or sending: {e}{bcolors.ENDC}")
                
        except Exception as e:
            # print(f"Failed to connect to server: {e}")
            print(f"{bcolors.FAIL}Failed to connect to server: {e}{bcolors.ENDC}")
        finally:
            self.client_socket.close()
            
    def send_message(self,message:str)-> None:
        try:
            self.client_socket.sendall(message.encode())
            data = self.client_socket.recv(1024)
            # print(f"Received from server: {data.decode()}")
            print(f"{bcolors.OKCYAN}Received from server: {data.decode()}{bcolors.ENDC}")
        except Exception as e:
            # print(f"Error during message sending/receiving: {e}")
            print(f"{bcolors.FAIL}Error during message sending/receiving: {e}{bcolors.ENDC}")