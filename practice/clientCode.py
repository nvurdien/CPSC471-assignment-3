from socket import *

serverName = "ecs.fullerton.edu"
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName, serverPort))

data = "Hello World! This is a very long string."

bytesSent = 0

while bytesSent != len(data):
    bytesSent += clientSocket.send(data[bytesSent:])

clientSocket.close()
