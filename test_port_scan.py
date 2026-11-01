import socket
import unittest

from port_scan import escanear, interpretar_portas, main


class TestPortas(unittest.TestCase):
    def test_lista_e_intervalo_sem_repeticao(self):
        self.assertEqual(interpretar_portas("80, 22,20-22"), [20, 21, 22, 80])

    def test_valores_invalidos(self):
        for texto in ("abc", "0", "70000", "90-80", ""):
            with self.subTest(texto=texto), self.assertRaises(ValueError):
                interpretar_portas(texto)


class TestVarredura(unittest.TestCase):
    def setUp(self):
        self.servidor = socket.socket()
        self.addCleanup(self.servidor.close)
        self.servidor.bind(("127.0.0.1", 0))
        self.servidor.listen()
        self.aberta = self.servidor.getsockname()[1]
        # Reserva uma porta e a libera para garantir que nada está escutando nela
        livre = socket.socket()
        livre.bind(("127.0.0.1", 0))
        self.fechada = livre.getsockname()[1]
        livre.close()

    def test_diferencia_porta_aberta_de_fechada(self):
        self.assertEqual(escanear("127.0.0.1", [self.aberta, self.fechada]), [self.aberta])

    def test_cli_sucesso_e_erros_de_entrada(self):
        self.assertEqual(main(["127.0.0.1", "-p", str(self.aberta)]), 0)
        self.assertEqual(main(["127.0.0.1", "-p", "abc"]), 2)
        self.assertEqual(main(["host.invalid", "-p", "80"]), 2)


if __name__ == "__main__":
    unittest.main()
