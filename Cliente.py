from socket import *


myHost = "192.168.5.46"
ports = 50008
messageReturnCloseConnection = "Conexão encerrada!"

socketClient = socket(AF_INET, SOCK_STREAM)
print("O cliente solicita conexao agora...")

socketClient.connect((myHost,ports))
print("Conexao solicitada!")

while True:
    msgSend = input("Cliente diz: ")
    socketClient.send(msgSend.encode('utf-8'))
    msgRcv = socketClient.recv(1024).decode('utf-8')

    if(messageReturnCloseConnection in msgRcv):
        print("Conexão finalizada no cliente")
        break

    print("Servidor disse: ", msgRcv)

socketClient.close()



