import sys
from socket import *
import os
import serv

HOST = 'localhost'
PORT = int(sys.argv[1])
backlog = 5


done = False
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen(backlog)
print("The server is ready to receive")

process_list = {}

i = 0

while True:
    client, addr = serverSocket.accept()
    pid = os.fork()
    if pid == 0:
        print("\nconnection successful with client " + str(i) + str(addr) + "\n")
        serv.perform(client, addr)
        break  # fix here!
    else:
        i += 1
