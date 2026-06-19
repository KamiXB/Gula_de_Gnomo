import tkinter as tk
from tkinter import messagebox
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
        self.receitas = {
            "X-Burger": ["Pão", "Hambúrguer", "Queijo"],
            "X-Salada": ["Pão", "Hambúrguer", "Queijo", "Alface", "Tomate"],
            "Bacon Burger": ["Pão", "Hambúrguer", "Queijo", "Bacon"],
            "Duplo Monstro": ["Pão", "Hambúrguer", "Hambúrguer", "Queijo", "Bacon"],
            "Veggie": ["Pão", "Alface", "Tomate", "Queijo"]
        }

    def adicionar_ingrediente(self, ingrediente):
        self.ingredientes_montados.append(ingrediente)
        self.adicionar_historico(f"Adicionou {ingrediente}")

    def remover_ultimo_ingrediente(self, quantidade):
        for i in range(quantidade):
            if self.ingredientes_montados:
                removido = self.ingredientes_montados.pop()
                self.adicionar_historico(f"Removeu {removido}")

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

    def calcular_recompensa_final(self, bonus_tempo):
        if self.acertou:
            return self.pontos_base + self.gorjeta + bonus_tempo
        return 0


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
        self.tempo_tick = 1000
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

        self.criar_interface(650)
        self.after(100, self.iniciar_jogo)

    def mostrar_tutorial(self):
        tutorial = """
    🍖 BEM-VINDO AO GULA DE GNOMO! 🍄

    OBJETIVO:
    Monte os hambúrgueres exatamente como o cliente pediu.

    COMO JOGAR:
    1. Leia o pedido mostrado na tela.
    2. Clique nos ingredientes na ordem correta.
    3. Use os botões para desfazer ou limpar o lanche.
    4. Clique em "Entregar Pedido" quando terminar.

    ✅ Pedido correto:
    - Ganha pontos
    - Recebe gorjeta
    - Recebe bônus pelo tempo restante

    ❌ Pedido errado:
    - Conta como erro

    ⏰ Se o tempo acabar:
    - O cliente vai embora
    - Conta como erro

    💀 O jogo termina após 5 erros.

    Boa sorte!
    """
        messagebox.showinfo("Tutorial", tutorial)

    def iniciar_jogo(self):
        self.mostrar_tutorial()
        self.gerar_novo_pedido(self.rodada)
        self.contar_tempo(1)
    

    def criar_interface(self, largura):
        self.lbl_titulo = tk.Label(
            self,
            text="🏰🍄 Gula de Gnomo 🍄🏰",
            font=("Arial", 22, "bold")
        )
        self.lbl_titulo.pack(pady=10)

        self.lbl_pedido = tk.Label(
            self,
            text="",
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
            font=("Arial", 12),
            wraplength=560,
            justify="center"
        )
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

        self.btn_desfazer = tk.Button(
            self,
            text="Remover último ingrediente",
            font=("Arial", 11),
            command=lambda: self.desfazer_ingrediente(1)
        )
        self.btn_desfazer.pack(pady=4)

        self.btn_limpar = tk.Button(
            self,
            text="Limpar lanche",
            font=("Arial", 11),
            command=lambda: self.limpar_lanche(True)
        )
        self.btn_limpar.pack(pady=4)

        self.lbl_status = tk.Label(
            self,
            text="",
            font=("Arial", 12, "italic")
        )
        self.lbl_status.pack(pady=10)

        self.lbl_placar = tk.Label(
            self,
            text="",
            font=("Arial", 12, "bold")
        )
        self.lbl_placar.pack(pady=10)

        self.btn_reiniciar = tk.Button(
            self,
            text="Reiniciar Jogo",
            font=("Arial", 11, "bold"),
            command=lambda: self.reiniciar_jogo(True)
        )
        self.btn_reiniciar.pack(pady=10)

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
        nome_pedido = random.choice([
            "X-Burger",
            "X-Salada",
            "Bacon Burger",
            "Duplo Monstro",
            "Veggie"
        ])

        receitas = {
            "X-Burger": ["Pão", "Hambúrguer", "Queijo"],
            "X-Salada": ["Pão", "Hambúrguer", "Queijo", "Alface", "Tomate"],
            "Bacon Burger": ["Pão", "Hambúrguer", "Queijo", "Bacon"],
            "Duplo Monstro": ["Pão", "Hambúrguer", "Hambúrguer", "Queijo", "Bacon"],
            "Veggie": ["Pão", "Alface", "Tomate", "Queijo"]
        }

        tempo = max(10, 25 - nivel)

        self.pedido_atual = PedidoHamburguer(
            nome=nome_pedido,
            dificuldade=nivel,
            tempo_limite=tempo,
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
        self.atualizar_montagem("Ingrediente adicionado")

    def desfazer_ingrediente(self, quantidade):
        if not self.jogo_ativo:
            return

        for i in range(quantidade):
            if self.montagem_atual:
                self.montagem_atual.pop()

        self.pedido_atual.remover_ultimo_ingrediente(quantidade)
        self.atualizar_montagem("Último ingrediente removido")

    def limpar_lanche(self, confirmar):
        if confirmar:
            self.montagem_atual = []
            self.atualizar_montagem("Lanche limpo")
            self.pontos -= 15

    def entregar_pedido(self, manual):
        if not self.jogo_ativo:
            return

        acertou = self.pedido_atual.finalizar_pedido(self.montagem_atual)

        if acertou:
            bonus_tempo = self.pedido_atual.tempo_restante
            pontos_ganhos = self.pedido_atual.calcular_recompensa_final(bonus_tempo)

            self.pontos += pontos_ganhos
            self.pedidos_entregues += 1
            self.rodada += 1

            self.lbl_status.config(
                text=f"✅ Pedido correto! +{pontos_ganhos} pontos."
            )
        else:
            self.erros += 1
            self.lbl_status.config(
                text=f"❌ Pedido errado! Receita correta: {self.pedido_atual.receita}"
            )

        if self.erros >= self.max_erros:
            self.finalizar_jogo("Muitos erros cometidos")
        else:
            self.gerar_novo_pedido(self.rodada)

        self.atualizar_placar("Atualizando placar")

    def contar_tempo(self, valor):
        if self.jogo_ativo and self.pedido_atual:
            self.pedido_atual.reduzir_tempo(valor)
            self.lbl_timer.config(text=f"{self.pedido_atual.tempo_restante}s")

            if self.pedido_atual.tempo_restante <= 0:
                self.erros += 1
                self.lbl_status.config(text="Tempo esgotado! Cliente foi embora.")

                if self.erros >= self.max_erros:
                    self.finalizar_jogo("Tempo esgotado muitas vezes")
                    return
                else:
                    self.gerar_novo_pedido(self.rodada)

            self.atualizar_placar("Tempo atualizado")
            self.after(self.tempo_tick, lambda: self.contar_tempo(1))

    def atualizar_tela_pedido(self, mensagem):
        receita_texto = " + ".join(self.pedido_atual.receita)

        self.lbl_pedido.config(
            text=f"{mensagem}\n"
                 f"Cliente: {self.pedido_atual.cliente}\n"
                 f"Pedido: {self.pedido_atual.nome}\n"
                 f"Ingredientes pedidos: {receita_texto}"
        )

        self.lbl_timer.config(text=f"Tempo: {self.pedido_atual.tempo_restante}s")
        self.atualizar_montagem("Pedido atualizado")
        self.atualizar_placar("Pedido atualizado")

    def atualizar_montagem(self, mensagem):
        if self.montagem_atual:
            texto = " + ".join(self.montagem_atual)
        else:
            texto = "vazio"

        self.lbl_montagem.config(text=f"Seu lanche: {texto}")

    def atualizar_placar(self, motivo):
        self.lbl_placar.config(
            text=f"Pontos: {self.pontos} | Erros: {self.erros}/{self.max_erros} | "
                 f"Pedidos corretos: {self.pedidos_entregues} | Rodada: {self.rodada}"
        )

    def finalizar_jogo(self, motivo):
        self.jogo_ativo = False
        self.lbl_pedido.config(
            text=f"💀 Fim de jogo!\nMotivo: {motivo}"
        )
        self.lbl_status.config(
            text=f"Pontuação final: {self.pontos}"
        )

    def reiniciar_jogo(self, confirmar):
        if confirmar:
            self.pontos = 0
            self.erros = 0
            self.pedidos_entregues = 0
            self.rodada = 1
            self.jogo_ativo = True
            self.lbl_status.config(text="")
            self.gerar_novo_pedido(self.rodada)


jogo = GulaDeGnomo()
jogo.mainloop()