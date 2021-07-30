from src.Agenda import Agenda
from src.PyCodersClientes import PyCodersClientes
from src.constantes import NOME_ARQUIVO

contatos, grupos = PyCodersClientes.carrega_arquivo_csv(NOME_ARQUIVO)
agenda = Agenda(contatos, grupos)
agenda.executar()