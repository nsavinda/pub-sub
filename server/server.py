import socket
import threading
from config import HOST, PORT, MAXC
from utils import bcolors
from enum import Enum

import json

class ConnectionType(Enum):
    PUBLISHER = "publisher"
    SUBSCRIBER = "subscriber"

class RelativeServer:
    def __init__(self,host:str, port:int) -> None:
        print(f"Connecting to {host}:{port}")
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print(f"{bcolors.OKGREEN}Connected to server at {host}:{port}{bcolors.ENDC}")
        # self.server_socket.connect((host, port))
        # self.thread = threading.Thread(target=self.handle_server)
    def handle_server(self,host:str="",port:str="") -> None:
        self.server_socket.connect((self.host, self.port))
        # self.server_socket.sendall(f'/server:{self.conn.getsockname()[0]}:{self.conn.getsockname()[1]}'.encode())
        if host and port:
            self.server_socket.sendall(f'/server:{host}:{port}'.encode())
            # print(f"Sending to {self.host}:{self.port} -> {host}:{port}")
        


    # def send_server(self) -> None:
    #     for RelativeServer in sel


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
    def __init__(self, host: str = HOST, port: int = PORT,relative_server:str = "" ) -> None:
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections : list[Connection] = []
        self.relative_servers : list[RelativeServer] = []
        self.relative_server: str = relative_server
        
    
    def start(self) -> None:
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(MAXC)
            print(f"{bcolors.OKGREEN}Server listening on {self.host}:{self.port}{bcolors.ENDC}")

            if self.relative_server:
                servers = self.relative_server.split(',')
                for server in servers:
                    self.relative_servers.append(RelativeServer(server.split(':')[0], int(server.split(':')[1])))
                    self.relative_servers[-1].handle_server(self.host, self.port)
                # self.relative_servers.append(RelativeServer(self.relative_server.split(':')[0], int(self.relative_server.split(':')[1])))
                # self.relative_servers[0].handle_server(self.host, self.port)


            while True:
                try:
                    conn, addr = self.server_socket.accept()

                    # print(conn)

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
                msg_from_server:int = 0
                try:
                    data = conn.recv(4096)
                    if not data:
                        break
                    # print(f"Received from client({conn.getpeername()}): {data.decode()}")
                    # pritn relative servers host and port
                    # print([server.host + ":" + str(server.port) for server in self.relative_servers])
                    
                    if data.decode().startswith('/'):
                        headers = data.decode().lstrip('/').split(':')
                        if headers[0] == 'subscriber':
                            self.connections.append(Connection(conn,ConnectionType.SUBSCRIBER, headers[1]))
                            print(f"{bcolors.OKGREEN}New subscriber added{bcolors.ENDC} with topic {headers[1]}")
                        elif headers[0] == 'publisher':
                            self.connections.append(Connection(conn,ConnectionType.PUBLISHER, headers[1]))
                            print(f"{bcolors.OKGREEN}New publisher added{bcolors.ENDC} with topic {headers[1]}")
                        elif headers[0] == 'server':
                            if any(server.host == headers[1] and server.port == int(headers[2]) for server in self.relative_servers):
                                print(f"{bcolors.FAIL}Server already exists{bcolors.ENDC}")
                            else:
                                for server in self.relative_servers:
                                    # print(server.host+":"+str(server.port))
                                    # if server.conn.getpeername()[0] == conn.getpeername()[0] and server.conn.getpeername()[1] == conn.getpeername()[1]:
                                    if server.host != headers[1] or server.port != int(headers[2]) and server.host != self.host and server.port != self.port:
                                        # server.server_socket.sendall(f'/server:{conn.getsockname()[0]}:{conn.getsockname()[1]}'.encode())

                                        server.server_socket.sendall(f'/server:{headers[1]}:{headers[2]}'.encode())
                                        # print(f"Sending to {server.host}:{server.port} -> {headers[1]}:{headers[2]}")


                                        # print(f"Sending to {conn.getpeername()} -> {server.host}:{server.port}")
                                        # conn.sendall(f'/server:{server.host}:{server.port}'.encode())
                                relative_server = RelativeServer(headers[1], int(headers[2]))
                                thread = threading.Thread(target=relative_server.handle_server)
                                thread.start()
                                self.relative_servers.append(relative_server)
                                # thread = threading.Thread(target=RelativeServer, args=(conn, headers[1], int(headers[2])))
                                # thread.start()

                                # self.relative_servers.append(RelativeServer(conn, headers[1], int(headers[2])))

                                # print([server.server_socket for server in self.relative_servers])
                                print(f"{bcolors.OKGREEN}New server added{bcolors.ENDC} with host {headers[1]} and port {headers[2]}")
                        elif headers[0] == 'topic':
                            # check server in relative_servers
                            # if not in relative_servers, send error
                            msg_from_server = 1
                            # print(f"{server.conn.getpeername()[0]}:{server.conn.getpeername()[1]}")
                            # if any(server.conn.getpeername()[0] == conn.getpeername()[0] and server.conn.getpeername()[1] == conn.getpeername()[1] for server in self.relative_servers):
                            #     print(f"{bcolors.OKGREEN}Topic added{bcolors.ENDC} with topic {headers[1]}")
                            #     for connection in self.connections:
                            #         if connection.type == ConnectionType.SUBSCRIBER and connection.topic == headers[1]:
                            #             connection.conn.sendall(f'{headers[2]}'.encode())
                            # else:
                            #     print(f"{bcolors.FAIL}Server not found in relative servers{bcolors.ENDC}")
                            # print(f"{bcolors.OKGREEN}Topic added{bcolors.ENDC} with topic {headers[1]}")
                            for connection in self.connections:
                                if connection.type == ConnectionType.SUBSCRIBER and connection.topic == headers[1]:
                                    connection.conn.sendall(f'{headers[2]}'.encode())

                            
                        else:
                            print(f"{bcolors.FAIL}Invalid header{bcolors.ENDC}")
                        continue


                    # if data.decode().lower().startswith('/'):
                    #     if data.decode().lower() == '/subscriber':
                    #         self.connections.append(Connection(conn,ConnectionType.SUBSCRIBER))
                    #         print(f"{bcolors.OKGREEN}New subscriber added{bcolors.ENDC}")
                    #     elif data.decode().lower() == '/publisher':
                    #         self.connections.append(Connection(conn,ConnectionType.PUBLISHER))Connection closed
                    #         print(f"{bcolors.OKGREEN}New publisher added{bcolors.ENDC}")

                    # print(f"Received from client: {data.decode()}")
                    # conn.sendall(data)
                    conn.sendall("200".encode())
                    # send to all subscribers
                    for connection in self.connections:
                        if connection.type == ConnectionType.SUBSCRIBER and connection.topic == headers[1]:
                        # and connection.topic == 

                            connection.conn.sendall(data)
                    if msg_from_server == 0:
                        for server in self.relative_servers:
                            server.server_socket.sendall(f'/topic:{headers[1]}:{data.decode()}'.encode())

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


    # def client_init(self, conn: socket.socket) -> None:
    #     try:
    #         client_json = conn.recv(4096)
    #         if not client_json:
    #             print(f"{bcolors.FAIL}Error: No data received from client{bcolors.ENDC}")
    #             return

    #         client = json.loads(client_json.decode())
    #         print(client)

    #         return client['type']

    #     except json.JSONDecodeError as je:
    #         print(f"{bcolors.FAIL}Error decoding JSON: {je}{bcolors.ENDC}")
    #     except socket.error as se:
    #         print(f"{bcolors.FAIL}Socket error: {se}{bcolors.ENDC}")
    #     except Exception as e:
    #         print(f"{bcolors.FAIL}Error during client initialization: {e}{bcolors.ENDC}")
    #     finally:
    #         try:
    #             if conn:
    #                 conn.close()
    #                 # remove connection from list
    #                 self.connections = [connection for connection in self.connections if connection.conn != conn]
    #                 print(f"{bcolors.WARNING}Connection closed{bcolors.ENDC}")
    #         except Exception as e:
    #             print(f"{bcolors.FAIL}Error closing connection: {e}{bcolors.ENDC}")

    
        
# if __name__ == "__main__":
#     server = Server()
#     server.start()
