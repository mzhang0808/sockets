import socket
import sys

while True:
    # Take IP as input
    IP = input("Enter server name or IP address:")
    # Validate IP
    try:
        socket.inet_aton(IP)
        break
    except socket.error:
        print("Could not connect to server.")

while True:
    # Take port # as input
    port = input("Enter port:")
    # Check that it's int
    try: 
        port = int(port)
        break
    except Exception:
        print("Invalid port number.")

# Check valid port number
while port > 65535 or port < 0:
    print("Invalid port number.")
    port = input("Enter port:")
    while True:
        # Ensure inputted port is #
        try:
            port = int(port)
            break
        except Exception:
            print("Invalid port number.")

# Input Command 
command = (input("Enter command:"))

if command.find(" > ") == -1:
    command = command + " > " + command + ".txt"

# Makes UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

addr = (IP, port)
s.sendto((str(len(command))).encode('utf-8'),addr)