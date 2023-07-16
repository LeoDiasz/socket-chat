from socket import *
import threading

hostConnect = "localhost"
portConnect = 5011

messagePatternConnect = f"{hostConnect}:{portConnect}"
messagePatternEndConnect = "Conexão encerrada com o servidor!"
messageStop = "sair"
optionsClients = []


def main():
    socketClient = socket(AF_INET, SOCK_STREAM)

    try:
        socketClient.connect((hostConnect, portConnect))
        print("Tentando se conectar com o servidor...")
    except:
        return print(f"Não foi possível se conectar com o servidor na rota: {messagePatternConnect}")

    print(f"conectado com o servidor: {messagePatternConnect}")

    thread1 = threading.Thread(target=receiveMessages, args=[socketClient])
    thread1.start()
    menuOptions(socketClient)


def menuOptions(client: socket):
    while True:
        try:
            options = "\nDigite uma das opções: \n 1 - Enviar somente para o mural \n 2 - Enviar para todos os clientes \n 3 - Enviar para clientes selecionados \n 4 - Sair\n"

            choice = input(options)

            if choice == "1":
                sendMessages(client, "mural")
            elif choice == "2":
                if len(optionsClients) == 0:
                    print("Não existe cliente para enviar")
                    continue

                sendMessages(client, "broadcast")
            elif choice == "3":
                if len(optionsClients) == 0:
                    print("Não existe cliente para enviar")
                    continue
                sendForSelectedClients(client)
            elif choice == "4" or choice.lower() == "sair":
                print(messagePatternEndConnect)
                client.close()
                break
        except:
            print("Não foi possivel entender sua escolha")
            continue


def sendMessages(client: socket, typeAction: str, listClient: None or [] = None):
    while True:
        try:
            message = input("\nDigite uma mensagem para envio:")

            client.send(f"{typeAction}:{message}:{listClient}".encode("utf-8"))

            if messageStop in message.lower():
                print(messagePatternEndConnect)
                client.close()
                break

            print("Mensagem enviada com sucesso")
        except:
            print("Não foi possivel enviar a mensagem")
            client.close()
            continue
        finally:
            choice = comeBack()

            if choice is True:
                break


def sendForSelectedClients(client: socket):
    listChoice = choiceClients()

    if len(listChoice) == 0:
        return

    sendMessages(client, "multicast", listChoice)


def removeValues(value):
    if value == "":
        return False
    else:
        return True
def receiveMessages(client: socket):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")

            if "removeClient" in message:
                tag, addressClient = message.split(":", 1)

                if addressClient in optionsClients:
                    try:
                        print(f"Usuário {addressClient} foi removido")
                        optionsClients.remove(addressClient)
                    except:
                        print("Não foi possivel remover")
                    continue

            if "saveClient" in message:
                listMessage = filter(removeValues, message.split("-"))

                for messageClient in listMessage:
                    tag, addressClient = messageClient.split(":", 1)
                    if(addressClient in optionsClients):
                        continue
                    optionsClients.append(addressClient)
                continue

            print(f"\n{message}")

        except:
            client.close()
            break

def mapOptions(option):
    host, port = option
    return f"{port}: {option}\n"


def comeBack():
    while True:
        try:
            choice = input("\nDeseja continuar?\n1 - sim\n2 - não\n")

            if choice == "1" or choice.lower() == "sim":
                return False
            elif choice == "2" or choice.lower() == "não":
                return True

            raise Exception

        except:
            print("Não entendemos sua escolha, digite novamente!")
            continue


def choiceClients():
    listClientsChoice = []
    cloneOptionsClients = optionsClients.copy()

    while True:
        try:
            removeClient = ""
            if len(cloneOptionsClients) == 0:
                print("Não existe mais opções para escolher")
                return listClientsChoice

            choice = input(f"Digite a porta da tua escolha:\n{cloneOptionsClients}\n")

            for option in cloneOptionsClients:
                if choice in option:
                    print("cliente adicionado na lista")
                    listClientsChoice.append(option)
                    removeClient = option

            if removeClient:
                cloneOptionsClients.remove(removeClient)
            else:
                raise Exception

            if comeBack() is True:
                return listClientsChoice
        except:
            print("Essa porta não existe nas opções")
            if comeBack() is True:
                return listClientsChoice
            continue



main()
