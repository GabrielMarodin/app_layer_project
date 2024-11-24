Programa cliente-servidor para controle de acesso.

- Protocolo de transporte TCP. Garantia de envio e recebimento dos pacotes completos em ordem e controle de conexão.
- Servidor utiliza muiltithreading para gerenciar múltiplos sockets. Nunca fecha está sempre ouvindo.
- Cliente depois de aberto não fecha até o programa deixar de executar.

Funcionamento:

1- Servidor é aberto executando Servidor.py;
2- Servidor aguarda conexão;
3- Cliente é aberto executando Cliente.py [porta] (se nemhum argumento for passado utiliza a porta 1);
4- Cliente estabelece conexão;
5- Servidor entra no loop de handling do cliente onde aguarda uma mensagem;
6- Usuário interage com o terminal;
7- Cliente empacota mensagem;
8- Cliente envia mensagem;
10- Cliente espera resposta;
11- Servidor recebe mensagem;
12- Servidor desempacota mensagem;
13- Servidor executa a rotina referente ao tipo de mensagem;
14- Servidor enpacota mensage;
15- Servidor envia mensagem;
16- Servidor volta a esperar recebimento de mensagem;
17- Cliente recebe mensagem e desempacota ela;
18- Cliente mostra resposta correspondente ao usuário;
19- Cliente volta ao começo do loop em (6)

Estrutura da mensagem:

tamanho: 60 bytes
       primeiro_byte { 
         porta: 4 bits,
         autorização: 2 bits,
         tipo: 2 bits,
       }
       credenciais: 2 bytes
       datatempo: 7 bytes
       nome: 50 bytes

Rotinas do servidor:

Login:
Ler as credenciais do arquivo de texto, se elas forem iguais as recebidas setar autorização como True e escrever no arquivo de log como autorizado, 
se não, setar autorização como False e escrever no arquivo de log como negado.

Cadastro:
Ler o arquivo de usuários, se o usuário exisitir modificar sua permissão para a porta de onde a mensagem veio e autorizar, 
se já tiver a permissão não fazer nada e negar, se o usuário não existir escrever nova linha com o nome e uma credencial única e autorizar.
