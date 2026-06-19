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

    def comparar_receita(self, ingredientes_jogador):
        return ingredientes_jogador == self.receita

    def finalizar_pedido(self, ingredientes_jogador):
        self.tentativas += 1
        self.finalizado = True

        if self.comparar_receita(ingredientes_jogador):
            self.acertou = True
            self.mudar_status("Pedido correto")
            return True

        self.acertou = False
        self.mudar_status("Pedido errado")
        self.aumentar_erros(1)
        return False


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
        self.pedido_atual = None
        self.montagem_atual = []
        self.clientes = ["Centauro", "Dragão", "Goblin", "Ogro", "Mago", "Slime"]

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
        self.gerar_novo_pedido(self.rodada)

    def criar_interface(self):
        self.lbl_titulo = tk.Label(self, text="🏰🍄 Gula de Gnomo 🍄🏰", font=("Arial", 22, "bold"))
        self.lbl_titulo.pack(pady=10)

        self.lbl_pedido = tk.Label(self, text="", font=("Arial", 14), justify="left")
        self.lbl_pedido.pack(pady=10)

        self.lbl_montagem = tk.Label(self, text="Seu lanche: vazio", font=("Arial", 12))
        self.lbl_montagem.pack(pady=10)

        self.frame_ingredientes = tk.Frame(self)
        self.frame_ingredientes.pack(pady=10)

        self.criar_botoes_ingredientes()

        self.btn_finalizar = tk.Button(
            self,
            text="Entregar Pedido",
            font=("Arial", 12, "bold"),
            bg="#90EE90",
            command=lambda: self.entregar_pedido(True)
        )
        self.btn_finalizar.pack(pady=8)

        self.lbl_status = tk.Label(self, text="", font=("Arial", 12, "italic"))
        self.lbl_status.pack(pady=10)

        self.lbl_placar = tk.Label(self, text="", font=("Arial", 12, "bold"))
        self.lbl_placar.pack(pady=10)

    def criar_botoes_ingredientes(self):
        for botao in self.botoes_ingredientes:
            botao.destroy()

        self.botoes_ingredientes = []

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

    def gerar_novo_pedido(self, nivel):
        nome_pedido = random.choice(["X-Burger", "X-Salada", "Bacon Burger", "Duplo Monstro", "Veggie"])

        receitas = {
            "X-Burger": ["Pão", "Hambúrguer", "Queijo"],
            "X-Salada": ["Pão", "Hambúrguer", "Queijo", "Alface", "Tomate"],
            "Bacon Burger": ["Pão", "Hambúrguer", "Queijo", "Bacon"],
            "Duplo Monstro": ["Pão", "Hambúrguer", "Hambúrguer", "Queijo", "Bacon"],
            "Veggie": ["Pão", "Alface", "Tomate", "Queijo"]
        }

        self.pedido_atual = PedidoHamburguer(
            nome=nome_pedido,
            dificuldade=nivel,
            tempo_limite=25,
            pontos_base=10 + nivel,
            ativo=True,
            cliente=random.choice(self.clientes),
            receita=receitas[nome_pedido],
            ingredientes_disponiveis=self.ingredientes,
            cor_pedido="#FFD966",
            gorjeta=random.randint(3, 10)
        )

        self.montagem_atual = []
        self.criar_botoes_ingredientes()
        self.atualizar_tela_pedido("Novo pedido recebido!")

    def adicionar_ao_lanche(self, ingrediente):
        if not self.jogo_ativo:
            return

        self.montagem_atual.append(ingrediente)
        self.pedido_atual.adicionar_ingrediente(ingrediente)
        self.atualizar_montagem()

    def entregar_pedido(self, manual):
        if not self.jogo_ativo:
            return

        acertou = self.pedido_atual.finalizar_pedido(self.montagem_atual)

        if acertou:
            self.pontos += 10
            self.pedidos_entregues += 1
            self.rodada += 1
            self.lbl_status.config(text="✅ Pedido correto! +10 pontos.")
        else:
            self.erros += 1
            self.lbl_status.config(text=f"❌ Pedido errado! Receita correta: {self.pedido_atual.receita}")

        self.gerar_novo_pedido(self.rodada)
        self.atualizar_placar()

    def atualizar_tela_pedido(self, mensagem):
        receita_texto = " + ".join(self.pedido_atual.receita)

        self.lbl_pedido.config(
            text=f"{mensagem}\n"
                 f"Cliente: {self.pedido_atual.cliente}\n"
                 f"Pedido: {self.pedido_atual.nome}\n"
                 f"Ingredientes pedidos: {receita_texto}"
        )

        self.atualizar_montagem()
        self.atualizar_placar()

    def atualizar_montagem(self):
        texto = " + ".join(self.montagem_atual) if self.montagem_atual else "vazio"
        self.lbl_montagem.config(text=f"Seu lanche: {texto}")

    def atualizar_placar(self):
        self.lbl_placar.config(
            text=f"Pontos: {self.pontos} | Erros: {self.erros}/{self.max_erros} | "
                 f"Pedidos corretos: {self.pedidos_entregues} | Rodada: {self.rodada}"
        )


jogo = GulaDeGnomo()
jogo.mainloop()
