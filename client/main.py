from client import Client

if __name__ == "__main__":
    try:
        client = Client()
        client.start()
    except KeyboardInterrupt:
        print("Client stopped by user")