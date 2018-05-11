from threading import Thread
import sys
from socket import *
import serv

HOST = 'localhost'
PORT = int(sys.argv[1])
backlog = 5

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen(backlog)
print("The server is ready to receive")
thread_list = []

while True:
    c, addr = serverSocket.accept()     # Establish connection with client.
    thread = Thread(target=serv.perform, args=(c, addr))
    thread_list.append(thread)
    thread.start()
