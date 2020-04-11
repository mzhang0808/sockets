import socket
import time
import sys

def testConnection(s, addr):
    # Test if connection successful
    try:
        # Random packet to see if connection established
        s.sendto("bigmac".encode('utf-8'), addr)
        s.settimeout(1)
        data, addr = s.recvfrom(1024)
        if data.decode('utf-8') == "bigmac":
            s.settimeout(None)
            return True
    # Message failed to even send
    except socket.error:
        print("Could not connect to server")
        s.settimeout(None)
        return False
    # No "ACK" received
    except socket.timeout:
        print("Could not connect to server")
        s.ssettimeout(None)
        return False

def sendCommand(command, s, addr):
    # Tries to send command
    for i in range(0,4):
        if i == 3:
            print("Failed to send command. Terminating")
            return False
        try:
            # Send size first
            s.sendto((str(len(command))).encode('utf-8'),addr)
            s.sendto(command.encode('utf-8'), addr)
            # Set timeout to receive "ACK" from server
            s.settimeout(1)
            deadline = time.time() + 1.0
            resp, addr = s.recvfrom(1024)
            while(resp.decode('utf-8') != "ACK"):
                # Means no "ACK" received
                if(time.time() >= deadline):
                    raise socket.timeout
                # Update socket timeout
                s.settimeout(deadline - time.time())
                resp, addr = s.recvfrom(1024)
            s.settimeout(None)
            return True
        except socket.timeout:
            pass
        s.settimeout(None)

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
    if port > 65535 or port < 0:
        print("Invalid port number.")
        return False
    return True

def receiveOutput(s, addr, filename):
    # Receives total length of file
    total_length, addr = s.recvfrom(1024)

    if total_length.decode('utf-8') == "Did not receive response.":
        print("Did not receive response.")
        return False

    # Take length of segment and text in segment
    total_length = int(total_length.decode('utf-8'))
    length, addr = s.recvfrom(1024)
    # Checks that size of command received matches length of command
    try:
        s.settimeout(0.5)
        deadline = time.time() + 0.5
        l, addr = s.recvfrom(1024)
        while(int(len(l.decode('utf-8'))) != int(length.decode('utf-8'))):
            # Break if timeout exceeded
            if(time.time() >= deadline):
                    raise socket.timeout
            s.settimeout(deadline - time.time())
            l, addr = s.recvfrom(1024)
        s.settimeout(None)
    except socket.timeout:
        print("Did not receive response.")
        s.settimeout(None)
        return False

    # Open file for writing
    f = open(filename, 'w')
    f.write(l.decode('utf-8'))
    counting_length = int(length.decode('utf-8'))

    # Send ACK
    s.sendto("ACK".encode('utf-8'), addr)

    # While the entire file has not been sent (by checking lengths received)
    while(total_length!=counting_length):
        try:
            # Sets timeout of 0.5 s to receive a length, then 0.5s after to receive
            # a message
            s.settimeout(0.5)
            # Receive length
            length, addr = s.recvfrom(1024)
            deadline = time.time() + 0.5
            l, addr = s.recvfrom(1024)
            # Wait for a segment that matches length received previously
            while(int(length.decode('utf-8')) != len(l.decode('utf-8'))):
                # Break if timeout exceeded
                if(time.time() >= deadline):
                    raise socket.timeout
                s.settimeout(deadline - time.time())
                l, addr = s.recvfrom(1024)
            # Send back an "ACK"
            s.sendto("ACK".encode('utf-8'), addr)
            s.settimeout(None)
        # Catch the timeout error
        except socket.timeout:
            print("Did not receive response.")
            s.settimeout(None)
            f.close()
            return False
        f.write(l.decode('utf-8'))
        # Increment counting_length
        counting_length += int(length.decode('utf-8')) 
    f.close()
    s.close()
    print("File ", filename, " saved.")
    return True     

def main():
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

    # Input Command 
    command = (input("Enter command:"))

    if command.find(" > ") == -1:
        command = command + " > " + command + ".txt"

    temp = command.split(" > ")
    filename = temp[1]

    # Makes UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    addr = (IP, port)

    # Test connection
    if not testConnection(s, addr):
        sys.exit()

    # Send command
    if not sendCommand(command, s, addr):
        sys.exit()

    if not receiveOutput(s, addr, filename):
        sys.exit()

if __name__ == '__main__':
    main()