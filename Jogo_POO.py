import tkinter as tk

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
            text="Protótipo inicial do jogo.",
            font=("Arial", 14)
        )
        self.lbl_texto.pack(pady=20)


jogo = GulaDeGnomo()
jogo.mainloop()
