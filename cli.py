from socket import *
from os import listdir
from os.path import isfile, join

serverName = "ecs.fullerton.edu"
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName, serverPort))

print('Welcome to my FTP')
print('Commands:')
print('\tget - requests a file from the server')
print('\tput - uploads a file to the server')
print('\tls - list files server side')
print('\tlls - list files on your side')
print('\thelp - sees this list again')

command = ''
filename = ''

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

    # downloads file from server
    if command == 'get':
        # checks if there is a filename
        if filename == '':
            print('filename required for \'get\' commands')
            continue

        # sends filename to server
        bytesSent = 0
        while bytesSent != len(filename):
            bytesSent += clientSocket.send(filename[bytesSent:])

        # then prepares to receive file from server
        with open(filename, 'wb') as f:
            print('receiving data ...')
            while True:
                data = clientSocket.recv(1024)
                if not data:
                    break
                f.write(data)

        print('successfully received file ', filename, '!', sep='')
        # close file once done writing
        f.close()

    # uploads file to server
    elif command == 'put':
        # checks if there is a filename
        if filename == '':
            print('filename required for \'put\' commands')
            continue

        # checks if file exists in client's directory
        try:
            with open(filename) as sendFile:
                clientSocket.send(sendFile)

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

clientSocket.close()
print('It was nice doing business with you! I hope to see you back!')
