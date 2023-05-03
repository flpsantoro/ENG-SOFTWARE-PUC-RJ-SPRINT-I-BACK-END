from datetime import date
from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from model.base import Base
from model.dados_medidos import DadosMedidos


class DadosCadastro(Base):
    __tablename__ = 'tb_dados_cadastro'

    id = Column(Integer, primary_key=True)
    nome = Column(String(255))
    sobrenome = Column(String(255))
    nascimento = Column(Date)
    altura = Column(Integer)
    email = Column(String(255))
    dados_medidos = relationship('DadosMedidos', backref='tb_dados_cadastro')

    def __init__(self, nome: str, sobrenome: str,  nascimento: date, altura: int,
                 email: str) -> None:
        self.nome = nome
        self.sobrenome = sobrenome
        self.nascimento = nascimento
        self.altura = altura
        self.email = email
