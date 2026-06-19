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
        self.jogo_ativo = True
        self.montagem_atual = []

        self.ingredientes = [
            "Pão",
            "Hambúrguer",
            "Queijo",
            "Alface",
            "Tomate",
            "Bacon"
        ]

        self.botoes_ingredientes = []

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

        self.lbl_montagem = tk.Label(
            self,
            text="Seu lanche: vazio",
            font=("Arial", 12)
        )
        self.lbl_montagem.pack(pady=10)

        self.frame_ingredientes = tk.Frame(self)
        self.frame_ingredientes.pack(pady=10)

        self.criar_botoes_ingredientes()

    def criar_botoes_ingredientes(self):
        ingredientes_embaralhados = self.ingredientes.copy()
        random.shuffle(ingredientes_embaralhados)

        for indice, ingrediente in enumerate(ingredientes_embaralhados):
            linha = indice // 3
            coluna = indice % 3

            btn = tk.Button(
                self.frame_ingredientes,
                text=ingrediente,
                width=18,
                height=2,
                font=("Arial", 10, "bold"),
                command=lambda i=ingrediente: self.adicionar_ao_lanche(i)
            )

            btn.grid(row=linha, column=coluna, padx=5, pady=5)
            self.botoes_ingredientes.append(btn)

    def adicionar_ao_lanche(self, ingrediente):
        if not self.jogo_ativo:
            return

        self.montagem_atual.append(ingrediente)
        self.atualizar_montagem()

    def atualizar_montagem(self):
        if self.montagem_atual:
            texto = " + ".join(self.montagem_atual)
        else:
            texto = "vazio"

        self.lbl_montagem.config(text=f"Seu lanche: {texto}")


jogo = GulaDeGnomo()
jogo.mainloop()
