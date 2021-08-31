from models import Pessoas, Usuarios


def insere_pessoas():
    pessoa = Pessoas(nome='Caique', idade=28)
    print(pessoa)
    pessoa.save()


def consulta_pessoas():
    pessoas = Pessoas.query.all()
    print(pessoas)
    pessoa = Pessoas.query.filter_by(nome='Jacob').first()
    print(pessoa.idade)


def altera_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Jacob').first()
    pessoa.idade = 30
    pessoa.save()


def exclui_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Felipe').first()
    pessoa.delete()


def insere_usuario(login, senha):
    usuario = Usuarios(login=login, senha=senha)
    usuario.save()


def consulta_todos_usuarios():
    usuarios = Usuarios.query.all()
    print(usuarios)


if __name__ == '__main__':
    #insere_pessoas()
    insere_usuario('Jacobi', '1234')
    insere_usuario('kalu', '4321')
    consulta_todos_usuarios()
    # altera_pessoa()
    # exclui_pessoa()
    # consulta_pessoas()
