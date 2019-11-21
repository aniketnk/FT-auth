import socket
import sys, os, requests

serverName = input('Enter server IP[localhost]: ') or "127.0.0.1"
serverPort = int(input('Enter port number[7005]: ') or 7005)
authServerPort = int(input('Enter auth Server port: [5000]: ') or 5000)
baseUrl = "http://" + serverName + ":" + str(authServerPort)
token = "token"

def doSignIn(cred = False):
    global token 

    if not cred:
        username = input("Username: ") or "user"
        password = input("Password: ") or "password"
        cred = (username, password)
    
    res = requests.post(baseUrl+"/signIn", json={"username": cred[0], "password": cred[1]})
    if res.status_code != 200:
        print("Error: ", res.text)
        return False

    token = res.text
    print("SignedIn \n[token: ", token + ']\n(Enter to continue)')
    input()
    return True

def doSignUp():
    username = input("Username: ") or "user"
    password = input("Password: ") or "password"
    name = input("name: ") or "name"
    res = requests.post(baseUrl+"/signUp", json={"username": username, "password": password, "name": name})
    
    # print("SENT\n\n", res, res.text)
    if res.status_code == 200:
        return (username, password)
    
    print("Error:", res.text)
    return False

def main():
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

if __name__ == "__main__":
    
    # main()    #To test only tcp server

    while(True):
        choice = int(input("\nMenu\n1. Sign In\n2. Sign Up\n >"))
        result = False
        if choice==1:
            result = doSignIn()

        else:
            cred = doSignUp()
            if cred:
                result = doSignIn(cred)

        if result:
            main()