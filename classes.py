from __future__ import annotations
from typing import Dict, List
from constantes import LIMITE_AGENDA
import re


class Contato:
    curr_id = 1  # valor de Id do contato

    def __init__(self, nome, sobrenome='', emails=[], telefones=[]):
        self.id = Contato.curr_id
        self.nome = nome
        self.sobrenome = sobrenome
        self.emails = emails
        self.telefones = telefones

        if Contato.curr_id > LIMITE_AGENDA:
            raise Exception(f"Limite de contatos ({LIMITE_AGENDA}) na agenda atingido!")
        Contato.curr_id += 1

    def __repr__(self):
        return f'''id: {self.id} | nome: {self.nome} {self.sobrenome} 
    emails: {self.emails}
    telefones: {self.telefones}'''

    @staticmethod
    def verificar_email(string):
        return re.search(r'^[\w\-\.]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,3}$', string)

    @staticmethod
    def verificar_telefone(string):
        return re.search('^(\(?[0-9]{2,3}\)?)? ?(?:[2-8]|9[1-9])[0-9]{3}\-?[0-9]{4}$', string)


    def edita_emails(self):
        self.emails = self.edita_lista(self.emails, 'E-mails', self.verificar_email)

    def edita_telefones(self):
        self.telefones = self.edita_lista(self.telefones, 'Telefones', self.verificar_telefone)

    @staticmethod
    def edita_lista(lista_in, titulo='Lista', validacao=''):
        lista_out = lista_in[:]

        while True:
            print('\n\n' + '-'*4 + f'[ {titulo} ]' + '-'*(42-len(titulo)))
            if len(lista_out) == 0:
                print('  Não há itens na lista')
            else:
                for _id, item in enumerate(lista_out):
                    print(f'  {_id+1}: {item}')
            print('-'*50)
            print('Digite 0 para inserir um novo item na lista')
            if len(lista_out) > 0:
                print('Digite o número correspondente para removê-lo da lista')
            print('Deixe em branco e aperte Enter para sair')
            inp = input('    > ')
            if inp == '':
                break
            if inp == '0':
                novo_item = input('Digite o valor do novo item: ')

                if validacao == '' or (callable(validacao) and validacao(novo_item)):
                    lista_out.append(novo_item)
                else:
                    print("O dado inserido é inválido!")
            elif inp.isdigit() and 0 <= int(inp) <= len(lista_out):
                lista_out.pop(int(inp) - 1)

        return lista_out


