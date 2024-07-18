from client import Client
import sys
from config import SERVER_HOST, SERVER_PORT, SERVER_ROLE, SERVER_TOPIC

if len(sys.argv) < 4:
    print("Usage: python main.py <server_host> <server_port> <role> <topic>")
#     sys.exit(1)

host = sys.argv[1] if len(sys.argv) > 1 else SERVER_HOST
port = int(sys.argv[2] if len(sys.argv) > 2 else SERVER_PORT)
role = sys.argv[3] if len(sys.argv) > 3 else SERVER_ROLE
topic = sys.argv[4] if len(sys.argv) > 4 else SERVER_TOPIC

if __name__ == "__main__":
    client = Client(server_host=host, server_port=port , role=role, topic=topic)
    client.start()
