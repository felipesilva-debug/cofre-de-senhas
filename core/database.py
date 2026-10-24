import sqlite3

def conectar(caminho_db: str = "cofre.db"):
    """Conecta ao arquivo local do banco de dados SQLite."""
    return sqlite3.connect(caminho_db)

def inicializar_banco(conn):
    """Cria as tabelas de configuração e credenciais caso não existam."""
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS config (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            master_hash BLOB NOT NULL,
            salt BLOB NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS credenciais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            usuario TEXT,
            senha_criptografada BLOB NOT NULL
        )
    """)
    conn.commit()

def configurar_senha_mestre(conn, master_hash: bytes, salt: bytes):
    """Registra o verificador da senha mestre e o salt no primeiro acesso."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO config (id, master_hash, salt)
        VALUES (1, ?, ?)
    """, (master_hash, salt))
    conn.commit()

def obter_configuracao(conn):
    """Busca o verificador e o salt salvos."""
    cursor = conn.cursor()
    cursor.execute("SELECT master_hash, salt FROM config WHERE id = 1")
    return cursor.fetchone()

def adicionar_credencial(conn, titulo: str, usuario: str, senha_criptografada: bytes):
    """Insere um novo registro de senha no banco."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO credenciais (titulo, usuario, senha_criptografada)
        VALUES (?, ?, ?)
    """, (titulo, usuario, senha_criptografada))
    conn.commit()

def listar_credenciais(conn):
    """Retorna todas as credenciais salvas."""
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo, usuario, senha_criptografada FROM credenciais ORDER BY titulo ASC")
    return cursor.fetchall()

def atualizar_credencial(conn, id_credencial: int, titulo: str, usuario: str, senha_criptografada: bytes):
    """Atualiza os dados de uma credencial existente pelo ID."""
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE credenciais
        SET titulo = ?, usuario = ?, senha_criptografada = ?
        WHERE id = ?
    """, (titulo, usuario, senha_criptografada, id_credencial))
    conn.commit()

def remover_credencial(conn, id_credencial: int):
    """Remove uma credencial específica pelo ID."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM credenciais WHERE id = ?", (id_credencial,))
    conn.commit()