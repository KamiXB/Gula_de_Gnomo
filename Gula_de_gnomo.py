import tkinter as tk
import random

class EntidadePedido:
    def __init__(self, nome, dificuldade, tempo_limite, pontos_base, ativo):
        self.nome = nome
        self.dificuldade = dificuldade
        self.tempo_limite = tempo_limite
        self.pontos_base = pontos_base
        self.ativo = ativo

        self.status = "Aguardando"
        self.tempo_restante = tempo_limite
        self.historico = []
        self.tentativas = 0
        self.erros = 0

    def mudar_status(self, novo_status):
        self.status = novo_status

    def reduzir_tempo(self, valor):
        self.tempo_restante -= valor
        if self.tempo_restante < 0:
            self.tempo_restante = 0

    def adicionar_historico(self, acao):
        self.historico.append(acao)

    def aumentar_erros(self, quantidade):
        self.erros += quantidade

    def calcular_pontos(self, multiplicador):
        return self.pontos_base * multiplicador


class PedidoHamburguer(EntidadePedido):
    def __init__(self, nome, dificuldade, tempo_limite, pontos_base, ativo,
                 cliente, receita, ingredientes_disponiveis, cor_pedido, gorjeta):
        super().__init__(nome, dificuldade, tempo_limite, pontos_base, ativo)

        self.cliente = cliente
        self.receita = receita
        self.ingredientes_disponiveis = ingredientes_disponiveis
        self.cor_pedido = cor_pedido
        self.gorjeta = gorjeta

        self.ingredientes_montados = []
        self.finalizado = False
        self.acertou = False
        self.combo = 0

    def adicionar_ingrediente(self, ingrediente):
        self.ingredientes_montados.append(ingrediente)
        self.adicionar_historico(f"Adicionou {ingrediente}")


class GulaDeGnomo(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gula de Gnomo")
        self.geometry("800x700")
        self.resizable(False, False)

        self.pontos = 0
        self.erros = 0
        self.max_erros = 5
        self.pedidos_entregues = 0
        self.rodada = 1

        self.criar_interface()

    def criar_interface(self):
        self.lbl_titulo = tk.Label(
            self,
            text="🏰🍄 Gula de Gnomo 🍄🏰",
            font=("Arial", 22, "bold")
        )
        self.lbl_titulo.pack(pady=10)

        self.lbl_pedido = tk.Label(
            self,
            text="Pedido aparecerá aqui.",
            font=("Arial", 14),
            justify="left"
        )
        self.lbl_pedido.pack(pady=10)

        self.lbl_timer = tk.Label(
            self,
            text="Tempo: 0",
            font=("Arial", 18, "bold"),
            fg="red"
        )
        self.lbl_timer.pack(pady=5)

        self.lbl_montagem = tk.Label(
            self,
            text="Seu lanche: vazio",
            font=("Arial", 12)
        )
        self.lbl_montagem.pack(pady=10)

        self.lbl_placar = tk.Label(
            self,
            text=f"Pontos: {self.pontos} | Erros: {self.erros}/{self.max_erros}",
            font=("Arial", 12, "bold")
        )
        self.lbl_placar.pack(pady=10)


jogo = GulaDeGnomo()
jogo.mainloop()
