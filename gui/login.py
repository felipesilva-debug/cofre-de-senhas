import customtkinter as ctk
from tkinter import messagebox
from core import database, crypto

class TelaLogin(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(pady=60, padx=80, fill="both", expand=True)
        self.master = master

        self.config = database.obter_configuracao(self.master.conn)
        primeiro_acesso = self.config is None

        titulo = "Criar Novo Cofre" if primeiro_acesso else "Desbloquear Cofre"
        ctk.CTkLabel(self, text=titulo, font=("Arial", 26, "bold")).pack(pady=(40, 20))

        self.entrada_senha = ctk.CTkEntry(
            self, placeholder_text="Digite sua Senha Mestre", show="*", width=320, height=40
        )
        self.entrada_senha.pack(pady=10)
        self.entrada_senha.bind("<Return>", lambda event: self.autenticar())

        self.entrada_confirmacao = None
        if primeiro_acesso:
            self.entrada_confirmacao = ctk.CTkEntry(
                self, placeholder_text="Confirme a Senha Mestre", show="*", width=320, height=40
            )
            self.entrada_confirmacao.pack(pady=10)
            self.entrada_confirmacao.bind("<Return>", lambda event: self.autenticar())

        texto_botao = "Criar Cofre" if primeiro_acesso else "Entrar"
        ctk.CTkButton(
            self, text=texto_botao, command=self.autenticar, width=320, height=40, font=("Arial", 14, "bold")
        ).pack(pady=20)

    def autenticar(self):
        senha = self.entrada_senha.get()
        if not senha:
            messagebox.showwarning("Aviso", "O campo de senha não pode ficar vazio.")
            return

        # Fluxo de Primeiro Acesso
        if not self.config:
            confirmacao = self.entrada_confirmacao.get()
            if senha != confirmacao:
                messagebox.showerror("Erro", "As senhas não coincidem!")
                return
            if len(senha) < 6:
                messagebox.showwarning("Senha Fraca", "Crie uma Senha Mestre com pelo menos 6 caracteres.")
                return

            salt = crypto.gerar_salt()
            chave = crypto.derivar_chave(senha, salt)
            verificador = crypto.criptografar_texto("COFRE_VALIDO", chave)
            database.configurar_senha_mestre(self.master.conn, verificador, salt)
            self.master.mostrar_tela_cofre(chave)

        # Fluxo de Login Normal
        else:
            hash_salvo, salt_salvo = self.config
            chave = crypto.derivar_chave(senha, salt_salvo)
            try:
                texto_teste = crypto.descriptografar_texto(hash_salvo, chave)
                if texto_teste == "COFRE_VALIDO":
                    self.master.mostrar_tela_cofre(chave)
            except Exception:
                messagebox.showerror("Acesso Negado", "Senha Mestre incorreta!")
                self.entrada_senha.delete(0, "end")