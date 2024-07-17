import socket
from config import SERVER_HOST, SERVER_PORT, SERVER_ROLE
from utils import bcolors


class Client:
    def __init__(self, server_host: str = SERVER_HOST, server_port: int = SERVER_PORT, role: str = SERVER_ROLE) -> None:
        self.server_host = server_host
        self.server_port = server_port
        self.role = role.upper()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self) -> None:
        try:
            self.client_socket.connect((self.server_host, self.server_port))
            print(f"{bcolors.OKGREEN}Connected to server at {self.server_host}:{self.server_port}{bcolors.ENDC} as {self.role}")
            self.client_socket.sendall(self.role.encode())

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
                message = input(f"{bcolors.OKBLUE}Enter message to send (or '/terminate' to quit):{bcolors.ENDC}")
                if message.lower() == '/terminate':
                    self.client_socket.close()
                    break
                self.send_message(message)
        except KeyboardInterrupt:
            print("Publisher stopped by user")
        except ConnectionAbortedError:
            print(f"{bcolors.FAIL}Connection Aborted: Server closed the connection.{bcolors.ENDC}")
        except ConnectionResetError:
            print(f"{bcolors.FAIL}Connection Reset: Connection reset by peer.{bcolors.ENDC}")
        except BrokenPipeError:
            print(f"{bcolors.FAIL}Broken Pipe: Server unexpectedly closed the connection.{bcolors.ENDC}")
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
        except ConnectionResetError:
            print("Connection reset by peer")
        except KeyboardInterrupt:
            print("Subscriber stopped by user")
        except Exception as e:
            print(f"{bcolors.FAIL}Error: {e}{bcolors.ENDC}")
        finally:
            self.client_socket.close()

    def send_message(self, message: str) -> None:
        try:
            self.client_socket.sendall(message.encode())
            data = self.client_socket.recv(1024)
            print(f"{bcolors.OKCYAN}Received from server: {data.decode()}{bcolors.ENDC}")
        except Exception as e:
            print(f"{bcolors.FAIL}Error during message sending/receiving: {e}{bcolors.ENDC}")
