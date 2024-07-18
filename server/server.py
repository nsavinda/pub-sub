import socket
import threading
from typing import List, Dict, Tuple
from utils import bcolors  # Assuming bcolors for colorizing output

class Server:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected_peers: List[Tuple[str, int]] = []  # List of connected peers (host, port)
        self.clients: Dict[socket.socket, Tuple[str, str]] = {}  # (role, topic)
        self.lock = threading.Lock()

    def start(self) -> None:
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
            print(f"{bcolors.OKGREEN}Server listening on {self.host}:{self.port}{bcolors.ENDC}")

            # Thread to handle incoming connections from other servers
            threading.Thread(target=self.accept_connections).start()

            while True:
                try:
                    conn, addr = self.server_socket.accept()
                    print(f"{bcolors.OKCYAN}Connected by {addr}{bcolors.ENDC}")
                    threading.Thread(target=self.handle_client, args=(conn,)).start()
                except Exception as e:
                    print(f"{bcolors.FAIL}Error handling client: {e}{bcolors.ENDC}")
        except KeyboardInterrupt:
            print("Server stopped by user")
        except Exception as e:
            print(f"{bcolors.FAIL}Failed to start server: {e}{bcolors.ENDC}")
        finally:
            self.server_socket.close()
            print("Server stopped")

    def accept_connections(self) -> None:
        while True:
            try:
                conn, addr = self.server_socket.accept()
                self.connected_peers.append(addr)
                print(f"{bcolors.OKCYAN}Connected to peer {addr}{bcolors.ENDC}")
                threading.Thread(target=self.handle_peer, args=(conn,)).start()
            except Exception as e:
                print(f"{bcolors.FAIL}Error accepting peer connection: {e}{bcolors.ENDC}")

    def handle_peer(self, conn: socket.socket) -> None:
        try:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                parts = data.split(',')
                action = parts[0].strip().upper()

                if action == 'PUBLISH':
                    topic = parts[1].strip().upper()
                    message = parts[2].strip()
                    self.broadcast(message, topic, conn)

                elif action == 'REGISTER':
                    topic = parts[1].strip().upper()
                    with self.lock:
                        self.clients[conn] = ('SUBSCRIBER', topic)
        except Exception as e:
            print(f"{bcolors.FAIL}Error handling peer: {e}{bcolors.ENDC}")
        finally:
            with self.lock:
                if conn in self.clients:
                    del self.clients[conn]
            conn.close()

    def handle_client(self, conn: socket.socket) -> None:
        try:
            data = conn.recv(1024).decode()
            parts = data.split(',')
            role = parts[0].strip().upper()

            if role == 'PUBLISHER':
                topic = parts[1].strip().upper()
                with self.lock:
                    self.clients[conn] = ('PUBLISHER', topic)
            else:
                print(f"Invalid role '{role}' received from client.")
                conn.close()
                return

        except Exception as e:
            print(f"{bcolors.FAIL}Error handling client: {e}{bcolors.ENDC}")
        finally:
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
                for peer_host, peer_port in self.connected_peers:
                    try:
                        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        peer_socket.connect((peer_host, peer_port))
                        peer_socket.sendall(f"PUBLISH,{topic},{message}".encode())
                        peer_socket.close()
                    except Exception as e:
                        print(f"{bcolors.FAIL}Error broadcasting message to peer {peer_host}:{peer_port}: {e}{bcolors.ENDC}")
            except Exception as e:
                print(f"{bcolors.FAIL}Error broadcasting message: {e}{bcolors.ENDC}")
