import customtkinter as ctk
from tkinter import messagebox
from core import database, crypto

class TelaCofre(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(pady=15, padx=15, fill="both", expand=True)
        self.master = master

        # Cabeçalho
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(5, 10))
        ctk.CTkLabel(header, text="Minhas Credenciais", font=("Arial", 22, "bold")).pack(side="left")
        ctk.CTkButton(
            header, text="Bloquear Cofre", width=120, fg_color="#555555", command=self.master.mostrar_tela_login
        ).pack(side="right")

        # Formulário de Adição
        form = ctk.CTkFrame(self)
        form.pack(fill="x", padx=10, pady=5)

        self.entry_servico = ctk.CTkEntry(form, placeholder_text="Serviço (Ex: GitHub, Gmail)")
        self.entry_servico.pack(side="left", padx=5, pady=10, expand=True, fill="x")

        self.entry_usuario = ctk.CTkEntry(form, placeholder_text="Usuário ou E-mail")
        self.entry_usuario.pack(side="left", padx=5, pady=10, expand=True, fill="x")

        self.entry_senha = ctk.CTkEntry(form, placeholder_text="Senha")
        self.entry_senha.pack(side="left", padx=5, pady=10, expand=True, fill="x")

        ctk.CTkButton(
            form, text="Gerar Senha", width=100, fg_color="#2b7a78", command=self.preencher_senha_gerada
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            form, text="Salvar", width=90, command=self.adicionar_senha
        ).pack(side="left", padx=(5, 10))

        # Barra de Pesquisa
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=10, pady=(10, 0))

        self.entry_pesquisa = ctk.CTkEntry(
            search_frame, placeholder_text="🔍 Pesquisar por serviço ou usuário..."
        )
        self.entry_pesquisa.pack(side="left", expand=True, fill="x", padx=(0, 5))
        # Atualiza a lista automaticamente a cada tecla digitada
        self.entry_pesquisa.bind("<KeyRelease>", lambda event: self.carregar_senhas())

        ctk.CTkButton(
            search_frame, text="Limpar", width=80, fg_color="#444444", command=self.limpar_pesquisa
        ).pack(side="left")

        # Lista Rolável de Senhas
        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.pack(fill="both", expand=True, padx=10, pady=10)

        self.carregar_senhas()

    def limpar_pesquisa(self):
        self.entry_pesquisa.delete(0, "end")
        self.carregar_senhas()

    def preencher_senha_gerada(self):
        nova_senha = crypto.gerar_senha_forte(16)
        self.entry_senha.delete(0, "end")
        self.entry_senha.insert(0, nova_senha)

    def adicionar_senha(self):
        servico = self.entry_servico.get().strip()
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get()

        if not servico or not senha:
            messagebox.showwarning("Campos Obrigatórios", "Preencha pelo menos o Serviço e a Senha.")
            return

        senha_cripto = crypto.criptografar_texto(senha, self.master.chave_acesso)
        database.adicionar_credencial(self.master.conn, servico, usuario, senha_cripto)

        self.entry_servico.delete(0, "end")
        self.entry_usuario.delete(0, "end")
        self.entry_senha.delete(0, "end")
        self.carregar_senhas()

    def copiar_para_clipboard(self, senha: str):
        self.master.clipboard_clear()
        self.master.clipboard_append(senha)
        self.master.update()
        messagebox.showinfo("Copiado", "A senha foi copiada para a sua área de transferência!")

    def excluir_item(self, id_cred: int, titulo: str):
        confirmar = messagebox.askyesno("Confirmar Exclusão", f"Deseja realmente apagar a senha de '{titulo}'?")
        if confirmar:
            database.remover_credencial(self.master.conn, id_cred)
            self.carregar_senhas()

    def abrir_janela_edicao(self, id_cred: int, titulo_atual: str, usuario_atual: str, senha_atual: str):
        """Abre uma janela modal para editar os dados da credencial selecionada."""
        janela = ctk.CTkToplevel(self)
        janela.title(f"Editar - {titulo_atual}")
        janela.geometry("400x330")
        janela.resizable(False, False)
        janela.transient(self.master)
        janela.grab_set()

        ctk.CTkLabel(janela, text="Editar Credencial", font=("Arial", 18, "bold")).pack(pady=(20, 15))

        entry_servico = ctk.CTkEntry(janela, placeholder_text="Serviço", width=320)
        entry_servico.pack(pady=8)
        entry_servico.insert(0, titulo_atual)

        entry_usuario = ctk.CTkEntry(janela, placeholder_text="Usuário ou E-mail", width=320)
        entry_usuario.pack(pady=8)
        if usuario_atual:
            entry_usuario.insert(0, usuario_atual)

        frame_senha = ctk.CTkFrame(janela, fg_color="transparent")
        frame_senha.pack(pady=8)

        entry_senha = ctk.CTkEntry(frame_senha, placeholder_text="Senha", width=210)
        entry_senha.pack(side="left", padx=(0, 10))
        entry_senha.insert(0, senha_atual)

        def gerar_nova():
            nova = crypto.gerar_senha_forte(16)
            entry_senha.delete(0, "end")
            entry_senha.insert(0, nova)

        ctk.CTkButton(
            frame_senha, text="Gerar Nova", width=100, fg_color="#2b7a78", command=gerar_nova
        ).pack(side="left")

        def salvar_edicao():
            novo_servico = entry_servico.get().strip()
            novo_usuario = entry_usuario.get().strip()
            nova_senha = entry_senha.get()

            if not novo_servico or not nova_senha:
                messagebox.showwarning("Aviso", "Serviço e Senha são obrigatórios!", parent=janela)
                return

            nova_senha_cripto = crypto.criptografar_texto(nova_senha, self.master.chave_acesso)
            database.atualizar_credencial(
                self.master.conn, id_cred, novo_servico, novo_usuario, nova_senha_cripto
            )
            janela.destroy()
            self.carregar_senhas()

        ctk.CTkButton(
            janela, text="Salvar Alterações", width=320, height=38,
            font=("Arial", 14, "bold"), command=salvar_edicao
        ).pack(pady=20)

    def criar_item_lista(self, id_cred: int, titulo: str, usuario: str, senha_aberta: str):
        """Cria a linha visual de cada credencial com seus respectivos botões."""
        item_frame = ctk.CTkFrame(self.scroll, fg_color="gray20", corner_radius=6)
        item_frame.pack(fill="x", pady=4, padx=5)

        usuario_exibicao = usuario if usuario else "Não informado"
        texto_oculto = f"{titulo}   |   Usuário: {usuario_exibicao}   |   Senha: ••••••••"
        texto_visivel = f"{titulo}   |   Usuário: {usuario_exibicao}   |   Senha: {senha_aberta}"

        lbl_info = ctk.CTkLabel(
            item_frame, text=texto_oculto, font=("Arial", 13, "bold"), anchor="w"
        )
        lbl_info.pack(side="left", padx=15, pady=10, expand=True, fill="x")

        visivel = False

        def alternar_visualizacao():
            nonlocal visivel
            visivel = not visivel
            if visivel:
                lbl_info.configure(text=texto_visivel, text_color="#4ea8de")
                btn_ver.configure(text="Ocultar", fg_color="#555555")
            else:
                lbl_info.configure(text=texto_oculto, text_color=("gray10", "gray90"))
                btn_ver.configure(text="Ver", fg_color="#3b8ed0")

        btn_ver = ctk.CTkButton(
            item_frame, text="Ver", width=70, command=alternar_visualizacao
        )
        btn_ver.pack(side="left", padx=3, pady=8)

        ctk.CTkButton(
            item_frame, text="Copiar", width=70,
            command=lambda: self.copiar_para_clipboard(senha_aberta)
        ).pack(side="left", padx=3, pady=8)

        ctk.CTkButton(
            item_frame, text="Editar", width=70, fg_color="#d97706", hover_color="#b45309",
            command=lambda: self.abrir_janela_edicao(id_cred, titulo, usuario, senha_aberta)
        ).pack(side="left", padx=3, pady=8)

        ctk.CTkButton(
            item_frame, text="Excluir", width=70, fg_color="#a83232", hover_color="#7a2020",
            command=lambda: self.excluir_item(id_cred, titulo)
        ).pack(side="left", padx=(3, 10), pady=8)

    def carregar_senhas(self):
        for widget in self.scroll.winfo_children():
            widget.destroy()

        termo_busca = self.entry_pesquisa.get().strip().lower()
        credenciais = database.listar_credenciais(self.master.conn)

        # Filtra pelo serviço ou usuário caso exista algo digitado na busca
        if termo_busca:
            credenciais = [
                c for c in credenciais
                if termo_busca in c[1].lower() or (c[2] and termo_busca in c[2].lower())
            ]

        if not credenciais:
            msg = "Nenhum resultado encontrado para a pesquisa." if termo_busca else "Nenhuma senha cadastrada ainda."
            ctk.CTkLabel(self.scroll, text=msg, text_color="gray").pack(pady=30)
            return

        for cred in credenciais:
            id_cred, titulo, usuario, senha_cripto = cred
            try:
                senha_aberta = crypto.descriptografar_texto(senha_cripto, self.master.chave_acesso)
                self.criar_item_lista(id_cred, titulo, usuario, senha_aberta)
            except Exception:
                continue