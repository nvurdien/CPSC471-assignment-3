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

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind((HOST, PORT))

serverSocket.listen(backlog)
done = False

print("The server is ready to receive")

while not done:
    client, addr = serverSocket.accept()
    combined = client.recv(4096).decode()
    command = ''
    filename = ''
    if len(combined.split()) > 1:
        # tries to split into 2 variables
        try:
            command, filename = combined.split()
            command = command.strip().lower()
            filename = filename.strip().lower()

        # if not lets user know there are too many values
        except ValueError:
            print('too many parameters')
            continue
    else:
        command = combined.strip().lower()

    print(combined)
    print(command)
    print(filename)

    if command == 'ls':
        data = os.listdir("./")
        ss = socket(AF_INET, SOCK_STREAM)
        sleep(1)
        ss.connect((HOST, PORT + 1))
        ss.send(data)
    elif command == 'get':
        # checks if file exists in client's directory
        try:
            ss = socket(AF_INET, SOCK_STREAM)
            sleep(1)
            ss.connect((HOST, PORT+1))
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
            clientSocket.bind((HOST, PORT + 1))
            clientSocket.listen(backlog)
            client, addr = clientSocket.accept()
            while True:
                data = client.recv(4096)
                if not data:
                    break
                f.write(data)
        data = ('successfully received file ' + filename + '!').encode()
        bytesSent = 0
        while bytesSent != len(data):
            bytesSent += client.send(data[bytesSent:])
        # close file once done writing
        f.close()
serverSocket.close()
print('Server is closed')
