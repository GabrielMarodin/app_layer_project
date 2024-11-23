import socket
import threading
from util import login
from util import unpack_message
from util import register
from util import send_message

def client_handling(socket_cliente):

    while True:
        mensagem = socket_cliente.recv(60)

        if not mensagem:
            break

        porta, auth, tipo, creds, timestamp, nome = unpack_message(mensagem)
        
        if tipo == 1:
            estado, auth = login(creds, nome, timestamp, porta)
            #send_message(socket_servidor, porta, auth, tipo, creds, nome)
        else:
            if tipo == 2:
                estado, porta, creds = register(nome)
                #send_message(socket_servidor, porta, True, tipo, creds, nome)
            else:
                #send_message(socket_servidor, porta, True, tipo, creds, nome)
                socket_cliente.close()

    socket_cliente.close()

######init#####
host = '127.0.0.1'
port = 49152
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_servidor.bind((host,port))
socket_servidor.listen(10)

print ('aguardando conexao')

while True:
    socket_cliente, cliente = socket_servidor.accept() #espera por conexão
    print ('conectado')

    thread_cliente = threading.Thread(target = client_handling,args=(socket_cliente))
    thread_cliente.start()
