import socket
import sys

while True:
    # Take IP as input
    IP = input("Enter server name or IP address:")
    # Validate IP in family ipV4
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

temp = command.split(" > ")
filename = temp[1]

# Makes UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

addr = (IP, port)

# Tries to send command
for i in range(0,4):
    if i == 3:
        print("Failed to send command. Terminating")
    try:
        s.sendto((str(len(command))).encode('utf-8'),addr)
        s.sendto(command.encode('utf-8'), addr)
        s.settimeout(1)
        resp, addr = s.recvfrom(1024)
        if resp.decode('utf-8') == "ACK":
            print("ACK")
            break
    except socket.timeout:
        pass

# Receives response


