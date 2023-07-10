from socket import *
import threading


serverPort = 5007
serverHost = "localhost"

clients = []

messageStop = "sair"
messageCloseConnection = "Conexão encerrada com o servidor!".encode('utf-8')

def main():
    socketServer = socket(AF_INET, SOCK_STREAM)

    try:
        socketServer.bind(("localhost", 5007))
        socketServer.listen()
        print(f"Servidor no ar na rota: {serverHost}:{serverPort}")

    except:
        return print("Não foi possivel iniciar o servidor")

    while True:
        client, address = socketServer.accept()

        print(f"cliente {convertAddress(address)} aterrissou no servidor!!")

        ip, port = address
        clients.append(client)

        thread = threading.Thread(target=distributeMessage, args=[client, address])

        thread.start()


def distributeMessage(client: socket, address):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if messageStop in message.lower():
                print(f"Conexão finalizada com cliente {convertAddress(address)}")
                deleteClientInList(client)
                break

            broadcast(message, client, address)
        except:
            deleteClientInList(client)
            break

    client.close()
def broadcast(message, client, address):
    for clientItem in clients:
        if(clientItem != client):
            try:
                clientItem.send(f"Usuário {convertAddress(address)}: {message}".encode("utf-8"))
            except:
                deleteClientInList(clientItem)


def deleteClientInList(client):
    clients.remove(client)


def convertAddress(address):
    ip, port = address

    return f"{ip}:{port}"

main()