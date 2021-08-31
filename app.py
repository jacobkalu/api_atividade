# Importando as libs necessárias
from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades, Usuarios
from flask_httpauth import HTTPBasicAuth

# nomeando os apps
auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

"""
# Criando os usuários e seus respectivos logins
USUARIOS = {
    'kalu': '321',
    'Jacob': '122'
}"""

"""# Decorando a funcao verificadora de senha
@auth.verify_password
# Criando o método de verificação
def verificacao(login, senha):
    #Verificando se existe login e senha, se houver, login e senha retornará como False
    if not (login, senha):
        return False
    return USUARIOS.get(login) == senha"""

# Decorando a funcao verificadora de senha
@auth.verify_password
# Criando o método de verificação
def verificacao(login, senha):
    #Verificando se existe login e senha, se houver, login e senha retornará como False
    if not (login, senha):
        return False
    return Usuarios.query.filter_by(login=login, senha=senha).first()

# Recuperando os dados por nome de pesssoas e inserindo num dict (response)
class Pessoa(Resource):
    @auth.login_required # Para acessar este método é preciso estar logado
    #Definindo o método de recuperação GET
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        try:
            response = {
                'nome': pessoa.nome,
                'idade': pessoa.idade,
                'id': pessoa.id
            }
        #Tratando erros de atributo ( quando o nome não conta no bd)
        except AttributeError:
            response = {'status': 'erro', 'mensagem': 'Pessoa fora dos registros'}

        return response

    #Definindo o método de alteração PUT
    def put(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        dados = request.json
        if 'nome' in dados:
            pessoa.nome = dados['nome']

        if 'idade' in dados:
            pessoa.idade = dados['idade']

        #Adicionando os dados no bd
        pessoa.save()
        response = {
            'id': pessoa.id,
            'nome': pessoa.nome,
            'idade': pessoa.idade
        }
        return response

    #Definindo o método de exclusão DELETE
    def delete(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        mensagem = 'Pessoa {} excluída com sucesso'.format(pessoa.nome)

        #Excluindo a pesson no bd pela chamandoa função delete()
        pessoa.delete()
        return {'status': 'Sucesso!', 'mensagem':mensagem}


# Definindo o método de listar todas as pessoas no bd
class ListaPessoas(Resource):

    @auth.login_required  # Para acessar este método é preciso estar logado
    # Definindo o método de recuperação GET
    def get(self):
        pessoas = Pessoas.query.all()
        response = [{'id': i.id, 'nome': i.nome, 'idade': i.idade} for i in pessoas]
        return response

    # Definindo o método de inserção POST
    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])

        #Salvando o novo registro no bd com o método pessoa.save definida em util.py
        pessoa.save()
        response = {
            'id': pessoa.id,
            'nome': pessoa.nome,
            'idade': pessoa.idade
        }
        return response

# Definindo os verbos GET, POST, PUT e DELETE pata Atividades
class ListaAtividades(Resource):
    # Recuperando as atividade pelo GET e listando-as
    def get(self):
        atividades = Atividades.query.all()
        response = [{'id':i.id, 'nome': i.nome, 'pessoa': i.pessoa.nome } for i in atividades]
        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        atividade = Atividades(nome=dados['nome'], pessoa=pessoa)

        # Salvando o novo registro no bd com o método atividade.save definida em util.py
        atividade.save()
        response = {
            'pessoa' : atividade.pessoa.nome,
            'nome' : atividade.nome,
            'id': atividade.id,
        }
        return response


# Registrando os métodos
api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(ListaAtividades, '/atividades/')

if __name__ == '__main__':
    app.run(debug=True)
