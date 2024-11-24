import socket
import threading
from util import login
from util import unpack_message
from util import register
from util import send_message
from util import client_handling

######init#####
host = '127.0.0.1'
port = 49152
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_servidor.bind((host,port))
socket_servidor.listen(10)

print ('aguardando conexao')
######Main Loop#####
while True:
    socket_cliente, cliente = socket_servidor.accept() #espera por conexão
    print ('conectado')

    thread_cliente = threading.Thread(target = client_handling,args=(socket_cliente))
    thread_cliente.start()
