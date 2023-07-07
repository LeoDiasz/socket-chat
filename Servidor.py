from socket import *
import threading

messageCloseConnection = "tchau"
messageReturnCloseConnection = "Conexão encerrada!".encode('utf-8')
def Servidor(connection, address):
        
    while True:
        print("Servidor na escuta....")

        while True:
            msgRcv = connection.recv(1024).decode('utf-8')
            print("Cliente disse: ", msgRcv)

            if(messageCloseConnection in msgRcv.lower()):
                print("Conexão finalizada com cliente", address)
                connection.send(messageReturnCloseConnection)
                # msgSend = input("Servidor diz: ")
                break

            # if(messageCloseConnection in msgSend.lower()):
            #     print("Conexão finalizada com cliente", address)
            #     connection.send(messageReturnCloseConnection)
            #     connection.send(msgSend.encode('utf-8'))
            #     break

        connection.close()


        

# myHost = "localhost"
# myPort = 50007

# socketServer = socket(AF_INET, SOCK_STREAM)
# #apos criacao do objeto socket - crio o bind da comunicacao
# socketServer.bind((myHost, myPort))

#Servidor ou cliente dizer tchau, encerrar servidor


ports = [50007,  50008]


for port in ports:
    socketServer = socket(AF_INET, SOCK_STREAM)
    #apos criacao do objeto socket - crio o bind da comunicacao
    print(port)
    socketServer.bind(("192.168.5.46", port))
    socketServer.listen(1)
    connection, address = socketServer.accept()
    thread2 = threading.Thread(target=Servidor, args=(connection,address))
    # Iniciando a thread
    thread2.start()

    # # Aguardando a thread terminar
    # thread.join()
    
    
        

       


