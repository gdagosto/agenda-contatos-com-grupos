from __future__ import annotations
from typing import List
from src.constantes import LIMITE_AGENDA, DELIMITER
import re

class Contato:
    curr_id = 1  # valor de Id do contato

    def __init__(self, nome: str, sobrenome: str = '', emails: List[str] = [], telefones: List[str] = []):
        self.id = Contato.curr_id
        self.nome = nome
        self.sobrenome = sobrenome
        self.emails = emails
        self.telefones = telefones

        if Contato.curr_id > LIMITE_AGENDA:
            raise Exception(
                f"Limite de contatos ({LIMITE_AGENDA}) na agenda atingido!")
        Contato.curr_id += 1

    def __repr__(self):
        return f'''id: {self.id} | nome: {self.nome} {self.sobrenome} 
emails: {str(self.emails).strip("[]").replace("'","")}
telefones: {str(self.telefones).strip("[]").replace("'","")}'''

    @staticmethod
    def verificar_email(string: str) -> bool:
        '''
        Método que verifica se o e-mail é válido
        '''
        return bool(re.search(r'''^[\w\-\.]+ # começa com n caracteres (n>=1), podendo ser alfanum, - ou .
                        @ # necessariamente uma arroba
                        (?:[a-zA-Z0-9-]+\.)+ # pelo menos uma vez esse grupo: n caracteres pertencentes ao padrão e termina com um ponto
                        [a-zA-Z]+$ # termina com n letras
                        ''', string, re.VERBOSE))

    @staticmethod
    def verificar_telefone(string: str) -> bool:
        '''
        Método verifica se o telefone é válido
        '''
        return bool(re.search(r'''^(\(?[0-9]{2,3}\)?)? # começa ou não com o DDD, podendo ter parenteses ou não e 2 ou 3 dígitos
                                \ ? # um espaço ou não
                                [0-9]{4,5} # em seguida, 4 ou 5 números
                                \-?\ ? # tracinho ou não
                                [0-9]{4}$ # termina com 4 números''', string, re.VERBOSE))

    def edita_emails(self) -> None:
        '''
        Método atribuirá ao atributo "emails" uma lista de e-mails adicionada pelo usuário
        '''
        self.emails = self.edita_lista(
            self.emails, 'E-mails', self.verificar_email)

    def edita_telefones(self) -> None:
        '''
        Método atribuirá ao atributo "emails" uma lista de e-mails adicionada pelo usuário
        '''
        self.telefones = self.edita_lista(
            self.telefones, 'Telefones', self.verificar_telefone)

    def para_lista_contato(self) -> List[str]:
        '''
        Função pega os atributos do objeto Contato (nome+sobrenome, emails e telefones) e cria
        uma lista com esses dados
        '''
        nome = self.nome + DELIMITER + self.sobrenome if self.sobrenome else self.nome
        telefones = DELIMITER.join(self.telefones)
        emails = DELIMITER.join(self.emails)
        return [nome, telefones, emails]

    @staticmethod
    def edita_lista(lista_in: List[str], titulo: str = 'Lista', validacao: bool = '') -> List[str]:
        '''
        Função que recebe uma lista, exibe ela, dá opção ao usuário de acionar ou remover um item da lista.
        Retorna uma lista editada ou não
        '''
        lista_out: List[str] = lista_in[:]

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
