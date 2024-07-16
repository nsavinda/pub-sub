from client import Client
import sys

host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
port = int(sys.argv[2] if len(sys.argv) > 2 else 65432)

if __name__ == "__main__":
    client = Client(server_host=host, server_port=port)
    client.start()
