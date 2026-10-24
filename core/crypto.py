import os
import base64
import secrets
import string
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def gerar_salt(tamanho: int = 16) -> bytes:
    """Gera bytes aleatórios para proteger a derivação da senha mestre."""
    return os.urandom(tamanho)

def derivar_chave(senha_mestre: str, salt: bytes) -> bytes:
    """Transforma a senha mestre em uma chave criptográfica de 32 bytes."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480_000,
    )
    chave_crua = kdf.derive(senha_mestre.encode("utf-8"))
    return base64.urlsafe_b64encode(chave_crua)

def criptografar_texto(texto_plano: str, chave: bytes) -> bytes:
    """Criptografa uma string em texto puro usando a chave derivada."""
    f = Fernet(chave)
    return f.encrypt(texto_plano.encode("utf-8"))

def descriptografar_texto(texto_criptografado: bytes, chave: bytes) -> str:
    """Reverte a criptografia e devolve a string original."""
    f = Fernet(chave)
    return f.decrypt(texto_criptografado).decode("utf-8")

def gerar_senha_forte(tamanho: int = 16) -> str:
    """Gera uma senha aleatória contendo letras, números e símbolos."""
    caracteres = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return "".join(secrets.choice(caracteres) for _ in range(tamanho))