import socket
import threading
from typing import List, Tuple ,Dict
from config import HOST, PORT
from utils import bcolors

class Server:
    def __init__(self, host:str = HOST, port:int = PORT)-> None:
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients: Dict[socket.socket, str] = {}
        self.lock = threading.Lock()
    
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
                        client_thread = threading.Thread(target=self.handle_client, args=(conn,))
                        client_thread.start()

                except Exception as e:
                    # print(f"Error handling client {addr}: {e}")
                    print(f"{bcolors.FAIL}Error handling client {addr}: {e}{bcolors.ENDC}")
        except KeyboardInterrupt:
            print("Server stopped by user")
        except Exception as e:
            # print(f"Failed to start server: {e}")
            print(f"{bcolors.FAIL}Failed to start server: {e}{bcolors.ENDC}")  
        finally:
            self.server_socket.close()
            print("Server stopped")

    def handle_client(self, conn: socket.socket) -> None:
        try:
            role = conn.recv(1024).decode().upper()
            print(f"Client role: {role}")
            with self.lock:
                self.clients[conn] = role
                print(f"{bcolors.OKGREEN}Client role: {role}{bcolors.ENDC}")

            if role == 'PUBLISHER':
                print(f"{bcolors.OKGREEN}Handle Publisher called{bcolors.ENDC}")
                self.handle_publisher(conn)

            elif role == 'SUBSCRIBER':
                print(f"{bcolors.OKGREEN}Handle Subscriber called{bcolors.ENDC}")
                self.handle_subscriber(conn)
            else:
                print("Invalid role received from client.")
                conn.close()
        except Exception as e:
            print(f"{bcolors.FAIL}Error handling client: {e}{bcolors.ENDC}")
        finally:
            with self.lock:
                if conn in self.clients:
                    del self.clients[conn]
            conn.close()


    def handle_publisher(self, conn: socket.socket) -> None:
        try:
            while True:
                message = conn.recv(1024).decode()
                if not message:
                    break
                print(f"{bcolors.OKBLUE}Message from publisher: {message}{bcolors.ENDC}")
                self.broadcast(message, exclude_publisher=True)
        except ConnectionResetError:
            print(f"{bcolors.FAIL}Connection reset by peer{bcolors.ENDC}")
        except Exception as e:
            print(f"{bcolors.FAIL}Error in publisher mode: {e}{bcolors.ENDC}")
        finally:
            with self.lock:
                if conn in self.clients:
                    del self.clients[conn]
            conn.close()

    def handle_subscriber(self, conn: socket.socket) -> None:
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Received from client: {data.decode()}")
        except ConnectionResetError:
            print(f"{bcolors.FAIL}Connection reset by peer{bcolors.ENDC}")
        except Exception as e:
            print(f"{bcolors.FAIL}Error in subscriber mode: {e}{bcolors.ENDC}")
        finally:
            with self.lock:
                if conn in self.clients:
                    del self.clients[conn]
            conn.close()


    def broadcast(self, message: str, exclude_publisher: bool = False) -> None:
        with self.lock:
            for client, role in self.clients.items():
                if exclude_publisher and role == 'PUBLISHER':
                    continue
                try:
                    if role == 'SUBSCRIBER':
                        client.sendall(message.encode())
                except Exception as e:
                    print(f"{bcolors.FAIL}Error broadcasting message: {e}{bcolors.ENDC}")