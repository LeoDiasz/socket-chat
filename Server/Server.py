from socket import *
import threading

serverPort = 5011
serverHost = "localhost"

clients = []
messageStop = "sair"


def main():
    socketServer = socket(AF_INET, SOCK_STREAM)

    try:
        socketServer.bind((serverHost, serverPort))
        socketServer.listen()
        print(f"Servidor no ar na rota: {serverHost}:{serverPort}")

    except:
        return print("Não foi possivel iniciar o servidor")

    while True:
        client, address = socketServer.accept()

        print(f"cliente {convertAddress(address)} aterrissou no servidor!!")

        clients.append(convertObjectClient(client, address))

        thread1 = threading.Thread(target=sendClients)
        thread2 = threading.Thread(target=distributeMessage, args=[client, address])

        thread1.start()
        thread2.start()


def sendClients():
    for clientValue in clients:
        for clientItemInfo in clients:
            if clientItemInfo["client"] != clientValue["client"]:
                messageSend = f"saveClient:{convertAddress(clientItemInfo['address'])}-"
                clientValue["client"].send(messageSend.encode("utf-8"))


def removeClients(clientObject):
    for clientItem in clients:
        if clientItem["client"] != clientObject["client"]:
            messageSend = f"removeClient:{convertAddress(clientObject['address'])}"
            clientItem["client"].send(messageSend.encode("utf-8"))

    clients.remove(clientObject)


def distributeMessage(client: socket, address):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")

            if "mural" in message:
                mural(address, message)
            elif "broadcast" in message:
                threadBroadcast = threading.Thread(target=broadcast, args=[client, address, message])
                threadBroadcast.start()
            elif "multicast" in message:
                threadMulticast = threading.Thread(target=multicast, args=[address, message])
                threadMulticast.start()
            elif messageStop in message.lower():
                raise Exception

        except:
            deleteClientInList(convertObjectClient(client, address))
            break


def mural(address, message: str):
    try:
        listMessage = message.split(":")
        print(f"Usuário {convertAddress(address)} = {listMessage[1]}")

    except:
        print("Não foi possivel receber a mensagem")
        return


def broadcast(client: socket, address, message: str):
    splitMessage = message.split(":")

    for clientItem in clients:
        if clientItem["client"] != client:
            try:
                messageSend = f"Usuário {convertAddress(address)} = {splitMessage[1]}"
                clientItem["client"].send(messageSend.encode("utf-8"))
            except:
                deleteClientInList(clientItem)


def multicast(address, message):
    listMessage = message.split(":", 2)

    for clientItem in clients:
        if convertAddress(clientItem["address"]) in listMessage[2]:
            try:
                messageSend = f"Usuário {convertAddress(address)} = {listMessage[1]}"
                clientItem["client"].send(messageSend.encode("utf-8"))
            except:
                deleteClientInList(clientItem)


def deleteClientInList(clientObject):
    try:
        print(f"Conexão finalizada com cliente {convertAddress(clientObject['address'])}")
        threadRemoveClient = threading.Thread(target=removeClients, args=[clientObject])
        threadRemoveClient.start()
        clientObject["client"].close()
    except:
        print("Não foi possivel encerrar conexão")


def convertAddress(address):
    ip, port = address

    return f"{ip}:{port}"


def convertObjectClient(client, address):
    return {"client": client, "address": address}


main()
