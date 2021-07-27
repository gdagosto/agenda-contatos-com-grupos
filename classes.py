from __future__ import annotations
from typing import Dict, List

LIMITE_AGENDA = 75

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
        return True

    @staticmethod
    def verificar_telefone(string):
        return True

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
                    print('entrou')
                    lista_out.append(novo_item)
            elif inp.isdigit() and 0 <= int(inp) <= len(lista_out):
                lista_out.pop(int(inp) - 1)

        return lista_out


class Agenda:
    def __init__(self, contatos):
        self.contatos = contatos
        self.grupos: Dict[str, Grupo] = {}

    def listar_contatos(self):
        for objeto in self.contatos:
            lista_contato = [objeto.nome+' '+objeto.sobrenome, objeto.id]
            print(lista_contato)
        pass

    def pesquisar_contatos(self):
        pass

    def detalhar_contato(self):
        identificador = int(input('Digite o id do contato:'))
        contato = self.find_contato_by_id(identificador)
        print(contato)
        pass

    def adicionar_contato(self):
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

        # Remove contato da lista de contatos
        self.contatos.remove(contato)

        # Remove contato de cada grupo
        for grupo in self.grupos:
            grupo.remover_contato(contato)

    def __repr__(self):
        return (f'Este objeto pertence a classe {Agenda.__name__} e é uma lista de contatos')

    def criar_grupo(self):
        #TODO: Consertar o fato de q qdo o ID não existe ele adiciona um NONE
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
                ids = inp.split(",")  # ids recebe uma lista de números gravados como string
                if not ids:
                    break
                if all([i.isdigit() for i in ids]):
                    lista_contatos = [self.find_contato_by_id(int(_id)) for _id in ids if _id]
                    novo_grupo = Grupo(lista_contatos, nome_grupo)
                    self.grupos[nome_grupo] = novo_grupo
                    break
                else:  # caso tenha colocado a,2,5,a,charles
                    # TODO: ofender usuário
                    print("Preencha apenas números entre vírgulas, ex: 1,2,3")

    def alterar_grupo(self):
        pass

    def remover_grupo(self):
        pass

    def executar(self):
        pass


class Grupo:
    #    grupos: Dict[str, Grupo] = {}

    def __init__(self, contatos: List[Contato], nome: str):
        self.contatos = contatos
        #Grupo.grupos[nome] = self

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
