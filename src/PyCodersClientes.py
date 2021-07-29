import csv
from src.Contato import Contato
from src.Grupo import Grupo
from src.constantes import NOME, TELEFONE, EMAIL, GRUPOS, DELIMITER
from typing import List
import src.verificacoes as verificacoes

class PyCodersClientes:
    @staticmethod
    def carrega_arquivo_csv(nome_arquivo):
        with open(nome_arquivo, 'r', encoding='utf-8') as file_inicial:
            tabela_suja = csv.reader(file_inicial, delimiter=";", lineterminator="\n")

            colunas_embaralhadas = False
            # Verifica em que formato está o csv. Para tal, vamos checar a coluna de e-mails e ver se todos são e-mails
            for linha in tabela_suja:
                emails = linha[EMAIL].split(DELIMITER)
                if not all([Contato.verificar_email(email) for email in emails]):
                    colunas_embaralhadas = True
                    break
            
            # Reinicia o arquivo
            file_inicial.seek(0)

            print(f'Carregando os dados do arquivo {nome_arquivo}')
            if colunas_embaralhadas:
                # Se entrar aqui, o arquivo nunca foi salvo antes e precisa ser ajustado
                print(f'Ops! Parece que o estagiário da PyCoders embaralhou as colunas do arquivo {nome_arquivo}.')
                print('Não se preocupe! As colunas já foram ajustadas')
                lista_contatos_por_linhas = PyCodersClientes.ajusta_colunas(tabela_suja)
                contatos: List[List[Contato]] = [
                    Contato(nome=linha[NOME], emails=[linha[EMAIL]], telefones=[linha[TELEFONE]]) 
                    for linha in lista_contatos_por_linhas
                ]
                grupos = {}

            else:
                # Se entrar aqui, o arquivo já foi salvo ao menos uma vez e já está ajustado
                lista_contatos_por_linhas = PyCodersClientes.preenche_colunas(tabela_suja)
                contatos_e_grupos: List[List[Contato]] = [
                    (PyCodersClientes.inicializa_contato(linha), linha[GRUPOS]) for linha in lista_contatos_por_linhas
                ]
                contatos = [linha[0] for linha in contatos_e_grupos]
                grupos = PyCodersClientes.inicializa_grupos(contatos_e_grupos)
       
        
        return contatos, grupos
                                                 
    @staticmethod
    def inicializa_contato(linha):
        # FIXME: Não é o ideal, mas verifica se o nome tem sobrenome aqui
        if DELIMITER in linha[NOME]:
            nome, sobrenome = linha[NOME].split(DELIMITER)
        else:
            nome, sobrenome = linha[NOME], ''

        return Contato(nome=nome, sobrenome=sobrenome, emails = linha[EMAIL], telefones = linha[TELEFONE])

    @staticmethod
    def ajusta_colunas(tabela_suja):
        # Se entrar aqui, o arquivo nunca foi salvo antes e precisa ser ajustado
        listas: List[List[str]] = [[],[],[]]

        for linha in tabela_suja:
            for campo in linha:
                coluna = verificacoes.identifica_coluna(campo)
                if coluna in [NOME, TELEFONE, EMAIL]:
                    listas[coluna].append(campo)   
        return list(zip(*listas))
    
    @staticmethod
    def preenche_colunas(tabela_suja):
        # Se entrar aqui, o arquivo já foi salvo ao menos uma vez e já está ajustado
        listas: List[List[str]] = []

        for linha in tabela_suja:
            linha[EMAIL] = linha[EMAIL].split(DELIMITER)
            linha[TELEFONE] = linha[TELEFONE].split(DELIMITER)
            linha[GRUPOS] = linha[GRUPOS].split(DELIMITER)
            listas.append(linha)

        return listas

    @staticmethod
    def inicializa_grupos(contatos_e_grupos):
        grupos = {}
        for contato, pertence_a in contatos_e_grupos:
            for g in pertence_a:
                if g in grupos: # Adiciona no grupo
                    grupos[g].append(contato)
                elif g != '': # Inicializa o grupo
                    grupos[g] = [contato]

        for g in grupos:
            grupos[g] = Grupo(g, grupos[g])
        return grupos
