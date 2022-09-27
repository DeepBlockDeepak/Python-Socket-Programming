import socket
from socket import AF_INET, SOCK_STREAM
import sys

LOCAL_HOST = "127.0.0.1"
port = 12345
NUM_OF_ACCEPTED_BYTES = 1024
NUM_WAITING_CONNECTIONS = 10
HI_CLIENT_MSG = "Hi there, Client!"

# specify port number here?
serverSocket = socket.socket(family=AF_INET, type=SOCK_STREAM)
serverSocket.bind((LOCAL_HOST, port))
serverSocket.listen(NUM_WAITING_CONNECTIONS)

while True:
    print("Waiting to connect")
    clientSocket, clientAddr = serverSocket.accept()
    print(f"Accepted Client on {clientAddr}")

    msg_to_client_num = 0

    while True:
        data = clientSocket.recv(NUM_OF_ACCEPTED_BYTES)

        if not data or str(data, encoding="utf-8") == "END":  # data.decode()
            break
        print(f"Received from Client: {str(data, encoding='utf-8')}")

        try:
            msg_to_client_num += 1
            send_to_client = HI_CLIENT_MSG + str(msg_to_client_num)
            clientSocket.send(send_to_client.encode(encoding="utf-8"))  # bytes(HI_CLIENT_MSG, "utf-8")

        except:
            print("User exited program")

    clientSocket.close()

serverSocket.close()