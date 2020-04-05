import subprocess
import socket


PORT = 3000

# Creates socket instance with address family ipv4 and TCP protocol
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket to any machine & port 3000
s.bind(('', PORT))

# Begin accepting connections
s.listen()

# Ensure it is always listening until empty command passed in 
# or manually terminated
while True:
    # Establish connection
    c, addr = s.accept()

    # Receive command with buffer size 1024
    data = c.recv(1024)
    cmd = data.decode('utf-8')
    cmd = cmd + " > output.txt"

    # Run command using a shell - ensure that errors are caught
    try:
        out = subprocess.check_output(cmd, shell=True)

    # Any error will mean the command did not execute successfully - send a no response message to client
    # signifying the command failed                       
    except subprocess.CalledProcessError as grepexc:                                                                                                   
        l = "Did not receive response."
        c.send("Did not receive response.".encode('utf-8'))
        break

    # Open file that command's output was stored in
    f = open('output.txt', 'r')
    l = f.read(1024)
    
    # Read output back to client (potential multiple segments if size(line) > 1024)
    while(l):
        c.send(l.encode('utf-8'))
        l = f.read(1024)
    #Tell client finished reading and shutdown the socket
    c.shutdown(socket.SHUT_RDWR)
s.close()
