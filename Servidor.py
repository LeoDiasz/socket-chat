from socket import *
import socketserver

myHost = "localhost";
myPort = 50007;

socketServer = socket(AF_INET, SOCK_STREAM);
#apos criacao do objeto socket - crio o bind da comunicacao
socketServer.bind((myHost, myPort));
#Servidor ou cliente dizer tchau, encerrar servidor
messageCloseConnection = "tchau";
messageReturnCloseConnection = "Conexão encerrada!".encode('utf-8');


while True: ### ESTE LACO SERVE PARA O SERVIDOR PERMANECER NA ESCUTA

    socketServer.listen(1);
    print("Servidor na escuta....");
    connection, adress = socketServer.accept();

    while True:
        msgRcv = connection.recv(1024).decode('utf-8');
        print("Cliente disse: ", msgRcv);

        if(messageCloseConnection in msgRcv.lower()):
            print("Conexão finalizada com cliente", adress)
            connection.send(messageReturnCloseConnection);
            break

        msgSend = input("Servidor diz: ");

        if(messageCloseConnection in msgSend.lower()):
            print("Conexão finalizada com cliente", adress)
            connection.send(messageReturnCloseConnection);
            break
        
        connection.send(msgSend.encode('utf-8'));
    
    connection.close();