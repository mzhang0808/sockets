import subprocess
import socket

PORT = 3000

# Creates socket instance with address family ipv4 and TCP protocol
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind socket to any machine & port 3000
s.bind(('', PORT))

# Begin accepting connections
s.listen()

while True:
    # Receive command with buffer size 1024
    data, addr = s.recv(1024)