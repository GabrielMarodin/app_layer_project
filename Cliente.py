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
LIMITE = 5
ip = '127.0.0.1' #localhost
port = 49152
addr = (ip,port)
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
socket_cliente.connect(addr)
if len(sys.argv)>1:
    porta = int(sys.argv[1])
else:
    porta = 1

#####Main Loop#####
while True:

    if porta > LIMITE:
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

    while True:
            username = input("digite seu nome de usuário: ")
            if any(char.isdigit() for char in username):
                print('Nome não pode conter números')
            else:
                break

    credencial = int(input("Digite sua credencial: ")) if tipo == 1 else 0

    send_message(socket_cliente, porta, 0, tipo, credencial, username)

    dados = receive_message(socket_cliente)
    if dados is None:
        print('Mensagem do servidor inválida')
        continue

    porta = dados['porta']
    auth = dados['autorização']
    nome = dados['nome']
    credencial = dados['credencial']

    if auth:
        if tipo == 1:
            print(f'Abrindo porta {porta}...')
        else:
            print('Cadastro bem sucedido')
            print(f'Seu nome: {nome}; Sua credencial: {credencial}')
    else:
        print('acesso negado')

send_message(socket_cliente, porta, auth, tipo, 500, nome)
socket_cliente.close()



