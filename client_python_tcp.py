import sys
import socket

def validateIP(IP):
    # Validate IP in family ipV4
    try:
        socket.inet_aton(IP)
        return True
    except socket.error:
        print("Could not connect to server.")
        return False

def validatePort(port):
    # Check that it's int
    try: 
        port = int(port)
    except Exception:
        print("Invalid port number.")
        return False
    # Check that it's in bounds
    if port > 65535 or port < 0:
        return False
    return True

def testConnection(s, IP, port):
    # Try connection to given IP and Port - if server not listening on same port, exit
    try:
        s.connect((IP, port))
        return True
    except Exception:
        print("Could not connect to server.")
        return False

def sendCommand(s, command):
    if command.find(" > ") == -1:
        command = command + " > " + command + ".txt"

    # Send the command to server 
    s.send(command.encode('utf-8'))

    # Receive stream of data back
    l = s.recv(1024)

    temp = command.split(" > ")

    filename = temp[1]

    # Check first line sent from server [either error message or first line from file]
    firstLine = l.decode('utf-8')
    # Error - no response from server
    if firstLine == "Did not receive response.":
        print("Did not receive response.")
        return False

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
    return True

while True:
    IP = input("Enter server name or IP address:")
    if validateIP(IP):
        break

while True:
    # Take port # as input
    port = input("Enter port:")
    if validatePort(port):
        port = int(port)
        break

# Input Command - can be in form "[command]" or "[command] > [filename.txt]"
command = (input("Enter command:"))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Test connection
if not testConnection(s, IP, port):
    sys.exit()

# Send command
if not sendCommand(s, command):
    s.close()


