import argparse
import socket
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import sys
import os
import threading
from client import Client

NUM_OF_ACCEPTED_BYTES = 1024
ENCODING = "utf-8"  # or use 'ascii'


class Server(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.connections = []  # list of ServerSocket objects which are active Clients
        self.host = host
        self.port = port

    def run(self):
        # address family and socket type
        serverSock = socket.socket(AF_INET, SOCK_STREAM)
        # allow the resuse of an old Port after disconnect without waiting
        serverSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        # bind the socket to the address
        serverSock.bind((self.host, self.port))

        serverSock.listen(8)
        print(f"Listening at: {serverSock.getsockname()}")

        while True:
            # waiting for new connection, and then returns a new connected Socket along with its address
            print("Waiting to connect")
            clientSocket, clientAddr = serverSock.accept()
            print(
                f"New connection {clientSocket.getpeername()} to {clientSocket.getsockname()} ... Address:{clientAddr}"
            )

            # make new Thread for communicating with the new client
            server_sock = ServerSocket(clientSocket, clientAddr, self)
            # start
            server_sock.start()
            # Add this active thread to all active connections
            self.connections.append(server_sock)
            print(f"Ready for messaging from {clientSocket.getpeername()}")

    # @TODO : for the chat app only
    def broadcast(self, message, source):
        for connection in self.connections:
            if connection.clientAddr != source:
                connection.send(message)

    def remove_connection(self, connection):
        self.connections.remove(connection)


class ServerSocket(threading.Thread):
    def __init__(self, clientSocket, clientAddr, server):
        super().__init__()
        self.clientSocket = clientSocket
        self.clientAddr = clientAddr
        self.server = server

    def run(self):
        # listening for data sent by the client
        while True:
            # waiting for data to arrive
            message = str(self.clientSocket.recv(NUM_OF_ACCEPTED_BYTES), encoding=ENCODING)

            if message:
                print(f"{self.clientAddr} says {message}")
                # @TODO : for the chat app only
                self.server.broadcast(message, self.clientAddr)
            # when client closes, recv() returns an empty string
            else:
                # Client closed the socket. Kill the thread
                print(f"{self.clientAddr} exited")
                self.clientSocket.close()
                server.remove_connection(self)
                return

    def send(self, message):
        # @TODO : possibly for the chat app only??? NOTE: I think this is necessary
        self.clientSocket.sendall(bytes(message, ENCODING))


def exit(server):
    while True:
        userInput = input("")
        if userInput.lower() == "q" or userInput.lower() == "quit":
            print("Closing connections")
            for connection in server.connections:
                connection.clientSocket.close()
            print("Shutting down Server")
            os._exit(0)
            #sys.exit()  # os._exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Server")
    parser.add_argument(
        "host",
        help="Interface the Server Listens at"
    )
    parser.add_argument(
        '-p',
        metavar='PORT',
        type=int,
        default=1060,
        help="TCP port (default 1060)"
    )

    args = parser.parse_args()

    server = Server(args.host, args.p)
    server.start()

    exit = threading.Thread(target=exit, args=(server,))
    exit.start()
