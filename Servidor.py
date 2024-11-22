import socket
import struct
from datetime import datetime

#####funções auxiliares#####
def unpack_message(mensagem):
    if len(mensagem) == 60:
        porta = (mensagem[0] >> 6) & 0xF
        auth = (mensagem[0] >> 4) & 0x3
        tipo = (mensagem[0] >> 2) & 0x3
        creds = struct.unpack('>H', mensagem[1:3])[0]
        timestamp = struct.unpack('>Q', b'\x00' + mensagem[3:10])[0]
        nome = mensagem[10:60].decode('utf-8', errors='ignore').rstrip('\x00')

        return porta, auth, tipo, creds, timestamp, nome
    else:
        print("Mensagem inválida")

######init#####
host = '127.0.0.1'
port = 49152
addr = (host,port)
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_servidor.bind(addr)
socket_servidor.listen()
print ('aguardando conexao')

while True:
    conn, cliente = socket_servidor.accept() #espera por conexão
    print ('conectado')
    try:
        mensagem = conn.recv(60)
        porta, auth, tipo, creds, timestamp, nome = unpack_message(mensagem)
        data = datetime.fromtimestamp(timestamp)

        print(f"porta: {porta}")
        print(f"auth: {auth}")
        print(f"tipo: {tipo}")
        print(f"creds: {creds}")
        print(f"data: {data}")
        print(f"nome: {nome}")
    finally:
        conn.close()
