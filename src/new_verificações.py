import re

def verificar_email(emails):
    return re.search(r'^[\w-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,3}$', emails)

valido = verificar_email(emails)


if valido:
    print(emails, 'É um e-mail válido!')
else:
    print('Formato de e-mail inválido!:', emails)

#%%

if __name__ == '__main__':
    emails = [input() for _ in range (int(input()))]

  valido = (r'^[\w-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,3}$')
  
  validado = r.compile(padrao)

  for e in emails:
    print('E-mail válido' if validado.search(t) else 'E-mail Inválido')

#%%
import re

def verificar_telefone(telefones):
    return re.search('^\(?[1-9]{2,3}\)? ?(?:[2-8]|9[1-9])[0-9]{3}\-?[0-9]{4}$', telefones)


correto = verificar_telefone(telefones)

if correto:
    
    print(telefones, 'É um telefone válido!')
else:
    print('Telefone inválido!:', telefones)

#%%
if __name__ == '__main__':
  telefones = [input() for _ in range (int(input()))]

  padrao = '^\(?[1-9]{2,3}\)? ?(?:[2-8]|9[1-9])[0-9]{3}\-?[0-9]{4}$'
  validador = r.compile(padrao)

  for t in telefones:
    print('válido' if validador.search(t) else 'Inválido')