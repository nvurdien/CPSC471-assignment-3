import sys
from socket import *
import os
from time import sleep

HOST = 'localhost'
PORT = int(sys.argv[1])
backlog = 5

# serverID = socket.gethostbyname(socket.gethostname())
# info = 'SERVER ID: {} port: {}'.format(serverID, PORT)
# print(info)

done = False
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen(backlog)
print("The server is ready to receive")

client, addr = serverSocket.accept()

while not done:
    print("accepting")
    combined = client.recv(4096).decode()
    if combined.strip().lower() == 'quit':
        done = True
        continue
    command = ''
    filename = ''
    if len(combined.split()) > 2:
        # tries to split into 2 variables
        try:
            command, filename, port = combined.split()
            command = command.strip().lower()
            filename = filename.strip().lower()
            port = int(port.strip())

        # if not lets user know there are too many values
        except ValueError:
            print('too many parameters')
            continue
    else:
        command, port = combined.split()
        command = command.strip().lower()
        port = int(port.strip())

    print(combined)

    if command == 'ls':
        arr = os.listdir("./")
        data = ''
        for d in arr:
            data += d + '\n'
        data = data.encode()
        ss = socket(AF_INET, SOCK_STREAM)
        sleep(1)
        ss.connect((HOST, port))
        ss.send(data)
    elif command == 'get':
        # checks if file exists in client's directory
        try:
            ss = socket(AF_INET, SOCK_STREAM)
            sleep(1)
            ss.connect((HOST, port))
            with open(filename) as sendFile:
                data = sendFile.read(4096).encode()
                while data:
                    ss.send(data)
                    print('Sent ', repr(data))
                    data = sendFile.read(4096).encode()
            ss.close()
        # if not outputs that it can't find the file
        except FileNotFoundError:
            data = ('the file ' + filename + ' does not exist in this directory, please try again').encode()
            client.send(data)
            continue
    elif command == 'put':
        # then prepares to receive file from server
        with open(filename, 'wb') as f:
            print('receiving data ...')
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.bind((HOST, port))
            clientSocket.listen(backlog)
            client, addr = clientSocket.accept()
            while True:
                data = client.recv(4096)
                if not data:
                    break
                f.write(data)
            clientSocket.close()
        data = ('successfully received file ' + filename + '!').encode()
        bytesSent = 0
        while bytesSent != len(data):
            bytesSent += client.send(data[bytesSent:])
        # close file once done writing
        f.close()
serverSocket.close()
print('Server is closed')
