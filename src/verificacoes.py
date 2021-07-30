from src.constantes import NOME, TELEFONE, EMAIL
from src.Contato import Contato

def valida_caracteres_validos(valor: str, caracteres: str) -> bool:
    caracteres = caracteres.lower()
    for letra in valor.lower():
        if letra not in caracteres:
            return False
    return True

def is_nome(valor: str) -> bool:
    '''
        Dado uma string qualquer, identifica se é um nome válido
    '''
    if (valor.strip() == ''):
        return False
    caracteres_validos = "abcdefghijklmnopqrstuvwxyzç'-áéíóúâêîôûàèìòùäëïöüãõ "
    return valida_caracteres_validos(valor, caracteres_validos)

def identifica_coluna(valor: str) -> int:
    if Contato.verificar_telefone(valor):
        return TELEFONE
    if Contato.verificar_email(valor):
        return EMAIL
    if is_nome(valor):
        return NOME
    return -1