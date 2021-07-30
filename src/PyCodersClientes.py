import csv
from src.Contato import Contato
from src.Grupo import Grupo
from src.constantes import NOME, TELEFONE, EMAIL, GRUPOS, DELIMITER
from typing import Dict, List, Tuple
import src.verificacoes as verificacoes

class PyCodersClientes:
    @staticmethod
    def carrega_arquivo_csv(nome_arquivo: str) -> Tuple[List[Contato], Dict[str, Grupo]]:
        '''
        Método que carrega o arquivo csv e retorna um lista de Contatos e um Dicionário de Grupos
        '''
        with open(nome_arquivo, 'r', encoding='utf-8') as file_inicial:
            tabela_suja = csv.reader(
                file_inicial, delimiter=";", lineterminator="\n")

            colunas_embaralhadas = False
            # Verifica em que formato está o csv. Para tal, vamos checar a coluna de e-mails e ver se todos são e-mails
            for linha in tabela_suja:
                emails = linha[EMAIL].split(DELIMITER)
                if not all([Contato.verificar_email(email) for email in emails]):
                    colunas_embaralhadas = True
                    break

            # Reinicia o arquivo
            file_inicial.seek(0)

            print(f'Carregando os dados do arquivo {nome_arquivo}...')
            if colunas_embaralhadas:
                # Se entrar aqui, o arquivo nunca foi salvo antes e precisa ser ajustado
                print(
                    f'Ops! Parece que o estagiário da PyCoders embaralhou as colunas do arquivo {nome_arquivo}.')
                print("Colunas sendo ajustadas...")
                print('Não se preocupe! As colunas já foram ajustadas')
                lista_contatos_por_linhas = PyCodersClientes.ajusta_colunas(
                    tabela_suja)
                contatos: List[Contato] = [
                    Contato(nome=linha[NOME], emails=[
                            linha[EMAIL]], telefones=[linha[TELEFONE]])
                    for linha in lista_contatos_por_linhas
                ]
                grupos: Dict[str, Grupo] = {}

            else:
                # Se entrar aqui, o arquivo já foi salvo ao menos uma vez e já está ajustado
                lista_contatos_por_linhas: List[List[str]] = PyCodersClientes.preenche_colunas(
                    tabela_suja)
                contatos_e_grupos: List[Tuple[Contato, List[str]]] = [
                    (PyCodersClientes.inicializa_contato(linha), linha[GRUPOS]) for linha in lista_contatos_por_linhas
                ]
                contatos: List[Contato] = [linha[0]
                                           for linha in contatos_e_grupos]
                grupos = PyCodersClientes.inicializa_grupos(contatos_e_grupos)

        return contatos, grupos

    @staticmethod
    def inicializa_contato(linha: List[str]) -> Contato:
        ''''
        Pegará cada linha da lista com as informações de cada contato (listas) e 
        criará um objeto da classe contato 
        FIXME: Não é o ideal, mas verifica se o nome tem sobrenome aqui
        '''
        if DELIMITER in linha[NOME]:
            nome, sobrenome = linha[NOME].split(DELIMITER)
        else:
            nome, sobrenome = linha[NOME], ''

        return Contato(nome=nome, sobrenome=sobrenome, emails=linha[EMAIL], telefones=linha[TELEFONE])

    @staticmethod
    def ajusta_colunas(tabela_suja) -> List[List[str]]:
        '''
        Se entrar aqui, o arquivo nunca foi salvo antes e precisa ser ajustado.
        Arquivo irá verificar cada linha do arquivo CSV e em cada linha irá verificar cada campo
        para descobrir se é um nome, email ou telefone
        '''
        listas: List[List[str]] = [[], [], []]

        for linha in tabela_suja:
            for campo in linha:
                coluna = verificacoes.identifica_coluna(campo)
                if coluna in [NOME, TELEFONE, EMAIL]:
                    listas[coluna].append(campo)
                else:
                    print(campo)

        return list(zip(*listas))

    @staticmethod
    def preenche_colunas(tabela_suja: List[List[str]]) -> List[List[str]]:
        '''Se entrar aqui, o arquivo já foi salvo ao menos uma vez e já está ajustado
        Função irá percorrer cada linha do arquivo csv e para cada campo irá quebrar as strings no caracter "|" formando
        listas de dados (str). Retornando uma lista com várias listas de dados
        Exp: Campo emails gabriel@gmail|charles@gmail.com se tornará [gabriel@gmail.com,charles@gmail.com]
        '''
        listas: List[List[str]] = []

        for linha in tabela_suja:
            linha[EMAIL] = linha[EMAIL].split(DELIMITER)
            linha[TELEFONE] = linha[TELEFONE].split(DELIMITER)
            linha[GRUPOS] = linha[GRUPOS].split(DELIMITER)
            listas.append(linha)

        return listas

    @staticmethod
    def inicializa_grupos(contatos_e_grupos: List[Tuple[Contato, List[str]]]) -> Dict[str, Grupo]:
        '''
        Recebe um par: lista de objetos Contato e lista de nomes de grupo.
        A partir dai cria um dicionário que os valores são os objetos Contato que tem um determinado
        em comum. A chave desse dicionário será um dos nomes dos grupos que a função recebeu.
        Por mim ele usa esses dicionários para criar objetos da classe Grupo que são dicionários
        com o nome do grupo como a chave e o grupo de contatos como valor
        '''
        nomes_e_listas_de_contato: Dict[str, List[Contato]] = {}
        for contato, pertence_a in contatos_e_grupos:
            for g in pertence_a:
                if g in nomes_e_listas_de_contato:  # Adiciona no grupo
                    nomes_e_listas_de_contato[g].append(contato)
                elif g != '':  # Inicializa o grupo
                    nomes_e_listas_de_contato[g] = [contato]

        grupos: Dict[str, Grupo] = {}  # Dict[nomes,Grupos]
        for nome_grupo in nomes_e_listas_de_contato:
            grupos[nome_grupo] = Grupo(
                nome_grupo, nomes_e_listas_de_contato[nome_grupo])
        return grupos
