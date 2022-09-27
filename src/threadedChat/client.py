import argparse
import socket
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import sys
import os
import threading

LOCAL_HOST = "127.0.0.1"
PORT = 12345
NUM_OF_ACCEPTED_BYTES = 1024
PAYLOAD = "Hey Server"
ENCODING = "ascii" # or use 'ascii'


class Send(threading.Thread):

    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name


    def run(self):

        while True:
            msg = input(f"{self.name}: ")

            if msg.lower() == "q" or msg.lower() == "quit":
                print("Quitting")
                self.sock.sendall(bytes(f"Server: {self.name} exited.", encoding=ENCODING))
                break
            else:
                self.sock.sendall(bytes(f"{self.name}: {msg}", encoding = ENCODING))

            self.sock.close()
            sys.exit() # os._exit(0)


class Receive(threading.Thread):

    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):

        while True:
            msg = self.sock.recv(NUM_OF_ACCEPTED_BYTES)

            if msg:
                print(f"{str(msg, ENCODING)}\n{self.name}:", end="")
            else:
                print("Lost connection to Server")
                self.sock.close()
                sys.exit() # os._exit()


class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(AF_INET, SOCK_STREAM)

    def start(self):
        # connects to the specific address of the server
        self.sock.connect((self.host, self.port))
        print(f"Connected to {self.host}:{self.port}\n")

        name = input("Enter Name:\n\t-->$ ")

        send = Send(self.sock, name)
        receive = Receive(self.sock, name)

        send.start()
        receive.start()

        self.sock.sendall(bytes(f"Server: {name} joined", encoding= ENCODING))
        print(f"{name}", end="")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Server')
    parser.add_argument(
        'host',
        help='Interface the server listens at'
    )
    parser.add_argument(
        '-p',
        metavar='PORT',
        type=int,
        default=1060,
        help='TCP port (default 1060)'
    )

    args = parser.parse_args()

    client = Client(args.host, args.p)
    client.start()