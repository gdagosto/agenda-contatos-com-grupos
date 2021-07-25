class Contato:
    curr_id = 1 # valor de Id do contato 
    
    def __init__(self,nome,sobrenome = '',emails = [],telefones = []):
        self.id = Contato.curr_id
        self.nome = nome
        self.sobrenome = sobrenome
        self.emails = emails
        self.telefones = telefones

        Contato.curr_id += 1

    @staticmethod
    def verificar_email(string):
        pass

    @staticmethod
    def verificar_telefone(string):
        pass