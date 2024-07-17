from client import Client
import sys

if len(sys.argv) < 4:
    print("Usage: python main.py <server_host> <server_port> <role>")
    sys.exit(1)

host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
port = int(sys.argv[2] if len(sys.argv) > 2 else 65432)
role = sys.argv[3]

if __name__ == "__main__":
    client = Client(server_host=host, server_port=port , role=role)
    client.start()
