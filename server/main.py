from server import Server
from config import HOST  # Importing HOST from your configuration

import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    server = Server(host=HOST, port=port)  # Provide host argument here
    server.start()
