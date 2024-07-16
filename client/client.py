import socket
from config import SERVER_HOST, SERVER_PORT


class Client:
    def __init__(self, server_host: str = SERVER_HOST, server_port: int = SERVER_PORT) -> None:
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        
    def start(self) -> None:
        try:
            self.client_socket.connect((self.server_host,self.server_port))
            print(f"Connected to server at {self.server_host}:{self.server_port}")
            
            while True:
                try:
                    message = input("Enter message to send (or '/exit' to quit):")
                    if message.lower() == '/exit':
                        break
                    self.send_message(message)
                except Exception as e:
                    print(f"Error during message input or sending: {e}")
                
        except Exception as e:
            print(f"Failed to connect to server: {e}")
        finally:
            self.client_socket.close()
            
    def send_message(self,message:str)-> None:
        try:
            self.client_socket.sendall(message.encode())
            data = self.client_socket.recv(1024)
            print(f"Received from server: {data.decode()}")
        except Exception as e:
            print(f"Error during message sending/receiving: {e}")