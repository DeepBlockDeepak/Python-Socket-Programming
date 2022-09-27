import socket
from socket import AF_INET, SOCK_STREAM
import sys

LOCAL_HOST = "127.0.0.1"
port = 12345
NUM_OF_ACCEPTED_BYTES = 1024
payload = "Hey Server"

# specify port number here?
clientSocket = socket.socket(family=AF_INET, type=SOCK_STREAM)
clientSocket.connect((LOCAL_HOST, port))


try:
    while True:
        clientSocket.send(bytes(payload, 'utf-8'))
        data = clientSocket.recv(NUM_OF_ACCEPTED_BYTES)
        print(f"Data from server: {data}")

        more_data_option = input("Want to send more data?:\n\t--> ")
        if more_data_option.lower() == 'y':
            payload = input("Enter payload:\n\t-->$ ")
        else:
            break



except KeyboardInterrupt as e:
    print('Exited program')

clientSocket.close()
