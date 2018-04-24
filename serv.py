from socket import *
import os

HOST = ''
PORT = 12000
backlog = 5

serverID = socket.gethostbyname(socket.gethostname())
info = 'SERVER ID: {} port: {}'.format(serverID, PORT)
print(info)

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind((HOST, PORT))

serverSocket.listen(backlog)
done = False

print("The server is ready to receive")

while not done:
    client, addr = serverSocket.accept()
    data = client.recv(4096)

    if data[0] == 'ls':
        data = os.listdir("./")
        client.send(data[0])
    elif data[0] == 'get':
        # checks if file exists in client's directory
        try:
            with open(data[1]) as sendFile:
                serverSocket.send(sendFile)
        # if not outputs that it can't find the file
        except FileNotFoundError:
            print('the file', data[1], 'does not exist in this directory, please try again')
            continue
    elif data[0] == 'put':
        # then prepares to receive file from server
        with open(data[1], 'wb') as f:
            print('receiving data ...')
            while True:
                data = serverSocket.recv(4096)
                if not data:
                    break
                f.write(data)
        print('successfully received file ', data[1], '!', sep='')
        # close file once done writing
        f.close()
print('Connection to server has been closed!')
serverSocket.close()
