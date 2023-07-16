from socket import *
import threading
from Interface import *



listMessages = []
hostConnect = "localhost"
portConnect = 5007

messagePaternConnect = f"{hostConnect}:{portConnect}"
messageStop = "sair"
optionsClients = []

def main():
    socketClient = socket(AF_INET, SOCK_STREAM)

    try:
        socketClient.connect((hostConnect, portConnect))
        print("Tentando se conectar com o servidor...")
    except:
        return print(f"Não foi possível se conectar com o servidor na rota: {messagePaternConnect}")

    print(f"conectado com o servidor: {messagePaternConnect}")

    thread1 = threading.Thread(target=receiveMessages, args=[socketClient])
    thread2 = threading.Thread(target=sendMessages, args=[socketClient])
    # thread3 = threading.Thread(target=listenOptionsClients, args=[socketClient])

    thread1.start()
    thread2.start()
    # thread3.start()


# def listenOptionsClients(socketClient: socket):
#     while True:
#         try:
#             message = socketClient.recv(1024)
#
#             print("listen", message)
#             if (message is list):
#                 optionsClients = message
#         except:
#             break
#
#     socketClient.close()


def sendOnlyMural(client: socket):
    while True:
        try:
            events, values = windowSendMessages.read()

            if (events == sg.WINDOW_CLOSED):
                break

            if (events == "Enviar"):
                if(values["inputSend"] == ""):
                    continue

                message = values["inputSend"]

                client.send(message.encode("utf-8"))

                if(message in message.lower()):
                    print("Conexão encerrada com o servidor!")
                    break
        except:
            pass

def sendForAllClients():
    pass

def SendForSelectedClients():
    pass

def sendMessages(client: socket):
    while True:
        try:
            events, values = windowChoice.read()

            if(events == sg.WINDOW_CLOSED):
                break

            print(events, values)
            if(events == "sendChoice"):
                if(values["choice"] == "1"):
                    sendOnlyMural(client)
                    windowSendMessages.close()
                elif(values["choice"] == "2"):
                    pass
                elif(values["choice"] == "sair"):
                    pass
                else:
                    continue
            # client.send(message.encode("utf-8"))
            #
            # if(messageStop in message.lower()):
            #     print("Conexão encerrada com o servidor!")
            #     break

        except:
            print("\nNão foi possivel entender sua solicitação")
            return
    client.close()
def receiveMessages(client: socket):
    while True:
        try:
            events, values = windowChat.read()
            message = client.recv(1024).decode("utf-8")
            listMessages.append((message))
            windowChat["chat"].update(listMessages)

            print(f"\n{message}")


        except:
            client.close()
            break
main()