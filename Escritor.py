from socket import *
import threading


hostConnect = "localhost"
portConnect = 5007

messagePaternConnect = f"{hostConnect}:{portConnect}"
messageStop = "sair"

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

    thread1.start()
    thread2.start()


def sendMessages(client: socket):
    while True:
        try:
            message = input("\nDigite uma mensagem:")

            client.send(message.encode("utf-8"))

            if(messageStop in message.lower()):
                print("Conexão encerrada com o servidor!")
                client.close()
                break

        except:
            print("\nNão foi possivel enviar a mensagem")
            return

def receiveMessages(client: socket):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            print(f"\n{message}")

        except:
            client.close()
            break
main()