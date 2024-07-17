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
    def __init__(self,conn: socket.socket, type:ConnectionType, topic:str = None):
        self.conn = conn
        self.type = type
        self.topic = topic


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

                    print(conn)

                    # client_details_json = conn.recv(4096).decode()
                    # client_details = json.loads(client_details_json)
                    # print(client_details)

                    # type = self.client_init(conn)
                    # print(type)

                    # self.connections.append(Connection(conn,ConnectionType.SUBSCRIBER))
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
                    if data.decode().startswith('/'):
                        headers = data.decode().lstrip('/').split(':')
                        if headers[0] == 'subscriber':
                            self.connections.append(Connection(conn,ConnectionType.SUBSCRIBER, headers[1]))
                            print(f"{bcolors.OKGREEN}New subscriber added{bcolors.ENDC} with topic {headers[1]}")
                        elif headers[0] == 'publisher':
                            self.connections.append(Connection(conn,ConnectionType.PUBLISHER, headers[1]))
                            print(f"{bcolors.OKGREEN}New publisher added{bcolors.ENDC} with topic {headers[1]}")
                        else:
                            print(f"{bcolors.FAIL}Invalid header{bcolors.ENDC}")
                        continue


                    # if data.decode().lower().startswith('/'):
                    #     if data.decode().lower() == '/subscriber':
                    #         self.connections.append(Connection(conn,ConnectionType.SUBSCRIBER))
                    #         print(f"{bcolors.OKGREEN}New subscriber added{bcolors.ENDC}")
                    #     elif data.decode().lower() == '/publisher':
                    #         self.connections.append(Connection(conn,ConnectionType.PUBLISHER))
                    #         print(f"{bcolors.OKGREEN}New publisher added{bcolors.ENDC}")

                    # print(f"Received from client: {data.decode()}")
                    # conn.sendall(data)
                    conn.sendall("200".encode())
                    # send to all subscribers
                    for connection in self.connections:
                        if connection.type == ConnectionType.SUBSCRIBER and connection.topic == headers[1]:
                        # and connection.topic == 

                            connection.conn.sendall(data)
                    

                except socket.error as e:
                    print(f"{bcolors.FAIL}Socket error during client communication: {e}{bcolors.ENDC}")
                    break  # Break the loop if there is a socket error
        except Exception as e:
            print(f"{bcolors.FAIL}Error during client communication: {e}{bcolors.ENDC}")
        finally:
            try:
                conn.close()
                # remove connection from list
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
                    # remove connection from list
                    self.connections = [connection for connection in self.connections if connection.conn != conn]
                    print(f"{bcolors.WARNING}Connection closed{bcolors.ENDC}")
            except Exception as e:
                print(f"{bcolors.FAIL}Error closing connection: {e}{bcolors.ENDC}")


        
# if __name__ == "__main__":
#     server = Server()
#     server.start()
