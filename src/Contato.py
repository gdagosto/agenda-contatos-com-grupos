class Contato:
    curr_id = 1  # valor de Id do contato

    def __init__(self, nome, sobrenome='', emails=[], telefones=[]):
        self.id = Contato.curr_id
        self.nome = nome
        self.sobrenome = sobrenome
        self.emails = emails
        self.telefones = telefones

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
