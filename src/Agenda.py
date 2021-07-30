from src.Contato import Contato
from src.constantes import DELIMITER, NOME_ARQUIVO
from typing import Dict, List
from src.Grupo import Grupo
import csv

class Agenda:
    def __init__(self, contatos: List[Contato], grupos: Dict[str, Grupo] = {}) -> None:
        if len(contatos) > 75:
            print(
                "O tamanho máximo da Agenda é 75 contatos, foram importados apenas os 75 primeiros.")
        self.contatos = contatos[:75]
        self.grupos = grupos

    def listar_contatos(self) -> None:
        '''
        Método exibe cada contato com o nome, sobrenome e id único
        '''
        titulo = "Contatos"
        print('\n\n' + '-'*4 +
              f'[ {titulo} ]' + '-'*(42-len(titulo)))
        if len(self.contatos) == 0:
            print('  Não há itens na lista')
        else:
            for contato in self.contatos:
                print(
                    f'  id: {str(contato.id).rjust(2)} | {contato.nome} {contato.sobrenome}')
        print('-'*50)

    def detalhar_contato(self) -> None:
        '''
        Método que recebe do usuário um input de ID e printa todos os dados do contato (id, nome, sobrenome, email,telefones)
        '''
        print('Digite o id do contato para detalhar, ou deixe em branco para sair:')
        identificador = input('    ►')
        if not identificador.isdigit():
            return
        contato = self.find_contato_by_id(int(identificador))
        if not contato:
            print("O contato não foi encontrado")
            return
        print(contato)

    def adicionar_contato(self) -> None:
        '''
        Método que recebe um input obrigatório de nome e sobrenome do usuário e cria um objeto contato.
        Além disso é dada a opção de adicionar telefones e e-mail.
        
        '''
        if len(self.contatos) >= 75:
            print(
                "O tamanho máximo da Agenda é 75 contatos, não se pode adicionar mais contatos.")
            return
        print(' ADICIONAR CONTATO ')
        nome = input('Nome: ')
        sobrenome = input('Sobrenome: ')

        novo_contato = Contato(nome, sobrenome)

        novo_contato.edita_emails()
        novo_contato.edita_telefones()

        self.contatos.append(novo_contato)

    def find_contato_by_id(self, _id: int) -> Contato:
        '''
        Método que recebe um ID e retorna um objeto Contato, caso ele esteja na lista de contatos. Se não ele retorna none.
        '''
        for contato in self.contatos:
            if contato.id == _id:
                return contato
        return

    def alterar_contato(self) -> None:
        '''
        Método que permite ao usuário alterar um contato a partir de um input dele de ID
        '''
        print(' ALTERAR CONTATO ')
        self.listar_contatos()  # Exibe a lista de contatos com os ids
        print('Insira o id do contato que deseja alterar, ou deixe em branco para sair.')
        inp = input('    > ')

        if inp.isdigit():
            self.alterar_contato_by_id(int(inp))

    def alterar_contato_by_id(self, _id: int) -> None:
        '''
        Método que permite o usuário alterar os atributos de um contato a partir de um ID
        '''
        contato = self.find_contato_by_id(_id)
        if not(contato):
            return
        novo_nome = input(f'Nome [{contato.nome}]: ')
        if novo_nome != '':
            contato.nome = novo_nome

        novo_sobrenome = input(f'Sobrenome [{contato.sobrenome}]: ')
        if novo_sobrenome != '':
            contato.sobrenome = novo_sobrenome

        contato.edita_emails()

        contato.edita_telefones()

    def remover_contato(self) -> None:
        '''
        Método que recebe um input de ID do usuário e remove um contato da agenda a partir desse ID
        '''
        print(' REMOVER CONTATO ')
        self.listar_contatos()  # Exibe a lista de contatos com os ids
        print('Insira o id do contato que deseja remover, ou deixe em branco para sair.')
        inp = input('    > ')

        if inp.isdigit():
            self.remover_contato_by_id(int(inp))

    def remover_contato_by_id(self, _id: int) -> None:
        '''
        Método recebe um input de ID e remove o contato da lista de contatos.
        Além disso ele verifica se o contato está presente em algum grupo e também o remove do grupo
        '''
        contato = self.find_contato_by_id(_id)
        if not(contato):
            return

        print(f"Contato removido: {contato}")

        # Remove contato da lista de contatos
        self.contatos.remove(contato)

        # Remove contato de cada grupo
        for grupo in self.grupos.values():
            grupo.contatos.remove(contato)

    def criar_grupo(self) -> None:
        '''
        Método de cria os grupos a partir de inputs de ID dos usuários que ele deseja adicionar no grupo
        '''
        print(' CRIAR GRUPO ')
        self.listar_contatos()  # Exibe a lista de contatos com os ids
        while True:
            print('Insira o nome do Grupo ou deixe em branco para sair.')
            inp = input('    > ')
            if not inp:
                break
            nome_grupo = inp
            while True:
                print(
                    'Digite os ids para adicionar a este grupo (separados por vírgula) ou em branco para sair:')
                inp = input('    > ')
                if not inp:
                    print(f"Grupo {nome_grupo} cancelado!!")
                    break
                # ids recebe uma lista de números gravados como string
                ids = set(inp.split(","))
                if all([i.isdigit() for i in ids]):
                    lista_contatos = [self.find_contato_by_id(
                        int(_id)) for _id in ids if _id]
                    if None in lista_contatos:
                        print("Preencha apenas IDs válidos entre vírgulas.")
                    else:
                        novo_grupo = Grupo(nome_grupo, lista_contatos)
                        self.grupos[nome_grupo] = novo_grupo
                        print(f"Grupo {nome_grupo} criado com sucesso")
                        break
                else:  # caso tenha colocado a,2,5,a,charles
                    print("Preencha apenas números entre vírgulas, ex: 1,2,3")

    @staticmethod
    def input_menu_principal() -> str:
        '''
            Faz o print da mensagem do menu PRINCIPAL e aguarda input do usuário
            para que escolha uma das opções, retorna o valor inputado.
        '''
        print('''
        ###################################################################
        ###            Cadastro Clientes PyCoders - Menu                ###
        ###################################################################

        Digite sua opção e pressione ENTER: 
        → 1 para listar contatos, 
        → 2 para adicionar contato, 
        → 3 para alterar contato,
        → 4 para remover contato,
        → 5 para criar os grupos,
        → 6 para exibir os contatos dos grupos,
        → 7 para salvar a agenda,
        → Digite qualquer outro caracter para sair sem salvar:''')
        return input("►")

    def para_lista(self) -> List[List[str]]:
        '''
        Função pega os valores de cada grupo (lista de objetos Contato) e cria um dicionário com o ID
        de cada contato e o nome do grupo que ele pertence. Ela faz isso para grupo e adiciona nos valores
        desse dicionário, que é vinculado ao ID único de cada usuário, o nome dos grupos que ele percente.

        Depois ela pega cada contato, chamada uma função que quebra o objeto Contato em uma lista de strings
        com os atributos sendo as strings dessa lista e junta essa lista com os valores do dicionário com os nomes
        dos grupos que cada contato participa. Para adicionar uma lista de strings com os valores do dicionário
        é necessário transformar os valores do dicionário em uma lista.
        '''

        lista_contatos: List[List[str]] = []
        contatos_grupos: Dict[int, str] = {}

        for contato in self.contatos:
            contatos_grupos[contato.id] = ''

        for grupo in self.grupos.values():
            for contato in grupo.contatos:
                if contatos_grupos[contato.id] != '':
                    contatos_grupos[contato.id] += DELIMITER
                contatos_grupos[contato.id] += grupo.nome

        for contato in self.contatos:
            serialized_contato = contato.para_lista_contato()
            linha = serialized_contato + [contatos_grupos[contato.id]]
            lista_contatos.append(linha)

        return lista_contatos

    def executar(self) -> None:
        '''
        Faz o loop principal da agenda
        '''
        while True:
            user_input = Agenda.input_menu_principal()

            if user_input == "1":
                self.listar_contatos()
                self.detalhar_contato()

            elif user_input == "2":
                self.adicionar_contato()

            elif user_input == "3":
                self.alterar_contato()

            elif user_input == "4":
                self.remover_contato()

            elif user_input == "5":
                self.criar_grupo()

            elif user_input == "6":
                while True:
                    titulo = "Grupos"
                    lista_grupos = list(self.grupos.keys())
                    print('\n\n' + '-'*4 +
                          f'[ {titulo} ]' + '-'*(42-len(titulo)))
                    if len(lista_grupos) == 0:
                        print('  Não há itens na lista')
                    else:
                        for _id, item in enumerate(lista_grupos):
                            print(f'  {_id+1}: {item}')
                    print('-'*50)
                    if len(lista_grupos) > 0:
                        print(
                            'Digite o número correspondente para detalhá-lo')  # essa linha mudou para não dizer "remover"
                    print('Deixe em branco e aperte Enter para sair')
                    inp = input('    > ')
                    if inp == '':
                        break
                    elif inp.isdigit() and 0 <= int(inp) <= len(lista_grupos):
                        print(self.grupos[lista_grupos[int(inp)-1]])
            elif user_input == "7":  # Salvar
                lista_out = self.para_lista()
                with open(NOME_ARQUIVO, 'w', encoding='utf-8') as arquivo_out:
                    csv.writer(arquivo_out, delimiter=";",
                               lineterminator="\n").writerows(lista_out)
                print(f'Dados salvos com sucesso no arquivo {NOME_ARQUIVO}')

            else:
                break