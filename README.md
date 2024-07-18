# Pub-Sub

Publisher-Subscriber model using Python. Supports for Multiple servers and clients.

## Server 

### Run

```bash
cd server
python main.py -p <port>
```
example:

```bash
python main.py -p 5000
```

Add More servers:

```bash
python main.py -p <port> -r <previous server ip>:<previous server port>
```

example:

```bash
python main.py -p 5001 -r 127.0.0.1:5000
```

```bash
python main.py -p 5002 -r 127.0.0.1:5000,127.0.0.1:5001

## Client

### Run

```bash
cd client
python main.py <host> <port> <Publisher/Subscriber> <topic>
```

example:

```bash
python main.py 127.0.0.1 5000 Publisher topic1
```