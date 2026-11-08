# 🔐 Cofre de Senhas (Local & Open Source)

Um gestor de senhas desktop multiplataforma, desenvolvido em Python. Todos os dados são criptografados e armazenados estritamente de forma local no seu computador, garantindo controle total sobre a sua privacidade sem depender de servidores na nuvem.

---

## ✨ Funcionalidades

* **Senha Mestre Única:** Protege todas as suas credenciais com uma única senha principal.
* **Criptografia Forte:** Dados sensíveis protegidos com criptografia simétrica **Fernet (AES-128)** e derivação de chave **PBKDF2-HMAC-SHA256** (480.000 iterações) com *Salt* aleatório.
* **Pesquisa em Tempo Real:** Barra de pesquisa integrada que filtra instantaneamente as suas senhas por serviço ou usuário enquanto digita.
* **Gerador de Senhas Integrado:** Cria senhas aleatórias e seguras (letras maiúsculas, minúsculas, números e símbolos) com apenas um clique.
* **Gestão Completa (CRUD):** Adiciona novas contas, edita dados existentes, exclui credenciais antigas e revela/oculta as senhas diretamente na tela.
* **Cópia Rápida:** Copia as suas senhas diretamente para a área de transferência sem precisar exibi-las.
* **Interface Moderna:** Visual limpo em modo escuro (*Dark Mode*) construído com `CustomTkinter`.

---

## 🛠️ Tecnologias Utilizadas

* **[Python 3.10+](https://www.python.org/)**: Linguagem base do projeto.
* **[Cryptography](https://cryptography.io/)**: Biblioteca padrão da indústria para derivação de chaves e criptografia de dados.
* **[CustomTkinter](https://customtkinter.tomschimansky.com/)**: Framework de interface gráfica moderna.
* **SQLite3**: Banco de dados relacional embutido para armazenamento local em um único arquivo (`cofre.db`).
* **PyInstaller**: Utilizado para empacotar o projeto em um executável autônomo `.exe`.

---

## 📂 Estrutura do Projeto

```text
cofre_de_senhas/
├── .gitignore             # Ignora o banco de dados pessoal e caches no Git
├── requirements.txt       # Dependências externas do projeto
├── README.md              # Documentação do sistema
├── main.py                # Ponto de entrada da aplicação
├── main.spec              # (Gerado) Arquivo de configuração do PyInstaller
│
├── build/                 # (Gerado) Pasta de arquivos temporários da compilação do .exe
├── dist/                  # (Gerado) Contém o arquivo final main.exe pronto para uso
│
├── core/                  # Backend (Segurança e Dados)
│   ├── __init__.py
│   ├── crypto.py          # Derivação de chave, criptografia e gerador de senhas
│   └── database.py        # Conexão e operações CRUD no SQLite
│
└── gui/                   # Frontend (Interface Gráfica)
    ├── __init__.py
    ├── app.py             # Gerenciador da janela principal e navegação
    ├── login.py           # Tela de criação de cofre e autenticação
    └── vault.py           # Painel principal de gestão de senhas
```

---

## 🚀 Como Instalar e Executar

Existem duas formas de usar o Cofre de Senhas: baixando o executável pronto (recomendado para uso diário) ou executando a partir do código-fonte (para desenvolvedores).

### Opção 1: Arquivo Executável (.exe)
Não é necessário instalar o Python. Esta é a forma mais rápida de começar a usar.

1. Vá até a pasta `dist/` do projeto (ou baixe o `.exe` na aba **Releases** deste repositório).
2. Mova o arquivo executável (`main.exe`) para uma pasta segura no seu computador.
3. Dê um duplo clique para abrir. O banco de dados criptografado (`cofre.db`) será criado automaticamente na mesma pasta em que o executável estiver localizado.

### Opção 2: Código-Fonte (Desenvolvedores)
Requer o **Python 3** instalado na sua máquina.

1. **Clone este repositório:**
   ```bash
   git clone https://github.com/SEU-USUARIO/cofre-de-senhas.git
   cd cofre-de-senhas
   ```

2. **Crie um ambiente virtual e instale as dependências:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Execute a aplicação:**
   ```bash
   python main.py
   ```

### ⚙️ Como compilar o seu próprio executável
Se você fizer modificações no código e quiser gerar um novo `.exe` sem a tela preta de terminal ao fundo, utilize os comandos abaixo no seu ambiente virtual:
```bash
pip install pyinstaller
python -m PyInstaller --onefile --windowed main.py
```
O novo arquivo executável será gerado dentro da pasta `dist/`.

---

## 🛡️ Arquitetura de Segurança

1. **Zero Conhecimento da Senha Mestre:** A sua Senha Mestre **nunca** é salva no banco de dados. No primeiro acesso, o sistema gera um *Salt* criptográfico de 16 bytes e deriva uma chave na memória para criptografar um token de verificação.
2. **Validação de Acesso:** A cada login, a senha digitada passa pelo algoritmo `PBKDF2HMAC` junto ao *Salt* salvo. Se a chave resultante conseguir descriptografar o token de verificação, o acesso é liberado e a chave permanece apenas na memória RAM enquanto o cofre estiver aberto.
3. **Bloqueio Imediato:** Ao clicar em "Bloquear Cofre" ou fechar o programa, a chave criptográfica é apagada da memória.

> ⚠️ **Aviso Importante:** Como não há armazenamento na nuvem nem opções de recuperação de senha por e-mail, **não esqueça a sua Senha Mestre**. Caso ela seja perdida, será matematicamente impossível recuperar os dados guardados no arquivo `cofre.db`.

---

## 🤝 Como Contribuir

Contribuições são bem-vindas! Se deseja melhorar a interface, adicionar novas funcionalidades ou corrigir bugs:

1. Faça um **Fork** do projeto.
2. Crie uma *Branch* para a sua modificação (`git checkout -b feature/nova-funcionalidade`).
3. Faça o *Commit* das suas alterações (`git commit -m 'Adiciona nova funcionalidade'`).
4. Faça o *Push* para a sua *Branch* (`git push origin feature/nova-funcionalidade`).
5. Abra um **Pull Request**.

---

## 📄 Licença

Este projeto é distribuído sob a licença **MIT**.
