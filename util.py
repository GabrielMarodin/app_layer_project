import struct
import datetime
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

def send_message(socket, porta, auth, tipo, credenciais, username):
    
    mensagem = pack_message(porta, auth, tipo, credenciais, username)

    socket.sendall(mensagem)

def loggar(datatempo,porta,credencial,status):
    try:
        with open('log.txt','a') as f:
            data = f'{datatempo}, p{porta}, {credencial}, {status}\n'
            f.write(data)

    except FileNotFoundError:
        print(f"Arquivo log.txt não encontrado.")
        return None       

def login(credencial, nome, timestamp, porta):
    read = read_file('users.txt')
    datatempo = datetime.datetime.fromtimestamp(timestamp)

    try:
        data, length = read

    except TypeError:
        print('registro vazio')
        status = 'negado'
        auth = False
    
    else:
       
        i = 0

        while i < length:
            fcredencial, fnome, fporta = data[i].split(',')

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
            i = i + 1

        if i == length:
            print('não registrado')
            status = 'negado'
            auth = False

    loggar(datatempo, porta, credencial, status)
    return status, auth

def register(nome):
    read = read_file('users.txt')

    try:
        data, length = read
        
    except TypeError:
        data = f'1000,{nome},1\n'
        write_file('users.txt',data)
        return 'registrado', 1, 1000
    
    else:
        i = 0

        while i < length:
            fcredencial, fnome, fporta = data[i].split(',')

            if nome == fnome:
                porta = int(fporta) + 1
                data[i] = f'{fcredencial},{fnome},{porta}\n'
                estado = 'escalado'
                credencial = fcredencial

            i = i + 1
        
        if i == length:
            fcredencial, fnome, fporta = data[(i-1)].split(',')
            credencial = int(fcredencial) + 1
            data.insert(i,f'{credencial},{nome},1\n')
            estado = 'registrado'
            porta = 1

        write_file('users.txt',data)
        return estado, porta, credencial

def read_file(file):

    try:
        with open(file, 'r') as f:
            lines = f.readlines()

            if lines:
                length = len(lines)
                return lines, length
            else:
                print("Registro vazio")
                return None
            
    except FileNotFoundError:
        print(f"Arquivo {file} não existe.")
        return None

def write_file(file,data):
    try:
        with open(file, 'w') as f:
            f.writelines(data)
    except FileNotFoundError:
        print(f"Arquivo {file} não existe.")
        return None
