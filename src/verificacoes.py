from constantes import NOME, TELEFONE, EMAIL
from typing import List

def valida_caracteres_validos(valor: str, caracteres: str) -> bool:
    caracteres = caracteres.lower()
    for letra in valor.lower():
        if letra not in caracteres:
            return False
    return True

def is_telefone(valor: str) -> bool:
    '''
        Dado uma string qualquer, identifica se é um telefone válido
    '''
    caracteres_validos = '0123456789+()- .'
    if (valor.strip() == ''):
        return False
    if not(valida_caracteres_validos(valor, caracteres_validos)):
        return False
    if not(valor.count("(") == valor.count(")") <= 1):
        return False
    if "(" in valor:
        if not(valor.index("(") < valor.index(")")):
            return False
    

    return True


def is_email(valor: str) -> bool:
    '''
        Dado uma string, identifica se é um e-mail válido
        Verificação de e-mail é uma matéria muito complexa.
        Definimos que, para este trabalho, um e-mail válido deve seguir as seguintes regras:
        - Nenhum espaço
        - Apenas 1 caractere de '@'
    '''
    if (valor.strip() == ''):
        return False
    return valor.count('@') == 1 and valor.replace(' ','') == valor


def is_nome(valor: str) -> bool:
    '''
        Dado uma string qualquer, identifica se é um nome válido
    '''
    if (valor.strip() == ''):
        return False
    caracteres_validos = "abcdefghijklmnopqrstuvwxyzç'-áéíóúâêîôûàèìòùäëïöüãõ "
    return valida_caracteres_validos(valor, caracteres_validos)

def identifica_coluna(valor: str) -> int:
    if is_telefone(valor): return TELEFONE
    if is_email(valor): return EMAIL
    if is_nome(valor): return NOME
    return -1


def retorna_indices_na_lista(buscado: str, coluna_lista_in: List[str]) -> List[int]:
    '''
       A partir de uma lista[str] e um valor buscado, retorna uma lista[int] com 
       todos os indices da lista[str] em que o valor buscado está presente
    '''
    buscado = buscado.lower()
    return [i for i, valor in enumerate(coluna_lista_in) if buscado in valor.lower()]
