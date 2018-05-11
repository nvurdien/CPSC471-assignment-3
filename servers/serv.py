import random
import sys
from pathlib import Path
from socket import *
import os
from time import sleep

HOST = 'localhost'
backlog = 5


def get_open_port():
    return random.randint(10000, 60000)


def perform(client, addr):
    done = False
    while not done:
        print("accepting from", addr)
        combined = client.recv(4096).decode()
        if combined.strip().lower() in ['quit', '']:
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
            my_file = Path("./" + filename)
            if my_file.exists():
                data = ('the file ' + filename + ' does exist in this directory').encode()
                client.send(data)
                print(data)
                ss = socket(AF_INET, SOCK_STREAM)
                sleep(1)
                ss.connect((HOST, port))
                with open(filename) as sendFile:
                    data = sendFile.read(4096).encode()
                    while data:
                        ss.send(data)
                        data = sendFile.read(4096).encode()
                ss.close()
            # if not outputs that it can't find the file
            else:
                data = ('the file ' + filename + ' does not exist in this directory, please try again').encode()
                client.send(data)
                print(data)
                continue
        elif command == 'put':
            # then prepares to receive file from server
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.bind((HOST, port))
            clientSocket.listen(backlog)
            client, addr = clientSocket.accept()
            with open(filename, 'wb') as f:
                print('receiving data ...')
                while True:
                    data = client.recv(4096)
                    if not data:
                        break
                    f.write(data)
            clientSocket.close()
            # close file once done writing
            f.close()
    print('Server is closed')
    return addr


def main():
    PORT = int(sys.argv[1])

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
            my_file = Path("./" + filename)
            if my_file.exists():
                data = ('the file ' + filename + ' does exist in this directory').encode()
                client.send(data)
                print(data)
                ss = socket(AF_INET, SOCK_STREAM)
                sleep(1)
                ss.connect((HOST, port))
                with open(filename) as sendFile:
                    data = sendFile.read(4096).encode()
                    while data:
                        ss.send(data)
                        data = sendFile.read(4096).encode()
                ss.close()
            # if not outputs that it can't find the file
            else:
                data = ('the file ' + filename + ' does not exist in this directory, please try again').encode()
                client.send(data)
                print(data)
                continue
        elif command == 'put':
            # then prepares to receive file from server
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.bind((HOST, port))
            clientSocket.listen(backlog)
            client, addr = clientSocket.accept()
            with open(filename, 'wb') as f:
                print('receiving data ...')
                while True:
                    data = client.recv(4096)
                    if not data:
                        break
                    f.write(data)
            clientSocket.close()
            # close file once done writing
            f.close()
    serverSocket.close()
    print('Server is closed')


if __name__ == '__main__':
    main()