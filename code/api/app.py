from datetime import date

from flask import jsonify, request, redirect
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_openapi3 import OpenAPI, Info, Tag
from marshmallow import fields, INCLUDE
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from config import engine
from model.base import Base
from model.dados_cadastro import DadosCadastro
from model.dados_medidos import DadosMedidos

info = Info(title="API de dados para acompanhamento de composição corporal", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app, resources={r"/*": {"origins": "*"}})

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

ma = Marshmallow(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
cadastro_tag = Tag(name="Dados Cadastrais", description="Visualização de usuários")
dados_tag = Tag(name="Dados Medidos", description="Adição, Visualização e Remoção de dados medidos na balança")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


class DadosCadastroSchema(ma.SQLAlchemyAutoSchema):
    """
    Define como os dados cadastrais do usuário inserido deve ser representado
    """
    dados_medidos = fields.Nested('DadosMedidosSchema', many=True, include_relationships=True)

    class Meta:
        model = DadosCadastro
        include_fk = True
        load_instance = True
        include_relationships = True
        include_schema = True


class DadosMedidosSchema(ma.SQLAlchemyAutoSchema):
    """
        Define como os dados medidos na balança inseridos devem ser representado
    """
    class Meta:
        model = DadosMedidos
        include_fk = True
        load_instance = True


def calcular_idade(data_nascimento):
    hoje = date.today()
    return hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))


def calcular_imc(altura, peso):
    imc = peso / altura ** 2
    return round(imc,2)


@app.get('/cadastro', methods=['GET'], tags=[cadastro_tag])
def get_dados_cadastro():
    """
    Essa rota permite consultar informações de usuários cadastrados através de um ID. Se nenhum ID for informado,
    retorna todos os usuários cadastrados.
    Retorna um JSON com os dados cadastrais do usuário ou uma mensagem de erro 404 se nenhum usuário for encontrado.
    """
    session = Session()
    id = request.args.get('id')
    if id:
        dados_cadastrais = session.query(DadosCadastro).filter_by(id=id).all()
    else:
        dados_cadastrais = session.query(DadosCadastro).all()

    dados_cadastrais_serialized = DadosCadastroSchema(many=True).dump(dados_cadastrais)

    session.close()

    return jsonify(dados_cadastrais_serialized)


@app.get('/dados', methods=['GET'], tags=[dados_tag])
def get_dados_medidos():
    """
    Essa rota retorna os dados medidos pela balança, podendo ser filtrados por ID de cadastro e
    ordenados por data em ordem ascendente ou descendente

    """

    session = Session()
    cadastro_id = request.args.get('id')
    order = request.args.get('order')

    if cadastro_id is None:
        dados_medidos = session.query(DadosMedidos)
    else:
        dados_medidos = session.query(DadosMedidos).filter_by(cadastro_id=cadastro_id)

    if order == 'asc':
        dados_medidos = dados_medidos.order_by(DadosMedidos.data.asc())
    elif order == 'desc':
        dados_medidos = dados_medidos.order_by(DadosMedidos.data.desc())

    dados_medidos = dados_medidos.all()
    dados_medidos_serialized = DadosMedidosSchema(many=True).dump(dados_medidos)
    session.close()

    return jsonify(dados_medidos_serialized)


@app.post('/dados', methods=['POST'], tags=[dados_tag])
def cadastrar_dados_medidos():
    """
        Essa rota salva os dados medidos pela balança relacionando com a tabela de usuário pelo cadastro_id

    """

    session = Session()
    dados_medidos_serializer = DadosMedidosSchema()
    dados_medidos_dict = request.json
    dados_cadastro_id = dados_medidos_dict['cadastro_id']
    dados_cadastro = session.query(DadosCadastro).get(dados_cadastro_id)
    if not dados_cadastro:
        return jsonify({'mensagem': 'Cadastro não encontrado.'}), 400
    dados_medidos_dict['idade'] = calcular_idade(dados_cadastro.nascimento)
    peso_float = float(dados_medidos_dict['peso'])
    altura_metro = dados_cadastro.altura / 100
    dados_medidos_dict['imc'] = calcular_imc(altura_metro, peso_float)
    dados_medidos = dados_medidos_serializer.load(dados_medidos_dict, unknown=INCLUDE)
    session.add(dados_medidos)
    try:
        session.commit()
        session.refresh(dados_medidos)
        session.close()
        return jsonify(dados_medidos_serializer.dump(dados_medidos)), 201
    except IntegrityError as e:
        session.rollback()
        session.close()
        return jsonify({'mensagem': 'Erro ao cadastrar dados medidos.'}), 400


@app.delete('/dados/', methods=['DELETE'], tags=[dados_tag])
def deletar_dados_medidos():
    """
            Essa rota apaga os dados medidos pela balança buscando pelo id
    """

    id = request.args.get('id')
    session = Session()
    dados_medidos = session.query(DadosMedidos).get(id)
    if not dados_medidos:
        session.close()
        return jsonify({'mensagem': 'Registro não encontrado.'}), 404
    session.delete(dados_medidos)
    session.commit()
    session.close()
    return jsonify({'mensagem': 'Registro deletado com sucesso.'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
