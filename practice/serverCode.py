from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(('', serverPort))

serverSocket.listen(1)

print("The server is ready to receive")

while 1:
    connectionSocket, addr = serverSocket.accept()

    tmpBuffer = ''

    data = connectionSocket.recv(40)

    while len(data) != 40:
        tmpBuffer = connectionSocket.recv(40)
        if not tmpBuffer:
            break

        data += tmpBuffer

    print(data)

    connectionSocket.close()
