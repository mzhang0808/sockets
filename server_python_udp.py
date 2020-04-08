import subprocess
import socket
import sys

PORT = 3000

# Creates socket instance with address family ipv4 and TCP protocol
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind socket to any machine & port 3000
s.bind(('', PORT))

while True:
    # Receive command with buffer size 1024
    data, addr = s.recvfrom(1024)
    try: 
        s.settimeout(0.5)
        cmd, addr = s.recvfrom(1024)
        if int(data.decode('utf-8')) == len(cmd.decode('utf-8')):
            s.sendto("ACK".encode('utf-8'), addr)
    except socket.timeout:
        print("Failed to receive instructions from the client.")
        continue

    # Get command and place output in output.txt
    temp = cmd.decode("utf-8").split(" > ")
    command = temp[0] + " > output.txt"

    # Run command using a shell - ensure that errors are caught
    try:
        out = subprocess.check_output(command, shell=True)
    # Any error will mean the command did not execute successfully - send a no response message to client
    # signifying the command failed                       
    except subprocess.CalledProcessError as grepexc:
        s.sendto("Did not receive response.".encode('utf-8'),addr)
        continue

    # Open file that command's output was stored in
    f = open("output.txt", 'r')
    l = f.read(1024)
    
    # Read output back to client (potential multiple segments if size(line) > 1024)
    while(l):
        for i in range(0,4):
            if i == 3:
                print("File transmission failed.")
                break
            try:
                s.sendto((str(len(l))).encode('utf-8'), addr)
                s.sendto(l.encode('utf-8'),addr)
                s.settimeout(1)
                resp, addr = s.recvfrom(1024)
                if resp.decode('utf-8') == "ACK":
                    break
            except socket.timeout:
                pass
        l = f.read(1024)

    #Tell client finished reading and shutdown the socket
    print("Successful File Transmission")
    
