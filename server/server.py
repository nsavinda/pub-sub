import socket
from typing import List, Tuple
from config import HOST, PORT
from utils import bcolors


class Server:
    def __init__(self, host:str = HOST, port:int = PORT)-> None:
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def start(self)->None:
        try:
            self.server_socket.bind((self.host,self.port))
            self.server_socket.listen()
            # print(f"Server listening on {self.host}:{self.port}")
            print(f"{bcolors.OKGREEN}Server listening on {self.host}:{self.port}{bcolors.ENDC}")

            while True:
                try:
                    conn, addr = self.server_socket.accept()
                    with conn:
                        # print(f"Connected by {addr}")
                        print(f"{bcolors.OKCYAN}Connected by {addr}{bcolors.ENDC}")
                        
                        self.handle_client(conn)
                except Exception as e:
                    # print(f"Error handling client {addr}: {e}")
                    print(f"{bcolors.FAIL}Error handling client {addr}: {e}{bcolors.ENDC}")
                    
        except Exception as e:
            # print(f"Failed to start server: {e}")
            print(f"{bcolors.FAIL}Failed to start server: {e}{bcolors.ENDC}")
        
        finally:
            self.server_socket.close()
            

        
    def handle_client(self,conn:socket.socket) -> None: # handle client connection
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Received from client: {data.decode()}")
                conn.sendall(data)
        except Exception as e:
            # print(f"Error during client communication: {e}")
            print(f"{bcolors.FAIL}Error during client communication: {e}{bcolors.ENDC}")
        finally:
            conn.close()