import struct
import datetime
import threading

file_lock = threading.Lock()
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
    auth = auth & 0b11
    tipo = tipo & 0b11  
    creds = creds & 0xFFFF
    nome = nome.encode('utf-8')[:50]
    nome = nome.ljust(50, b'\x00')

    mensagem = bytearray(60)

    packed_header = (porta << 4) | (auth << 2) | tipo
    mensagem[0] = packed_header
    mensagem[1:3] = struct.pack('>H', creds)
    mensagem[3:10] = struct.pack('>Q', timestamp)[1:]
    mensagem[10:60] = nome[:50]

    return bytes(mensagem)

def unpack_message(mensagem):

    if len(mensagem) == 60:
        porta = (mensagem[0] >> 4) & 0xF
        auth = (mensagem[0] >> 2) & 0b11
        tipo = (mensagem[0]) & 0b11
        creds = struct.unpack('>H', mensagem[1:3])[0]
        timestamp = struct.unpack('>Q', b'\x00' + mensagem[3:10])[0]
        nome = mensagem[10:60].decode('utf-8', errors='ignore').rstrip('\x00')

        return porta, auth, tipo, creds, timestamp, nome
    else:
        print("Mensagem inválida")

def send_message(socket, porta, auth, tipo, credenciais, username):
    
    mensagem = pack_message(porta, auth, tipo, credenciais, username)

    socket.sendall(mensagem)

def receive_message(socket):
    try:
        mensagem = socket.recv(60)
        if not mensagem:
            raise ConnectionError('Conexão abortada')
        porta, auth, tipo, creds, timestamp, nome = unpack_message(mensagem)
        return porta, auth, tipo, creds, timestamp, nome
    except ConnectionError as e:
        print(f'Erro de conexão: {e}')
        return None
    except OSError as e:
        print(f"Erro de socket: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None
    
def loggar(datatempo,porta,credencial,status):
    with file_lock:
        try:
            with open('log.txt','a') as f:
                data = f'{datatempo}, p{porta}, {credencial}, {status}\n'
                f.write(data)

        except FileNotFoundError:
            print(f"Arquivo log.txt não encontrado.")
            return None       

def login(credencial, nome, timestamp, porta):
    datatempo = datetime.datetime.fromtimestamp(timestamp)

    try:
        data = read_file('users.txt')
        if data is None:
            status = 'negado'
            auth = False
            return auth
    except ValueError:
        status = 'negado'
        auth = False
    else:
        for i in range(len(data)):
            try:
                fcredencial, fnome, fporta = data[i].split(',')
            except ValueError as e:
                print(e)
                continue
            else:
                if nome == fnome and int(credencial) == int(fcredencial):
                    if int(fporta) >= porta:
                        print('logado corretamente')
                        status = 'autorizado'
                        auth = True
                    else:
                        print('nivel insuficiente')
                        status = 'negado'
                        auth = False
                    break

        if i == len(data):
            print('não registrado')
            status = 'negado'
            auth = False

    loggar(datatempo, porta, credencial, status)
    return auth

def register(nome):
    
    data = read_file('users.txt')

    if data is None:
        data = f'1000,{nome},1\n'
        write_file('users.txt',data)
        return 1, 1000
    
    for i in range(len(data)):
        fcredencial, fnome, fporta = data[i].split(',')

        if nome == fnome:
            porta = int(fporta) + 1
            credencial = fcredencial
            data[i] = f'{credencial},{fnome},{porta}\n'
            print('Register: escalamento')
            break
    
    if i == (len(data)-1):
        credencial = int(fcredencial) + 1
        porta = 1
        data.insert(i,f'{credencial},{nome},{porta}\n')
        print('Register: Novo registro')

    write_file('users.txt',data)
    return porta, credencial

def read_file(file):
    with file_lock:
        try:
            with open(file, 'r') as f:
                lines = f.readlines()

                if lines:
                    return lines
                else:
                    print("Registro vazio")
                    return None
                
        except FileNotFoundError:
            print(f"Arquivo {file} não existe.")
            return None

def write_file(file,data):
    with file_lock:
        try:
            with open(file, 'w') as f:
                f.writelines(data)
        except FileNotFoundError:
            print(f"Arquivo {file} não existe.")
            return None

def client_handling(socket_cliente,socket_servidor):

    while True:
        mensagem = receive_message(socket_cliente)

        if mensagem is None:
            print('cliente não respondeu')
            break

        porta, auth, tipo, creds, timestamp, nome = mensagem
        
        if tipo == 1:
            auth = login(creds, nome, timestamp, porta)
            send_message(socket_cliente, porta, auth, tipo, creds, nome)
        elif tipo == 2:
            porta, creds = register(nome)
            send_message(socket_cliente, porta, True, tipo, int(creds), nome)
        else:
            send_message(socket_cliente, porta, True, tipo, creds, nome)
            socket_cliente.close()
    socket_cliente.close()