**Projeto: Port Scanner com Python**

Desenvolvi um scanner de portas em Python utilizando a biblioteca socket. Este script é um port scanner simples e interativo, criado com Python. Ele tem como objetivo verificar se uma porta específica está aberta por meio de um domínio e número de porta informados pelo usuário.
O funcionamento é bem simples:

1.	Primeiro, o código importa a biblioteca socket, que permite a comunicação entre o seu computador e outros dispositivos na rede.
2.	Em seguida, ele cria um socket TCP (ou seja, uma conexão confiável) e define um tempo limite para evitar que o programa fique travado esperando por resposta.
3.	O usuário informa dois dados:
 ##O domínio ou endereço IP do alvo (por exemplo, dominiodeexemplo.com ou IP xxx.xxx.x.x);
 ##Após o número da porta que deseja testar (exemplo porta 22).
4.	O programa tenta se conectar à porta informada no destino.
5.	Se a conexão for bem-sucedida, isso significa que a porta está aberta. Se não for possível se conectar, é sinal de que a porta está fechada ou inacessível.
Esse tipo de verificação é muito útil em testes de segurança e diagnósticos de rede, ajudando a identificar serviços que estão disponíveis em um servidor.
