import socket
import sys

IP = input("Enter server name or IP address:")
port = int(input("Enter port:"))
if port > 65535 or port < 0:
    print("Invalid port number.")
    sys.exit()
command = (input("Enter command:"))