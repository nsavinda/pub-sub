import socket
import threading
from typing import Dict, Tuple
from utils import bcolors

class Server:
    def __init__(self, host: str = '127.0.0.1', port: int = 65432) -> None:
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients: Dict[socket.socket, Tuple[str, str]] = {}  # (role, topic)
        self.peers: Dict[socket.socket, Tuple[str, int]] = {}  # (host, port)
        self.lock = threading.Lock()

    def start(self) -> None:
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
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
        except Exception as e:
            print(f"{bcolors.FAIL}Failed to start server: {e}{bcolors.ENDC}")
        finally:
            self.server_socket.close()
            print("Server stopped")

    def handle_client(self, conn: socket.socket) -> None:
        try:
            data = conn.recv(1024).decode()
            parts = data.split(',')
            role = parts[0].strip().upper()
            if role == 'PEER':
                peer_host = parts[1].strip()
                peer_port = int(parts[2].strip())
                with self.lock:
                    self.peers[conn] = (peer_host, peer_port)
            else:
                topic = parts[1].strip().upper()
                if role not in ['PUBLISHER', 'SUBSCRIBER']:
                    print(f"Invalid role '{role}' received from client.")
                    conn.close()
                    return

                with self.lock:
                    self.clients[conn] = (role, topic)

                if 'PUBLISHER' in role:
                    self.handle_publisher(conn, topic)
                elif 'SUBSCRIBER' in role:
                    self.handle_subscriber(conn)
        except Exception as e:
            print(f"{bcolors.FAIL}Error handling client: {e}{bcolors.ENDC}")
        finally:
            with self.lock:
                if conn in self.clients:
                    del self.clients[conn]
                if conn in self.peers:
                    del self.peers[conn]
            conn.close()

    def handle_publisher(self, conn: socket.socket, topic: str) -> None:
        try:
            while True:
                message = conn.recv(1024).decode()
                if not message:
                    break
                print(f"{bcolors.OKBLUE}Message from publisher on topic {topic}: {message}{bcolors.ENDC}")
                self.broadcast(message, topic, conn)
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

    def broadcast(self, message: str, topic: str, publisher_conn: socket.socket) -> None:
        with self.lock:
            try:
                for client, (role, client_topic) in self.clients.items():
                    if role == 'SUBSCRIBER' and client_topic == topic:
                        try:
                            client.sendall(message.encode())
                        except Exception as e:
                            print(f"{bcolors.FAIL}Error broadcasting message: {e}{bcolors.ENDC}")
                for peer in self.peers:
                    try:
                        peer.sendall(f"BROADCAST,{topic},{message}".encode())
                    except Exception as e:
                        print(f"{bcolors.FAIL}Error broadcasting message to peer: {e}{bcolors.ENDC}")
                publisher_conn.sendall(message.encode())
            except Exception as e:
                if publisher_conn in self.clients:
                    print(f"{bcolors.FAIL}Error sending success response to publisher: {e}{bcolors.ENDC}")
                else:
                    print(f"{bcolors.FAIL}Error broadcasting message to subscriber: {e}{bcolors.ENDC}")

    def connect_to_peer(self, peer_host: str, peer_port: int) -> None:
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            peer_socket.connect((peer_host, peer_port))
            peer_socket.sendall(f"PEER,{self.host},{self.port}".encode())
            with self.lock:
                self.peers[peer_socket] = (peer_host, peer_port)
            print(f"{bcolors.OKGREEN}Connected to peer at {peer_host}:{peer_port}{bcolors.ENDC}")
        except Exception as e:
            print(f"{bcolors.FAIL}Failed to connect to peer: {e}{bcolors.ENDC}")
