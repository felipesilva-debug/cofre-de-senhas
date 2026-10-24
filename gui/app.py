import customtkinter as ctk
from core import database
from gui.login import TelaLogin
from gui.vault import TelaCofre

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cofre de Senhas")
        self.geometry("850x550")
        self.minsize(750, 450)
        
        self.conn = database.conectar()
        database.inicializar_banco(self.conn)
        self.chave_acesso = None
        
        self.mostrar_tela_login()

    def mostrar_tela_login(self):
        self.chave_acesso = None
        self.limpar_tela()
        TelaLogin(self)

    def mostrar_tela_cofre(self, chave: bytes):
        self.chave_acesso = chave
        self.limpar_tela()
        TelaCofre(self)

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()