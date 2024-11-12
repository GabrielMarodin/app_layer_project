import socket 
#ip = input('digite o ip de conexao: ') 
ip = '127.0.0.1' #localhost - endereço IP do meu próprio computador
porta = 7000 #porta aleatória
addr = ((ip,porta)) 
#criar o socket para o servidor passando a família do protocolo de transporte 
#socket.AF_INET define que é um protocolo para rede IP (AF_BLUETOOTH definiria comunicação bluetooth, por exemplo)
#socket.SOCK_STREAM para TCP
#socket.SOCK_DGRAM para UDP
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
#define endereço e porta do servidor ao qual o cliente irá se comunicar
socket_cliente.connect(addr) 
mensagem = input("digite uma mensagem para enviar ao servidor: ") 
socket_cliente.send(mensagem.encode()) #envia mensagem (codificada em bytes)
print ("mensagem enviada")
socket_cliente.close()