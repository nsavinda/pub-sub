# Pub-Sub


## Server 

### Run

```bash
cd server
python main.py <port>
```
example:

```bash
python main.py 5000
```

Add 2nd server

```bash
python main.py <port> -r <previous server ip>:<previous server port>
```

example:

```bash
python main.py 5001 -r 127.0.0.1:5000
```

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