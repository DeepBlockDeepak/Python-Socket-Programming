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
ENCODING = "utf-8"  # or use 'ascii'


class Send(threading.Thread):

    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):

        """
        TODO: loop over each line of the message and transmit line by line within a While loop

        """

        while True:
            #print(f"{self.name}: ")
            msg = input(f"{self.name}: ")
            sys.stdout.flush()
            # msg = sys.stdin.readline()[:-1]

            if msg.lower() == "q" or msg.lower() == "quit":
                print("Quitting")
                self.sock.sendall(bytes(f"Server: {self.name} exited.", encoding=ENCODING))
                break
            else:
                self.sock.sendall(bytes(f"{self.name}: {msg}", encoding=ENCODING))

        self.sock.close()
        sys.exit()  # os._exit(0)


class Receive(threading.Thread):

    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):

        while True:
            msg = str(self.sock.recv(NUM_OF_ACCEPTED_BYTES), encoding=ENCODING)
            # msg = self.sock.recv(NUM_OF_ACCEPTED_BYTES).decode(ENCODING)

            if msg: # TODO: don't format msg because each msg is line by line
                print(f"\n{msg}\n{self.name}: ", end="")
                #print(str(msg + "\n" + self.name + ":++ ", encoding=ENCODING))
            else:
                print("Lost connection to Server")
                self.sock.close()
                sys.exit()  # os._exit()


class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(AF_INET, SOCK_STREAM)
        self.name = None

    def start(self):
        # connects to the specific address of the server
        self.sock.connect((self.host, self.port))
        print(f"Connected to {self.host}:{self.port}\n")

        self.name = input("Enter Name:\n\t-->$ ")

        send = Send(self.sock, self.name)
        receive = Receive(self.sock, self.name)

        send.start()
        receive.start()

        self.sock.sendall(bytes(f"Server: {self.name} joined", encoding=ENCODING))
        # print(f"--{self.name}", end="")


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
