import socket 
import datetime
import struct
#estrutura da mensagem
#   tamanho: 60 bytes
#   porta: 4 bits
#   auth: 2 bits
#   tipo: 2 bits
#   creds: 2 bytes
#   data: 7 bytes
#   nome: 50 bytes

#####funções auxiliares#####
def get_time():
    now = datetime.now()
    year = now.year 
    month = now.month 
    day = now.day
    hour = now.hour
    minute = now.minute
    second = now.second

    data = (year << 40) | (month << 32) | (day<<24) | (hour<<16) | (minute<<8) | second 

    return data

def pack_message(porta, auth, tipo, creds, nome):
    timestamp = int(datetime.datetime.now().timestamp())

    porta = porta & 0xF
    auth = auth & 0x3  
    tipo = tipo & 0x3   
    creds = creds & 0xFFFF
    nome = nome.encode('utf-8')[:50]
    nome = nome.ljust(50, b'\x00')

    mensagem = bytearray(60)

    packed_header = (porta << 6) | (auth << 4) | (tipo << 2)

    mensagem[0] = packed_header
    mensagem[1:3] = struct.pack('>H', creds)
    mensagem[3:10] = struct.pack('>Q', timestamp)[1:]
    mensagem[10:60] = nome[:50]

    return bytes(mensagem)

def send_message(socket):
    
    mensagem = pack_message(porta, auth, tipo, credenciais, username)

    socket.sendall(mensagem)
##########

######init#####
#inicia a conexão com o servidor e manda a primeira mensagem que é sempre igual

ip = '127.0.0.1' #localhost - endereço IP do meu próprio computador
port = 49152
addr = (ip,port)
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
socket_cliente.connect(addr)

auth = 0
porta = 1
credenciais = 0

print("bem-vindo a porta 1\n")

tipo = int(input("Digite 1 para entrar e 2 para cadastrar: "))
username = input("digite seu nome de usuário: ")

if tipo == 1:
    credenciais = int(input("Digite sua credencial: "))
    
send_message(socket_cliente)

socket_cliente.close()


