import sys
import socket

IP = input("Enter server name or IP address:")
port = int(input("Enter port:"))
if port > 65535 or port < 0:
    print("Invalid port number.")
    sys.exit()
command = (input("Enter command:"))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((IP, port))

s.sendall(command.encode('utf-8'))
