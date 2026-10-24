# 🔐 Cofre de Senhas (Local & Open Source)

Um gestor de senhas desktop multiplataforma (Windows, Linux e macOS), desenvolvido em Python. Todos os dados são criptografados e armazenados estritamente de forma local no teu computador, garantindo controlo total sobre a tua privacidade sem depender de servidores na nuvem.

---

## ✨ Funcionalidades

* **Senha Mestre Única:** Protege todas as tuas credenciais com uma única senha principal.
* **Criptografia Forte:** Dados sensíveis protegidos com criptografia simétrica **Fernet (AES-128)** e derivação de chave **PBKDF2-HMAC-SHA256** (480.000 iterações) com *Salt* aleatório.
* **Pesquisa em Tempo Real:** Barra de pesquisa integrada que filtra instantaneamente as tuas senhas por serviço ou utilizador enquanto digitas.
* **Gerador de Senhas Integrado:** Cria senhas aleatórias e seguras (letras maiúsculas, minúsculas, números e símbolos) com apenas um clique.
* **Gestão Completa (CRUD):** Adiciona novas contas, edita dados existentes, exclui credenciais antigas e revela/oculta as senhas diretamente no ecrã.
* **Cópia Rápida:** Copia as tuas senhas diretamente para a área de transferência sem precisares de as exibir.
* **Interface Moderna:** Visual limpo em modo escuro (*Dark Mode*) construído com `CustomTkinter`.

<img width="1051" height="707" alt="image" src="https://github.com/user-attachments/assets/1fab9a8a-9cf2-40fe-a202-a16e265f12b1" />
<img width="1047" height="705" alt="image" src="https://github.com/user-attachments/assets/1f408b11-1861-4bba-9114-53085f9aab1b" />



---

## 🛠️ Tecnologias Utilizadas

* **[Python 3.10+](https://www.python.org/)**: Linguagem base do projeto.
* **[Cryptography](https://cryptography.io/)**: Biblioteca padrão da indústria para derivação de chaves e criptografia de dados.
* **[CustomTkinter](https://customtkinter.tomschimansky.com/)**: Framework de interface gráfica moderna.
* **SQLite3**: Banco de dados relacional embutido para armazenamento local num único ficheiro (`cofre.db`).

---

## 📂 Estrutura do Projeto

```text
cofre_de_senhas/
├── .gitignore             # Ignora o banco de dados pessoal e caches no Git
├── requirements.txt       # Dependências externas do projeto
├── README.md              # Documentação do sistema
├── main.py                # Ponto de entrada da aplicação
│
├── core/                  # Backend (Segurança e Dados)
│   ├── __init__.py
│   ├── crypto.py          # Derivação de chave, criptografia e gerador de senhas
│   └── database.py        # Conexão e operações CRUD no SQLite
│
└── gui/                   # Frontend (Interface Gráfica)
    ├── __init__.py
    ├── app.py             # Gestor da janela principal e navegação
    ├── login.py           # Tela de criação de cofre e autenticação
    └── vault.py           # Painel principal de gestão de senhas
```

---

## 🚀 Como Instalar e Executar Localmente

### Pré-requisitos
Certifica-te de ter o **Python 3** instalado na tua máquina. Durante a instalação no Windows, marca a opção **"Add Python to PATH"**.

### Passo a Passo

1. **Clonar este repositório:**
   ```bash
   git clone https://github.com/SEU-USUARIO/cofre-de-senhas.git
   cd cofre-de-senhas
   ```

2. **Criar e ativar um ambiente virtual (Recomendado):**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar as dependências:**
   ```bash
   python -m pip install -r requirements.txt
   ```

4. **Executar a aplicação:**
   ```bash
   python main.py
   ```

---

## 🛡️ Arquitetura de Segurança

1. **Zero Conhecimento da Senha Mestre:** A tua Senha Mestre **nunca** é guardada no banco de dados. No primeiro acesso, o sistema gera um *Salt* criptográfico de 16 bytes e deriva uma chave na memória para criptografar um token de verificação.
2. **Validação de Acesso:** A cada login, a senha digitada passa pelo algoritmo `PBKDF2HMAC` junto ao *Salt* guardado. Se a chave resultante conseguir descriptografar o token de verificação, o acesso é libertado e a chave permanece apenas na memória RAM enquanto o cofre estiver aberto.
3. **Bloqueio Imediato:** Ao clicares em "Bloquear Cofre" ou ao fechares o programa, a chave criptográfica é eliminada da memória.

> ⚠️ **Aviso Importante:** Como não há armazenamento na nuvem nem opções de recuperação, **não te esqueças da tua Senha Mestre**. Caso seja perdida, será matematicamente impossível recuperar os dados guardados no ficheiro `cofre.db`.

---

## 🤝 Como Contribuir

Contribuições são muito bem-vindas! Se desejas melhorar a interface, adicionar novas funcionalidades (como exportação de backup ou categorias) ou corrigir bugs:

1. Faz um **Fork** do projeto.
2. Cria uma *Branch* para a tua modificação (`git checkout -b feature/nova-funcionalidade`).
3. Faz o *Commit* das tuas alterações (`git commit -m 'Adiciona nova funcionalidade'`).
4. Faz o *Push* para a tua *Branch* (`git push origin feature/nova-funcionalidade`).
5. Abre um **Pull Request**.

---

## 📄 Licença

Este projeto será distribuído sob a licença **MIT** (ou equivalente escolhida futuramente).
