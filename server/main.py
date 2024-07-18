from server import Server
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m main <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    server = Server(port=port)
    server.start()