class Agenda:
    def __init__(self, contatos):
        if len(contatos) > 75:
            print("O tamanho máximo da Agenda é 75 contatos, foram importados apenas os 75 primeiros.")
        self.contatos = contatos[:75]
        self.grupos: Dict[str, Grupo] = {}

    def listar_contatos(self):
        for objeto in self.contatos:
            lista_contato = [objeto.nome+' '+objeto.sobrenome, objeto.id]
            print(lista_contato)

    def pesquisar_contatos(self):
        pass

    def detalhar_contato(self):
        print('Digite o id do contato para detalhar, ou deixe em branco para sair:')
        identificador = input('    ►')
        if not identificador.isdigit():
            return
        contato = self.find_contato_by_id(int(identificador))
        if not contato:
            print("O contato não foi encontrado")
            return
        print(contato)

    def adicionar_contato(self):
        if len(self.contatos) >= 75:
            print("O tamanho máximo da Agenda é 75 contatos, não se pode adicionar mais contatos.")
            return
        print(' ADICIONAR CONTATO ')
        nome = input('Nome: ')
        sobrenome = input('Sobrenome: ')

        novo_contato = Contato(nome, sobrenome)

        novo_contato.edita_emails()
        novo_contato.edita_telefones()

        self.contatos.append(novo_contato)

    def find_contato_by_id(self, _id) -> Contato:
        for contato in self.contatos:
            if contato.id == _id:
                return contato
        return

    def alterar_contato(self):
        print(' ALTERAR CONTATO ')
        self.listar_contatos()  # Exibe a lista de contatos com os ids
        print('Insira o id do contato que deseja alterar, ou deixe em branco para sair.')
        inp = input('    > ')

        if inp.isdigit():
            self.alterar_contato_by_id(int(inp))

    def alterar_contato_by_id(self, _id):
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

    def remover_contato(self):
        print(' REMOVER CONTATO ')
        self.listar_contatos()  # Exibe a lista de contatos com os ids
        print('Insira o id do contato que deseja remover, ou deixe em branco para sair.')
        inp = input('    > ')

        if inp.isdigit():
            self.remover_contato_by_id(int(inp))

    def remover_contato_by_id(self, _id):
        contato = self.find_contato_by_id(_id)
        if not(contato):
            return

        print(f"Contato removido: {contato}")

        # Remove contato da lista de contatos
        self.contatos.remove(contato)

        # Remove contato de cada grupo
        for grupo in self.grupos.values():
            grupo.remover_contato(contato)

    def __repr__(self):
        return (f'Este objeto pertence a classe {Agenda.__name__} e é uma lista de contatos')

    def criar_grupo(self):
        # TODO: Consertar o fato de q qdo o ID não existe ele adiciona um NONE
        print(' CRIAR GRUPO ')
        self.listar_contatos()  # Exibe a lista de contatos com os ids
        while True:
            print('Insira o nome do Grupo ou deixe em branco para sair.')
            inp = input('    > ')
            if not inp:
                break
            nome_grupo = inp
            while True:
                print('Digite os ids para adicionar a este grupo (separados por vírgula) ou em branco para sair:')
                inp = input('    > ')
                if not inp:
                    print(f"Grupo {nome_grupo} cancelado!!")
                    break
                ids = inp.split(",")  # ids recebe uma lista de números gravados como string
                if all([i.isdigit() for i in ids]):
                    lista_contatos = [self.find_contato_by_id(int(_id)) for _id in ids if _id]
                    if None in lista_contatos:
                        print("Preencha apenas IDs válidos entre vírgulas.")
                    else:
                        novo_grupo = Grupo(lista_contatos)
                        self.grupos[nome_grupo] = novo_grupo
                        print(f"Grupo {nome_grupo} criado com sucesso")
                        break
                else:  # caso tenha colocado a,2,5,a,charles
                    # TODO: ofender usuário
                    print("Preencha apenas números entre vírgulas, ex: 1,2,3")

    def alterar_grupo(self):
        pass

    def remover_grupo(self):
        pass

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

    def executar(self):
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
                    # TODO: Separar em método externo
                    titulo = "Grupos"
                    lista_grupos = list(self.grupos.keys())
                    print('\n\n' + '-'*4 + f'[ {titulo} ]' + '-'*(42-len(titulo)))
                    if len(lista_grupos) == 0:
                        print('  Não há itens na lista')
                    else:
                        for _id, item in enumerate(lista_grupos):
                            print(f'  {_id+1}: {item}')
                    print('-'*50)
                    if len(lista_grupos) > 0:
                        print('Digite o número correspondente para removê-lo da lista')
                    print('Deixe em branco e aperte Enter para sair')
                    inp = input('    > ')
                    if inp == '':
                        break
                    elif inp.isdigit() and 0 <= int(inp) <= len(lista_grupos):
                        print(self.grupos[lista_grupos[int(inp)-1]])
            # → 6 para salvar a agenda,
            elif user_input == "7":
                pass
            else:
                break


class Grupo:

    def __init__(self, contatos: List[Contato]):
        self.contatos = contatos

    def __repr__(self) -> str:
        repr = ""
        for c in self.contatos:
            repr += c.__repr__() + "\n"
        return repr

    def listar_contatos(self):
        for objeto in self.contatos:
            lista_contato = [objeto.nome+' '+objeto.sobrenome, objeto.id]
            print(lista_contato)

    def adicionar_contato(self, contato):
        self.contatos.append(contato)

    def find_contato_by_id(self, _id) -> Contato:
        for contato in self.contatos:
            if contato.id == _id:
                return contato
        return

    def remover_contato(self, arg):
        """ Remove contato do Grupo, uso:\n
        ...   grp.remover_contato(2) ==> passar o ID a remover\n
        ...   grp.remover_contato(meuContato) ==> passa direto um objeto Contato
        """
        if type(arg) != Contato:
            self.remover_contato_by_id(int(arg))
        else:
            self.remover_contato_by_id(arg.id)

    def remover_contato_by_id(self, _id):
        contato = self.find_contato_by_id(_id)
        if not(contato):
            return
        # Remove contato do grupo
        self.contatos.remove(contato)
