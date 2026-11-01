# PortScan em Python: varre várias portas ao mesmo tempo, sem dependências externas
import argparse
import json
import socket
import sys
from concurrent.futures import ThreadPoolExecutor


def interpretar_portas(texto):
    """Converte '22,80,8000-8010' em uma lista ordenada de portas únicas."""
    portas = set()
    for trecho in texto.split(","):
        inicio, separador, fim = trecho.strip().partition("-")
        try:
            primeira = int(inicio)
            ultima = int(fim) if separador else primeira
        except ValueError:
            raise ValueError(f"porta inválida: '{trecho.strip()}'") from None
        if not 1 <= primeira <= ultima <= 65535:
            raise ValueError(f"intervalo inválido: '{trecho.strip()}' (use portas de 1 a 65535)")
        portas.update(range(primeira, ultima + 1))
    return sorted(portas)


def testar_porta(ip, porta, timeout):
    """Retorna True se a conexão TCP for aceita."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.settimeout(timeout)
        return cliente.connect_ex((ip, porta)) == 0


def nome_do_servico(porta):
    try:
        return socket.getservbyport(porta, "tcp")
    except OSError:
        return "desconhecido"


def escanear(ip, portas, timeout=0.5, threads=100):
    """Retorna as portas abertas, em ordem crescente."""
    with ThreadPoolExecutor(max_workers=threads) as executor:
        estados = executor.map(lambda porta: testar_porta(ip, porta, timeout), portas)
        return [porta for porta, aberta in zip(portas, estados) if aberta]


def criar_parser():
    parser = argparse.ArgumentParser(description="Verifica portas TCP abertas em um host autorizado.")
    parser.add_argument("alvo", nargs="?", help="domínio ou IP (sem argumentos, o modo é interativo)")
    parser.add_argument("-p", "--portas", default="21,22,25,53,80,110,143,443,445,3306,3389,8080",
                        help="ex.: 22,80,8000-8010 (padrão: portas comuns)")
    parser.add_argument("--timeout", type=float, default=0.5, help="segundos por porta (padrão: 0.5)")
    parser.add_argument("--threads", type=int, default=100, help="conexões simultâneas (padrão: 100)")
    parser.add_argument("--json", action="store_true", help="exibe o resultado em JSON")
    return parser


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    parser = criar_parser()
    args = parser.parse_args(argv)

    if args.alvo:
        alvo, texto_portas = args.alvo, args.portas
    else:
        alvo = input("Digite o endereço que deseja escanear: ").strip()
        texto_portas = input("Digite as portas (ex.: 22,80,8000-8010): ").strip()

    if args.threads < 1 or args.timeout <= 0:
        parser.error("--threads e --timeout precisam ser maiores que zero")

    try:
        portas = interpretar_portas(texto_portas)
        ip = socket.gethostbyname(alvo)
    except ValueError as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 2
    except OSError:
        print(f"Erro: não foi possível resolver o endereço '{alvo}'", file=sys.stderr)
        return 2

    abertas = escanear(ip, portas, args.timeout, args.threads)

    if args.json:
        print(json.dumps({
            "alvo": alvo,
            "ip": ip,
            "portas_testadas": len(portas),
            "abertas": [{"porta": p, "servico": nome_do_servico(p)} for p in abertas],
        }, ensure_ascii=False, indent=2))
    else:
        print(f"Alvo: {alvo} ({ip}) - {len(portas)} porta(s) testada(s)")
        for porta in abertas:
            print(f"{porta:>5}/tcp  aberta  {nome_do_servico(porta)}")
        if not abertas:
            print("Nenhuma porta aberta encontrada.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
