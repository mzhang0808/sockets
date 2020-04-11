import subprocess
import socket
import time
import sys
import os

PORT = 3000

def receiveCommand(s, addr):
    # Receive command with buffer size 1024
    data, addr = s.recvfrom(1024)
    try:
        # Set 0.5 ms timeout/deadlien 
        s.settimeout(0.5)
        deadline = time.time() + 0.5
        cmd, addr = s.recvfrom(1024)
        # Wait for valid command matching length (size) previously sent
        while(int(data.decode('utf-8')) != len(cmd.decode('utf-8'))):
            # Means no command matching size was sent
            if(time.time() >= deadline):
                raise socket.timeout
            # Update socket timeout
            s.settimeout(deadline - time.time())
            cmd, addr = s.recvfrom(1024)
        s.sendto("ACK".encode('utf-8'), addr)
        s.settimeout(None)
        return cmd
    except socket.timeout:
        print("Failed to receive instructions from the client.")
        s.settimeout(None)
        return "Failed to receive instructions from the client."

def transferFile(s, addr):
    # Open file that command's output was stored in
    f = open("output.txt", 'r')
    l = f.read(1024)
    
    s.sendto((str(os.path.getsize("output.txt"))).encode('utf-8'), addr)

    flag = False
    # Read output back to client (potential multiple segments if size(line) > 1024)
    while(l):
        i=0
        while(i < 3):
            try:
                # send length of message
                length = (str(len(l)).encode('utf-8'))
                s.sendto(length, addr)
                # send actual message
                s.sendto(l.encode('utf-8'),addr)
                s.settimeout(1)
                deadline = time.time() + 1.0
                resp, addr = s.recvfrom(1024)
                # wait for ACK - given 0.5 s timer
                while(resp.decode('utf-8') != "ACK"):
                    # Deadline passed - means no "ACK" received
                    if(time.time() >= deadline):
                        raise socket.timeout
                    s.settimeout(deadline-time.time())
                    resp, addr = s.recvfrom(1024)
                s.settimeout(None)
                break
            except socket.timeout:
                s.settimeout(None)
            i+=1
        if(i == 3):
            print("File transmission failed.")
            flag = True
            break
        l = f.read(1024)
    f.close()
    if flag:
        return False
    #Tell client finished reading and shutdown the socket
    print("Successful File Transmission")
    return True

def main():
    # Creates socket instance with address family ipv4 and TCP protocol
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind socket to any machine & port 3000
    s.bind(('', PORT))

    while True:
        # test connection
        bigmac, addr = s.recvfrom(1024)
        s.sendto("bigmac".encode('utf-8'), addr)

        cmd = receiveCommand(s, addr)
        if cmd == "Failed to receive instructions from the client.":
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

        if not transferFile(s, addr):
            continue

if __name__ == '__main__':
    main()