import socket
from socket import AF_INET, SOCK_STREAM
import sys

try:
    # specify port number here?
    serverSocket = socket.socket(family=AF_INET, type=SOCK_STREAM)

except socket.error as e:  # might need to stringify the 'e'
    print(f"Could not create socket due to {e}")
    sys.exit()

print("\nSocket successfully created.")
target_address = input("Enter the target address:\n\t-->$ ")
target_port = int(input("Enter the port\n\t-->$ "))

try:
    serverSocket.connect((target_address, target_port))
    print(f"\nConnected to {target_address} on port {target_port}\n")
    serverSocket.shutdown(2)

except socket.error as e:  # might need to stringify the 'e'
    print(f"Failed to connect to {target_address} on port {target_port} due to {e}\n")
    sys.exit()
