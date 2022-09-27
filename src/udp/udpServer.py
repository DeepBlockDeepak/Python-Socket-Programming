import socket
from socket import AF_INET, SOCK_DGRAM

LOCAL_HOST = "127.0.0.1"
port = 12345
NUM_OF_ACCEPTED_BYTES = 1024
NUM_WAITING_CONNECTIONS = 10
HI_CLIENT_MSG = "Hi there, Client!"

serverSocket = socket.socket(family=AF_INET, type=SOCK_DGRAM)
serverSocket.bind((LOCAL_HOST, port))

msg_num = 0
while True:
    data, clientAddr = serverSocket.recvfrom(NUM_OF_ACCEPTED_BYTES)
    print(f"Data from Client: {str(data, encoding='utf-8')}")

    msg_num += 1
    message = bytes("Hi there Client " + str(msg_num), "utf-8")

    serverSocket.sendto(message, clientAddr)

serverSocket.close()
