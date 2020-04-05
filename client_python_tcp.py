import sys
import socket

while True:
    # Take IP as input
    IP = input("Enter server name or IP address:")
    # Validate IP
    try:
        socket.inet_aton(IP)
        break
    except socket.error:
        print("Could not connect to server")

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
       

# Input Command (MUST be in the form [command] with no extra spaces or chars)
command = (input("Enter command:"))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Try connection to given IP and Port - if server not listening on same port, exit
try:
    s.connect((IP, port))
except Exception:
    print("Could not connect to server.")
    sys.exit()

# Send the command to server 
s.send(command.encode('utf-8'))

# Receive stream of data back
l = s.recv(1024)
filename = command + ".txt"

# Check first line sent from server [either error message or first line from file]
firstLine = l.decode('utf-8')
# Error - no response from server
if firstLine == "Did not receive response.":
    print("Did not receive response.")
    sys.exit()

# Write to local file
f = open(filename, 'w')

# Write stream to a .txt file
while (l):
    f.write(l.decode('utf-8'))
    l = s.recv(1024)

# Finished reading file
f.close()
print ("File ", filename, " saved.")
s.close()                # Close the connection


