import tkinter as tk

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


class GulaDeGnomo(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gula de Gnomo")
        self.geometry("800x700")
        self.resizable(False, False)

        self.lbl_titulo = tk.Label(
            self,
            text="🏰🍄 Gula de Gnomo 🍄🏰",
            font=("Arial", 22, "bold")
        )
        self.lbl_titulo.pack(pady=20)

        self.lbl_texto = tk.Label(
            self,
            text="PedidoHamburguer e receitas adicionados.",
            font=("Arial", 14)
        )
        self.lbl_texto.pack(pady=20)


jogo = GulaDeGnomo()
jogo.mainloop()
