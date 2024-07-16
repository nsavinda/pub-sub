from client import Client
import sys
# from utils import ConnectionType


host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
port = int(sys.argv[2] if len(sys.argv) > 2 else 65432)

type = sys.argv[3] if len(sys.argv) > 3 else 'subscriber'

# if len(sys.argv) > 3:
#     type = sys.argv[3]
#     if type == ConnectionType.PUBLISHER.value:
#         type = ConnectionType.PUBLISHER
#     elif type == ConnectionType.SUBSCRIBER.value:
#         type = ConnectionType.SUBSCRIBER
#     else:
#         print(f"Invalid connection type: {type}")
#         exit(1)


if __name__ == "__main__":
    client = Client(server_host=host, server_port=port, type=type)
    client.start()
