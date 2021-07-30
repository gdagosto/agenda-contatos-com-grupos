from __future__ import annotations
from typing import List
from src.Contato import Contato

class Grupo:

    def __init__(self, nome: str, contatos: List[Contato]):
        self.contatos = contatos
        self.nome = nome

    def __repr__(self) -> str:
        representacao = "-"*50
        representacao += f"\n Grupo: {self.nome} \n"
        representacao += "-"*50
        representacao += "\n"
        for c in self.contatos:
            representacao += c.__repr__() + "\n\n"
        return representacao