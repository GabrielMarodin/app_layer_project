import socket 
host = '' 
porta = 7000 
addr = (host, porta) 
#criar o socket para o servidor passando a família do protocolo de transporte 
#socket.AF_INET define que é um protocolo para rede IP (AF_BLUETOOTH definiria comunicação bluetooth, por exemplo)
#socket.SOCK_STREAM para TCP
#socket.SOCK_DGRAM para UDP
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#reserva o socket para a nossa aplicação
socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
#define quais IP's e em qual porta o server vai aguardar conexão
socket_servidor.bind(addr) 
#define que servidor aguarda conexões e quantas conexão serão recebidas. Não é necessário caso UDP
socket_servidor.listen(10) 
print ('aguardando conexao')
con, cliente = socket_servidor.accept() #espera por conexão
print ('conectado') 
print ("aguardando mensagem") 
recebe = con.recv(1024) #recebe mensagem (em bytes, com tamanho max definido pelo parâmetro)
print ("mensagem recebida: ")  
print(recebe.decode()) 
socket_servidor.close()