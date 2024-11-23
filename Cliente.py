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
auth = 0

#####Main Loop#####
while True:
    if porta > 5:
        socket_cliente.close()
        break

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
        dados = receive_message(socket_cliente)

        if dados is None:
            print('Mensagem inválida')
            break
        
        porta = dados['porta']
        auth = dados['autorização']

        if auth:
            porta = (porta + 1)
            print('acesso cedido')
        else:
            print('acesso negado')
    elif tipo == 2:
        username = input("digite seu nome de usuário: ")
        send_message(socket_cliente, porta, auth, tipo, credenciais, username)
        dados = receive_message(socket_cliente)

        if dados is None:
            print('Mensagem inválida')
            break
        
        nome = dados['nome']
        creds = dados['credencial']
        auth = dados['autorização']

        if auth:
            print(f'Seu nome: {nome}; Sua credencial: {creds}')
        else:
            print(f'erro de cadastro')
        



