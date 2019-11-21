import socket
import sys, os

serverName = input('Enter server IP[localhost]: ') or "127.0.0.1"
serverPort = int(input('Enter port number[7005]: ') or 7005)


#in this loop, sockets open and close for each request the client makes
while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    #create socket object for client
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    clientSocket.connect((serverName,serverPort))
    print('Connected to server.')

    sentence = input('Enter a GET or SEND or LIST command: ')

    clientSocket.send(sentence.encode('utf-8'))

    if sentence == 'GET':
        fileName = input('\nEnter name of file: ')
        clientSocket.send(fileName.encode('utf-8'))
        f = open("dn_" + fileName, "wb")
        print('Receiving file..')
        l = clientSocket.recv(1024)
        while (l):
            f.write(l)
            l = clientSocket.recv(1024)
        f.close()
        print('Done receiving file')
        input()

    elif sentence == 'SEND':
        f = open(fileName,"rb")

        print('Sending file to server...')
        l = f.read(1024)
        while (l):
            clientSocket.send(l)
            l = f.read(1024)
        f.close()
        print('Done sending')
        input()
    elif sentence == 'LIST' :
        file_list = []
        #clientSocket.send("LIST".encode('utf-8'))
        print('Receiving list..')
        l = clientSocket.recv(1024).decode('utf-8')
        file_list.append(l)
        while (l):
            l = clientSocket.recv(1024).decode('utf-8')
            file_list.append(l)
        for i in file_list:
            print(i.rstrip("\n"))
        print('Done receiving list')
        input()
    clientSocket.close()
