import random
import sys
from socket import *
from os import listdir
from os.path import isfile, join
from time import sleep


def get_open_port():
    return random.randint(10000, 60000)


HOST = sys.argv[1]
PORT = int(sys.argv[2])
backlog = 1

print('Welcome to my FTP')
print('Commands:')
print('\tget - requests a file from the server')
print('\tput - uploads a file to the server')
print('\tls - list files server side')
print('\tlls - list files on your side')
print('\thelp - sees this list again')

command = ''
commandSocket = socket(AF_INET, SOCK_STREAM)
commandSocket.connect((HOST, PORT))

while command.strip().lower() != 'quit':
    command = ''
    filename = ''
    combined = input('ftp > ')

    # checks if there are more than 2 elements
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

    if command in ['ls', 'put', 'get']:
        # checks if there is a filename
        if filename == '' and command in ['put', 'get']:
            print('filename required for', command, 'commands')
            continue
        data = 0
        port = get_open_port()
        print("the port is going to be on " + str(port))
        if command in ['get'] and filename != '':
            data = (command + " " + filename + " " + str(port)).encode()
        if command in ['put'] and filename != '':
            data = (command + " " + filename + " " + str(port)).encode()
        elif command == 'ls':
            data = (command + " " + str(port)).encode()
        bytesSent = 0
        while bytesSent < len(command):
            bytesSent += commandSocket.send(data[bytesSent:])

    if command == 'quit':
        data = 'quit'.encode()
        bytesSent = 0
        while bytesSent < len(command):
            bytesSent += commandSocket.send(data[bytesSent:])

    # downloads file from server
    if command == 'get':
        print("opening socket!")
        clientSocket = socket(AF_INET, SOCK_STREAM)
        print("binding socket!")
        clientSocket.bind((HOST, port))
        print("listening socket with backlog " + str(backlog))
        clientSocket.listen(backlog)
        print("accepting connection")
        client, addr = clientSocket.accept()
        # then prepares to receive file from server
        with open(filename, 'wb') as f:
            print('receiving data ...')
            while True:
                data = client.recv(4096)
                if not data:
                    break
                f.write(data)
        clientSocket.close()
        print('successfully received file ', filename, '!', sep='')
        # close file once done writing
        f.close()

    # uploads file to server
    elif command == 'put':
        # checks if file exists in client's directory
        try:
            ss = socket(AF_INET, SOCK_STREAM)
            sleep(5)
            ss.connect((HOST, port))
            with open(filename) as sendFile:
                data = sendFile.read(4096).encode()
                while data:
                    ss.send(data)
                    data = sendFile.read(4096).encode()
            ss.close()
        # if not outputs that it can't find the file
        except FileNotFoundError:
            print('the file', filename, 'does not exist in this directory, please try again')
            continue

    # lists files on server side
    elif command == 'ls':
        # checks if there is an extra parameter then tells user to try again
        if filename != '':
            print('too many parameters for command \'ls\'')
            continue
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.bind((HOST, port))
        clientSocket.listen(backlog)
        client, addr = clientSocket.accept()
        data = client.recv(4096)
        print(data.decode())
        clientSocket.close()

    # lists files client side
    elif command == 'lls':
        # checks if there is an extra parameter than tells user to try again
        if filename != '':
            print('too many parameters for command \'lls\'')
            continue
        files = [print(f) for f in listdir('./') if isfile(join('./', f))]

    # prints commands again
    elif command == 'help':
        if filename != '':
            print('too many parameters for command \'help\'')
            continue
        print('Commands:')
        print('\tget - requests a file from the server')
        print('\tput - uploads a file to the server')
        print('\tls - list files server side')
        print('\tlls - list files on your side')
        print('\thelp - sees this list again')
    else:
        print('command \'', command, '\' does not exist please try again', sep="")
commandSocket.close()
print('It was nice doing business with you! I hope to see you back!')
