from src.Contato import Contato


class Agenda:
    def __init__(self, contatos):
        self.contatos = contatos
        self.grupos = {}

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

    def find_contato_by_id(self, _id):
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
            if contato in grupo:
                grupo.remove(contato)

    def __repr__(self):
        return (f'Este objeto pertence a classe {Agenda.__name__} e é uma lista de contatos')
    def criar_grupo(self):
        pass

    def alterar_grupo(self):
        pass

    def remover_grupo(self):
        pass

    def executar(self):
        pass
    