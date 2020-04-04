import os
import socket
from _thread import *
import threading

print_lock = threading.Lock()

def new_client(c):
    while True:
        #Open command
        data = c.recv(1024)
        if not data:
            print_lock.release()
            break
        os.system(data.decode('utf-8'))
    c.close()

PORT = 3000

# Creates socket instance  with address family ipv4 and TCP protocol
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind socket to any machine & port 80
s.bind(('127.0.0.1', PORT))

s.listen()

while True:
    #Establish connection
    c, addr = s.accept()
    print_lock.acquire()
    start_new_thread(new_client, (c,))
s.close()
