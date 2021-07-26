from typing import Dict
from src.Contato import Contato
from __future__ import annotations

class Grupo:
    grupos: Dict[str, Grupo] = {}

    def __init__(self, contatos, nome):
        self.contatos = contatos
        Grupo.grupos[nome] = self

    def listar_contatos(self):
        for objeto in self.contatos:
            lista_contato = [objeto.nome+' '+objeto.sobrenome, objeto.id]
            print(lista_contato)
        pass

    def adicionar_contato(self, contato):
        self.contatos.append(contato)

    def find_contato_by_id(self, _id):
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

    def criar_grupo(self):
        pass

    def alterar_grupo(self):
        pass

    def remover_grupo(self):
        pass

    def executar(self):
        pass
    