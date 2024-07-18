import socket
import sys
from config import SERVER_HOST, SERVER_PORT
from utils import bcolors

class Client:
    def __init__(self, server_host: str = SERVER_HOST, server_port: int = SERVER_PORT, role: str = 'PUBLISHER', topic: str = 'GENERAL') -> None:
        self.server_host = server_host
        self.server_port = server_port
        self.role = role.upper()
        self.topic = topic.upper()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self) -> None:
        try:
            self.client_socket.connect((self.server_host, self.server_port))
            print(f"{bcolors.OKGREEN}Connected to server at {self.server_host}:{self.server_port} as {self.role} on topic {self.topic}{bcolors.ENDC}")

            # Send role and topic as a single message with a delimiter
            self.client_socket.sendall(f"{self.role},{self.topic}".encode())

            if self.role == 'PUBLISHER':
                self.publisher_mode()
            elif self.role == 'SUBSCRIBER':
                self.subscriber_mode()
            else:
                print("Invalid role. Please choose either PUBLISHER or SUBSCRIBER.")

        except KeyboardInterrupt:
            print("Client stopped by user")
        except Exception as e:
            print(f"{bcolors.FAIL}Failed to connect to server: {e}{bcolors.ENDC}")
        finally:
            self.client_socket.close()

    def publisher_mode(self) -> None:
        try:
            while True:
                message = input(f"{bcolors.OKBLUE}Enter message to send (or '/terminate' to quit): {bcolors.ENDC}")
                if message.lower() == '/terminate':
                    break
                self.send_message(f"{self.topic}: {message}")
        except KeyboardInterrupt:
            print("Publisher stopped by user")
        except Exception as e:
            print(f"{bcolors.FAIL}Error during message input or sending: {e}{bcolors.ENDC}")
        finally:
            self.client_socket.close()

    def subscriber_mode(self) -> None:
        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                print(f"{bcolors.OKCYAN}Received from server: {data.decode()}{bcolors.ENDC}")
        except KeyboardInterrupt:
            print("Subscriber stopped by user")
        except Exception as e:
            print(f"{bcolors.FAIL}Error during receiving: {e}{bcolors.ENDC}")
        finally:
            self.client_socket.close()

    def send_message(self, message: str) -> None:
        try:
            self.client_socket.sendall(message.encode())
        except Exception as e:
            print(f"{bcolors.FAIL}Error during message sending: {e}{bcolors.ENDC}")
            return
        
        try:
            data = self.client_socket.recv(1024)
            print(f"{bcolors.OKCYAN}Received from server: {data.decode()}{bcolors.ENDC}")
        except Exception as e:
            print(f"{bcolors.FAIL}Error during receiving response: {e}{bcolors.ENDC}")