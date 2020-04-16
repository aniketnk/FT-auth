# TCP file tranfer with Auth

## Running
- `cd` into the repo
- Install the requirements \
	`pip3 install -r requirements.txt`
- Follow the steps below for auth, server and client

### 1. Auth Server
- This is a flask server to handle authentication. Should be run on the server machine \
	`./main.py &> /dev/null &` \
	OR \
	`python3 main.py`

### 2. Server
- This should run in the server machine \
	`(cd tcpServer && python3 server_tcp.py)`

### 3. Client
- This should be run in the client machine \
	`(cd tcpClient && python3 client_tcp.py)`