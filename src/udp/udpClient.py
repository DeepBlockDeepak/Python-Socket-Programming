import socket
from socket import AF_INET, SOCK_DGRAM

LOCAL_HOST = "127.0.0.1"
port = 12345
NUM_OF_ACCEPTED_BYTES = 1024
NUM_WAITING_CONNECTIONS = 10
HI_SERVER_MSG = "Hi, Server!"

clientSocket = socket.socket(family=AF_INET, type=SOCK_DGRAM)
clientSocket.sendto(bytes(HI_SERVER_MSG, "utf-8"), (LOCAL_HOST, port))

data, serverAddr = clientSocket.recvfrom(NUM_OF_ACCEPTED_BYTES)

print(f"Server : {str(data, encoding='utf-8')}")

clientSocket.close()
