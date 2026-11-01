# PortScanPython

Scanner de portas TCP em Python que testa várias portas ao mesmo tempo, usando somente a biblioteca padrão. Serve para diagnóstico de rede e para conferir quais serviços um host seu está expondo.

> **Uso autorizado:** faça varreduras apenas em hosts seus ou com permissão. Mesmo sem causar danos, uma varredura sem autorização pode violar regras de provedores e leis locais.

## Como funciona

1. Transforma a entrada (`22,80,8000-8010`) em uma lista de portas.
2. Resolve o domínio para um endereço IPv4.
3. Tenta abrir uma conexão TCP em cada porta, usando várias threads.
4. Se a conexão for aceita, a porta está aberta. O nome do serviço vem da tabela padrão do sistema e indica apenas o uso **comum** daquela porta.

## Passo a passo

### 1. Baixar

Testado com Python 3.13; não há bibliotecas para instalar.

```bash
git clone https://github.com/dilione-junior/PortScanPython.git
cd PortScanPython
```

### 2. Criar um alvo de teste

Para testar sem depender de outro host, abra um servidor local em um terminal e deixe-o aberto:

```bash
python -m http.server 8000 --bind 127.0.0.1
```

### 3. Executar a varredura

Em outro terminal:

```bash
python port_scan.py 127.0.0.1 -p 8000,8001
```

```text
Alvo: 127.0.0.1 (127.0.0.1) - 2 porta(s) testada(s)
 8000/tcp  aberta  desconhecido
```

### 4. Outros exemplos

```bash
# Portas mais comuns (padrão)
python port_scan.py 127.0.0.1

# Intervalo de portas com tempo limite maior, útil em redes lentas
python port_scan.py 127.0.0.1 -p 1-1024 --timeout 1

# Resultado em JSON
python port_scan.py 127.0.0.1 -p 8000 --json

# Modo interativo: o programa pergunta o alvo e as portas
python port_scan.py
```

## Opções

| Opção | Descrição | Padrão |
|---|---|---|
| `-p`, `--portas` | Portas e intervalos, como `22,80,8000-8010` | Portas comuns |
| `--timeout` | Segundos de espera por porta | 0.5 |
| `--threads` | Conexões simultâneas | 100 |
| `--json` | Exibe o resultado em JSON | Desativado |

## Limitações

- Testa apenas TCP sobre IPv4; não cobre UDP nem IPv6.
- Uma porta não listada pode estar fechada ou bloqueada por firewall: o programa não diferencia os dois casos.
- O serviço exibido não é confirmado por análise da resposta, então um programa pode estar usando uma porta diferente da habitual.
- Para varreduras completas, prefira o [Nmap](https://nmap.org/). Este projeto tem finalidade didática.

## Testes

```bash
python -m unittest -v
```
