import socket 
import sys
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
ip = '127.0.0.1' #localhost
port = 49152
addr = (ip,port)
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
socket_cliente.connect(addr)
if len(sys.argv)>1:
    porta = int(sys.argv[1])
else:
    porta = 1
credenciais = 0
auth = 0

#####Main Loop#####
while True:

    if porta > 5:
        break

    print(f"bem-vindo a porta {porta}\n")

    while True:
        try:
            tipo = int(input("Digite 1 para entrar e 2 para cadastrar: "))
            if tipo == 1 or tipo == 2:
                break
            else:
                print('Entrada inválida tente de novo.')
        except ValueError:
                print('Entrada inválida tente de novo.')

    if tipo == 1:
        while True:
            username = input("digite seu nome de usuário: ")
            if any(char.isdigit() for char in username):
                print('Nome não pode conter números')
            else:
                break
            
        credenciais = int(input("Digite sua credencial: "))
        send_message(socket_cliente, porta, auth, tipo, credenciais, username)
        dados = receive_message(socket_cliente)

        if dados is None:
            print('Mensagem do servidor inválida')
            continue
        
        porta = dados['porta']
        auth = dados['autorização']

        if auth:
            print(f'acesso cedido a porta {porta}')
            break
        else:
            print('acesso negado')
    elif tipo == 2:
        username = input("digite seu nome de usuário: ")
        send_message(socket_cliente, porta, auth, tipo, credenciais, username)
        dados = receive_message(socket_cliente)

        if dados is None:
            print('Mensagem do servidor inválida')
            continue
        
        nome = dados['nome']
        creds = dados['credencial']
        auth = dados['autorização']

        if auth:
            print('Cadastro bem sucedido')
            print(f'Seu nome: {nome}; Sua credencial: {creds}')
        else:
            print('Erro de cadastro')

send_message(socket_cliente, porta, auth, tipo, credenciais, '500')
socket_cliente.close()



