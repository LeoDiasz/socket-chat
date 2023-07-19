from socket import *
import PySimpleGUI as sg
import threading

from utils import removeValues

hostConnect = "localhost"
portConnect = 5011

messagePatternConnect = f"{hostConnect}:{portConnect}"
messagePatternEndConnect = "Conexão encerrada com o servidor!"
messageStop = "sair"
optionsClients = []


class ChatClient:
    def __init__(self, client):
        self.event = ""
        self.window = ""
        self.value = ""
        self.client = client

    def main(self):
        sg.theme('Reddit')

        layout = [[sg.Text('Saida', size=(5, 1)), sg.Button("Limpar tela", size=(10, 0), button_color=(sg.BLUES[0], "white"))],
                  [sg.Output(size=(134, 15), font='Helvetica 10', key="output")],
                  [sg.Button("Mural", size=(10, 2)), sg.Button("BroadCast", size=(10, 2), disabled=True),
                   sg.Button("MultiCast", size=(10, 2), disabled=True),
                   sg.Listbox([], size=(20, 2), disabled=True, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, key="listOptions")],
                  [sg.ML(size=(80, 5), enter_submits=True, key='query', do_not_clear=False, focus=True),
                   sg.Button("Limpar", size=(10, 2), button_color=("white", sg.BLUES[0])),
                   sg.Button('Enviar', size=(10, 2), button_color=("white", sg.BLUES[0]), bind_return_key=True)]]

        window = sg.Window('Interface Chat', layout,
                           default_element_size=(30, 2),
                           font=('Helvetica', ' 13'),
                           default_button_element_size=(8, 2),
                           return_keyboard_events=True, finalize=True, enable_close_attempted_event=True)

        self.window = window
        communicationType = ""

        thread1 = threading.Thread(target=receiveMessages, args=[self.client, window])
        thread1.start()

        while True:
            event, value = window.read()

            if len(optionsClients) > 0:
                window["MultiCast"].update(disabled=False)
                window["BroadCast"].update(disabled=False)
            else:
                window["MultiCast"].update(disabled=True)
                window["BroadCast"].update(disabled=True)

            try:
                if event == "Mural":
                    communicationType = "mural"
                    print("Mural Sistema\nDigite uma mensagem:")
                    window["listOptions"].update(optionsClients, disabled=True)
                elif event == "BroadCast":
                    window["listOptions"].update(optionsClients, disabled=True)
                    communicationType = "broadcast"
                    print("Broadcast Sistema\nDigite uma mensagem:")
                elif event == "MultiCast":
                    communicationType = "multicast"
                    print("Multicast Sistema\nDigite uma mensagem e selecione os clientes para envio")
                    window["listOptions"].update(optionsClients, disabled=False)
                elif event == "Enviar" and communicationType != "":
                    if len(value["listOptions"]) == 0 and communicationType == "multicast":
                        print("Selecione pelo menos um cliente para envio")
                        continue
                    sendMessages(self.client, communicationType, value["query"],self.window, value["listOptions"])
                    window["query"].update("")
                elif event == "Limpar":
                    window["query"].update("")
                elif event == "Limpar tela":
                    window["output"].update("")
                elif event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT and sg.popup_yes_no('Você quer realmente sair?') == 'Yes':
                    print(messagePatternEndConnect)
                    self.client.close()
                    break
                elif event == sg.WIN_CLOSED:
                    print(messagePatternEndConnect)
                    self.client.close()
                    break

            except:
                print("Não foi possivel entender sua escolha")

        window.Close()
        return

    def runThread(self):
        threading.Thread(target=self.main).start()


def main():
    socketClient = socket(AF_INET, SOCK_STREAM)

    try:
        socketClient.connect((hostConnect, portConnect))
        print("Tentando se conectar com o servidor...")
    except:
        return print(f"Não foi possível se conectar com o servidor na rota: {messagePatternConnect}")

    print(f"conectado com o servidor: {messagePatternConnect}")

    ChatClient(socketClient).main()


def sendMessages(client: socket, typeAction: str, message: str, window: sg.Window, listClient: None or [] = None):
    try:
        client.send(f"{typeAction}:{message}:{listClient}".encode("utf-8"))

        if messageStop in message.lower():
            print(messagePatternEndConnect)
            client.close()
            window.Close()
            return

        print("Mensagem enviada com sucesso")
    except:
        print("Não foi possivel enviar a mensagem")


def receiveMessages(client: socket, window: sg.Window):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")

            if "removeClient" in message:
                tag, addressClient = message.split(":", 1)

                if addressClient in optionsClients:
                    try:
                        print(f"Usuário {addressClient} foi removido")
                        optionsClients.remove(addressClient)
                        if len(optionsClients) == 0:
                            window["BroadCast"].update(disabled=True)
                            window["MultiCast"].update(disabled=True)
                            window["listOptions"].update([], disabled=True)
                    except:
                        print("Não foi possivel remover")
                    continue

            elif "saveClient" in message:
                listMessage = filter(removeValues, message.split("-"))

                for messageClient in listMessage:
                    tag, addressClient = messageClient.split(":", 1)
                    if (addressClient in optionsClients):
                        continue
                    print(f"Usuario {addressClient} online")
                    optionsClients.append(addressClient)

                window["BroadCast"].update(disabled=False)
                window["MultiCast"].update(disabled=False)
                window["listOptions"].update([optionsClients])
                continue

            print(f"{message}")

        except:
            client.close()
            break


main()
