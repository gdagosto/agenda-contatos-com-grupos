# %%

try:
    import csv
    import verificacoes  # usado do trabalho anterior
    from typing import List
    import sys  # ops

except ImportError:
    print(
        f"Verifique se os módulos de importação estão instalados ou presentes no diretório usado\n{sys.exc_info()[1]}")


class Contato:
    curr_id = 1  # valor de Id do contato, inicia em 1

    def __init__(self, nome: str, telefones: List[str] = [], emails: List[str] = [], sobrenome: str = '') -> None:
        self.id = Contato.curr_id
        self.nome = nome
        self.sobrenome = sobrenome
        self.emails = emails
        self.telefones = telefones

        Contato.curr_id += 1

    # somente para ficar fácil de visualizar como está saindo cada contato e a lista de contatos (na versão final podemos deletar)
    def __repr__(self):
        return f"""{self.__class__.__name__}(id = {self.id}, nome = {self.nome}, sobrenome = {self.sobrenome}, tel = {self.telefones}, email = {self.emails})"""

# somente para conseguir instanciar e testar o código na (versão final podemos deletar)


class Agenda:
    def __init__(self, contatos):
        self.contatos = contatos


def organiza_lista(lista_vazia: List[List[str]]) -> List[List[str]]:
    '''
    Função abre um arquivo CSV com campos desorganizados e para cada campo chama uma função de verificação de qual coluna o arquivo deveria estar 0 - nome, 1-telefone e 3 -email.
    Após essa verificação, o campo é adicionado na coluna correta e é retornado uma lista com 3 listas (lista de nomes, lista de telefones e lista de emails), porém organizada. 
    '''

    try:
        with open("contatos.csv", "r", encoding="utf-8") as file_inicial:
            tabela_suja = csv.reader(file_inicial, delimiter=";", lineterminator="\n")
            for linha in tabela_suja:
                for campo in linha:
                    lista_vazia[verificacoes.identifica_coluna(campo)].append(campo)
        lista_preenchida = lista_vazia  # somente para facilitar a leitura
        return lista_preenchida
    except FileNotFoundError:
        print(f"Arquivo não está no diretório especificado ou não existe\n{sys.exc_info()[1]}")


lista_vazia: List[List[str]] = [[],
                                [],
                                []]
lista_organizada_por_colunas = organiza_lista(lista_vazia)  # lista com 3 listas de 25 items cada
lista_organizada_por_linhas = list(zip(*lista_organizada_por_colunas))  # lista com 25 listas de 3 items cada


# %%
# tipagem para mostrar que é uma lista de listas de objetos Contato
lista_contatos_preenchida: List[List[Contato]] = [
    Contato(*lista_organizada_por_linhas[i]) for i in range(len(lista_organizada_por_linhas))]

# %%
agenda = Agenda(lista_contatos_preenchida)
