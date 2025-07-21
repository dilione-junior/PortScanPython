# PortScan Interativo em Python
import socket

# Criação do socket TCP/IPv4
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.settimeout(0.5)  # Tempo limite para resposta (em segundos)

# Entrada do usuário
ip = input("Digite o endereço que deseja escanear: ")
port = int(input("Digite a porta: "))

# Tentativa de conexão
scan = client.connect_ex((ip, port))

# Verificação do resultado
if scan == 0:
    print(str(port) + " -> Porta Aberta")
else:
    print(str(port) + " -> Porta Fechada")