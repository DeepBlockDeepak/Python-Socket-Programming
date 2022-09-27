import socket
from socket import AF_INET, SOCK_STREAM
import sys

LOCAL_HOST = "127.0.0.1"
PORT = 12345
NUM_OF_ACCEPTED_BYTES = 1024
PAYLOAD = "Hey Server"

# specify port number here?
clientSocket = socket.socket(family=AF_INET, type=SOCK_STREAM)
clientSocket.connect((LOCAL_HOST, PORT))


try:
    while True:
        clientSocket.send(bytes(PAYLOAD, 'utf-8'))
        data = clientSocket.recv(NUM_OF_ACCEPTED_BYTES)
        print(f"Data from server: {str(data, encoding='utf-8')}")

        more_data_option = input("Want to send more data?:\n\t--> ")
        if more_data_option.lower() == 'y':
            PAYLOAD = input("Enter payload:\n\t-->$ ")
        else:
            break



except KeyboardInterrupt as e:
    print('Exited program')

clientSocket.close()
