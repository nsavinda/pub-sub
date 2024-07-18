import socket
import sys
import threading
from config import HOST, PORT, MAXC
from utils import bcolors
from enum import Enum

import json

class ConnectionType(Enum):
    PUBLISHER = "publisher"
    SUBSCRIBER = "subscriber"

class RelativeServer:
    def __init__(self, conn: socket.socket, host: str, port: int) -> None:
        print(f"Connecting from {conn.getpeername()}")
        print(f"Connecting to {host}:{port}")
        self.host = host
        self.port = port
        self.conn = conn
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((host, port))

        print(f"{bcolors.OKGREEN}Connected to server at {host}:{port}{bcolors.ENDC}")

    def handle_server(self) -> None:
        self.server_socket.sendall(f'/server:{self.conn.getsockname()[0]}:{self.conn.getsockname()[1]}'.encode())
        print(f"Sending to {self.host}:{self.port} -> {self.conn.getsockname()[0]}:{self.conn.getsockname()[1]}")

class Connection:
    def __init__(self, conn: socket.socket, type: ConnectionType, topic: str = None):
        self.conn = conn
        self.type = type
        self.topic = topic

class Server:
    def __init__(self, host: str = HOST, port: int = PORT) -> None:
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections: list[Connection] = []
        self.relative_servers: list[RelativeServer] = []

    def start(self) -> None:
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(MAXC)
            print(f"{bcolors.OKGREEN}Server listening on {self.host}:{self.port}{bcolors.ENDC}")

            while True:
                try:
                    conn, addr = self.server_socket.accept()
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
                data = conn.recv(4096)
                if not data:
                    break
                print(f"Received from client({conn.getpeername()}): {data.decode()}")

                # Handle client requests and interactions here

        except Exception as e:
            print(f"{bcolors.FAIL}Error during client communication: {e}{bcolors.ENDC}")
        finally:
            try:
                conn.close()
                self.connections = [connection for connection in self.connections if connection.conn != conn]
                print(f"{bcolors.WARNING}Connection closed{bcolors.ENDC}")
            except Exception as e:
                print(f"{bcolors.FAIL}Error closing connection: {e}{bcolors.ENDC}")

    def client_init(self, conn: socket.socket) -> None:
        try:
            client_json = conn.recv(4096)
            if not client_json:
                print(f"{bcolors.FAIL}Error: No data received from client{bcolors.ENDC}")
                return

            client = json.loads(client_json.decode())
            print(client)

            return client['type']

        except json.JSONDecodeError as je:
            print(f"{bcolors.FAIL}Error decoding JSON: {je}{bcolors.ENDC}")
        except socket.error as se:
            print(f"{bcolors.FAIL}Socket error: {se}{bcolors.ENDC}")
        except Exception as e:
            print(f"{bcolors.FAIL}Error during client initialization: {e}{bcolors.ENDC}")
        finally:
            try:
                if conn:
                    conn.close()
                    self.connections = [connection for connection in self.connections if connection.conn != conn]
                    print(f"{bcolors.WARNING}Connection closed{bcolors.ENDC}")
            except Exception as e:
                print(f"{bcolors.FAIL}Error closing connection: {e}{bcolors.ENDC}")

port: int = int(sys.argv[1] if len(sys.argv) > 1 else 65432)


if __name__ == "__main__":
    server = Server(port = port)
    server.start()