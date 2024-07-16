import socket
from typing import List, Tuple
from config import HOST, PORT


class Server:
    def __init__(self, host:str = HOST, port:int = PORT)-> None:
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def start(self)->None:
        try:
            self.server_socket.bind((self.host,self.port))
            self.server_socket.listen()
            print(f"Server listening on {self.host}:{self.port}")

            while True:
                try:
                    conn, addr = self.server_socket.accept()
                    with conn:
                        print(f"Connected by {addr}")
                        self.handle_client(conn)
                except Exception as e:
                    print(f"Error handling client {addr}: {e}")
                    
        except Exception as e:
            print(f"Failed to start server: {e}")
        
        finally:
            self.server_socket.close()
            

        
    def handle_client(self,conn:socket.socket) -> None: # handle client connection
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)
        except Exception as e:
            print(f"Error during client communication: {e}")
        finally:
            conn.close()