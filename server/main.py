from server import Server
import sys

port: int = int(sys.argv[1] if len(sys.argv) > 1 else 65432)


if __name__ == "__main__":
    try:
        server = Server(port = port)
        server.start()
    except KeyboardInterrupt:
        print("Server stopped by user")