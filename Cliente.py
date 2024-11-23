import socket 
from util import send_message
from util import receive_message

############################
#estrutura da mensagem
#   tamanho: 60 bytes
#       porta: 4 bits
#       auth: 2 bits
#       tipo: 2 bits
#       creds: 2 bytes
#       data: 7 bytes
#       nome: 50 bytes
############################

######init#####
ip = '127.0.0.1' #localhost - endereço IP do meu próprio computador
port = 49152
addr = (ip,port)
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
socket_cliente.connect(addr)
porta = 1
credenciais = 0

#####Main Loop#####
while True:
    auth = 0
    print(f"bem-vindo a porta {porta}\n")

    while True:
        try:
            tipo = int(input("Digite 1 para entrar e 2 para cadastrar: "))
            break
        except ValueError:
                print("Entrada inválida tente de novo.\n")

    if tipo == 1:
        username = input("digite seu nome de usuário: ")
        credenciais = int(input("Digite sua credencial: "))
        send_message(socket_cliente, porta, auth, tipo, credenciais, username)
        mensagem = receive_message(socket_cliente)

        if mensagem is None:
            print('servidor não respondeu')
        else:
            porta, auth, tipo, creds, timestamp, nome = mensagem

        if auth == 1:
            porta = porta + 1
            print('acesso cedido')
        else:
            print('acesso negado')

    elif tipo == 2:
        username = input("digite seu nome de usuário: ")
        send_message(socket_cliente, porta, auth, tipo, credenciais, username)
        mensagem = receive_message(socket_cliente)

        if mensagem is None:
            print('servidor não respondeu')
        else:
            porta, auth, tipo, creds, timestamp, nome = mensagem
            print(f'Seu nome: {nome}, sua credencial: {creds}')



