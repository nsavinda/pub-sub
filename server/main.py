from server import Server
import sys
import argparse

parser = argparse.ArgumentParser(description="Server for handling client connections")
# -r, --relative-server <host>:<port>
parser.add_argument("-r", "--relative-server", type=str, help="Host and port of the relative server")
# -p, --port <port>
parser.add_argument("-p", "--port", type=int, help="Port to listen on")




port = parser.parse_args().port


# port: int = int(sys.argv[1] if len(sys.argv) > 1 else 65432)


if __name__ == "__main__":
    server = Server(port = port, relative_server = parser.parse_args().relative_server)
    server.start()