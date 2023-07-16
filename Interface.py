from PySimpleGUI import PySimpleGUI as sg


sg.theme("Reddit")

layoutChoice = [
    [sg.Text("Escolha uma das opções: \n 1 - Enviar somente para o mural \n 2 - Enviar para todos os clientes \n 3 - Enviar para clientes selecionados \n 4 - Sair")],
    [sg.Input(key="choice", size=(100, 1))],
    [sg.Button("Enviar", key="sendChoice", size=(100, 1))]
]

layoutChat = [[sg.Text("Sistema de chat:")], [sg.Text("", key="chat")]]
layoutSendMessages = [[sg.Text("Digite a mensagem"), [sg.Input(key="inputSend", size=(20,1))]], [sg.Button("Enviar")]]


windowChoice = sg.Window("Tela Cliente", layoutChoice)
windowChat = sg.Window("Chat", layoutChat)
windowSendMessages = sg.Window("Para mural", layoutSendMessages)