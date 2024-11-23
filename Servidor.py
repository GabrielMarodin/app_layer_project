import socket
from util import login
from util import unpack_message
from util import register
from util import send_message

######init#####
host = '127.0.0.1'
port = 49152
addr = (host,port)
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_servidor.bind(addr)
socket_servidor.listen()

while True:
    print ('aguardando conexao')
    conn, cliente = socket_servidor.accept() #espera por conexão
    print ('conectado')
    try:
        mensagem = conn.recv(60)
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
                socket_servidor.close()
        
    finally:
        conn.close()
