import socket 
from util import send_message

#estrutura da mensagem
#   tamanho: 60 bytes
#   porta: 4 bits
#   auth: 2 bits
#   tipo: 2 bits
#   creds: 2 bytes
#   data: 7 bytes
#   nome: 50 bytes

######init#####
ip = '127.0.0.1' #localhost - endereço IP do meu próprio computador
port = 49152
addr = (ip,port)
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
socket_cliente.connect(addr)
auth = 0
porta = 0
credenciais = 0
tipo = 0

print("bem-vindo a porta 1\n")



while True:
    try:
        tipo = int(input("Digite 1 para entrar e 2 para cadastrar ou Digite 3 para sair: "))
        username = input("digite seu nome de usuário: ")
        break
    except ValueError:
            print("Entrada inválida tente de novo.\n")


if tipo == 1:
    porta = porta + 1
    credenciais = int(input("Digite sua credencial: "))
if tipo == 3:
     send_message(socket_cliente, porta, auth, tipo, credenciais, username)

send_message(socket_cliente, porta, auth, tipo, credenciais, username)

socket_cliente.close()


