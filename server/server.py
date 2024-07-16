import socket
import threading
from config import HOST, PORT, MAXC
from utils import bcolors
from enum import Enum

import json

class ConnectionType(Enum):
    PUBLISHER = "publisher"
    SUBSCRIBER = "subscriber"


class Connection:
    def __init__(self,conn: socket.socket, type:ConnectionType):
        self.conn = conn
        self.type = type


# class Connection:
#     def __init__(self,tread: threading.Thread, type:ConnectionType):
#         self.conn = conn
#         self.type = type




class Server:
    def __init__(self, host: str = HOST, port: int = PORT) -> None:
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections : list[Connection] = []
    
    def start(self) -> None:
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(MAXC)
            print(f"{bcolors.OKGREEN}Server listening on {self.host}:{self.port}{bcolors.ENDC}")

            while True:
                try:
                    conn, addr = self.server_socket.accept()
                    # client_details_json = conn.recv(4096).decode()
                    # client_details = json.loads(client_details_json)
                    # print(client_details)

                    self.connections.append(Connection(conn,ConnectionType.SUBSCRIBER))
                    print(f"{bcolors.OKCYAN}Connected by {addr}{bcolors.ENDC}")
                    client_thread = threading.Thread(target=self.handle_client, args=(conn,))
                    client_thread.start()
                except Exception as e:
                    print(f"{bcolors.FAIL}Error handling client: {e}{bcolors.ENDC}")
        except KeyboardInterrupt:
            print("Server stopped by user")
            exit(0)
        except Exception as e:
            print(f"{bcolors.FAIL}Failed to start server: {e}{bcolors.ENDC}")
        finally:
            self.server_socket.close()
            

    def handle_client(self, conn: socket.socket) -> None:
        try:
            while True:
                try:
                    data = conn.recv(4096)
                    if not data:
                        break
                    print(f"Received from client: {data.decode()}")
                    # conn.sendall(data)
                    # send to all subscribers
                    for connection in self.connections:
                        if connection.type == ConnectionType.SUBSCRIBER:
                            connection.conn.sendall(data)

                except socket.error as e:
                    print(f"{bcolors.FAIL}Socket error during client communication: {e}{bcolors.ENDC}")
                    break  # Break the loop if there is a socket error
        except Exception as e:
            print(f"{bcolors.FAIL}Error during client communication: {e}{bcolors.ENDC}")
        finally:
            try:
                conn.close()
                print(f"{bcolors.WARNING}Connection closed{bcolors.ENDC}")
            except Exception as e:
                print(f"{bcolors.FAIL}Error closing connection: {e}{bcolors.ENDC}")

# if __name__ == "__main__":
#     server = Server()
#     server.start()
