from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float

from model.base import Base


class DadosMedidos(Base):
    __tablename__ = 'tb_dados_medidos'

    id = Column(Integer, primary_key=True)
    data = Column("data_medicao", DateTime, nullable=False)
    gordura = Column("porcen_gordura", Float)
    gordura_visceral = Column("gordura_visceral", Integer)
    idade = Column("idade", Integer)
    idade_corporal = Column("idade_corporal", Integer)
    imc = Column("imc", Float)
    met_basal = Column("metabolismo_basal", Integer)
    musculo = Column("porcen_musculo", Float)
    peso = Column("peso", Float, nullable=False)
    cadastro_id = Column("dados_cadastro_id", Integer, ForeignKey('tb_dados_cadastro.id'), nullable=False)

    def __init__(self, data: DateTime, peso: float, gordura: float, gordura_visceral: int, idade: int, idade_corporal: int,
                 imc: float, met_basal: int, musculo: float, cadastro_id: int) -> None:
        self.data = datetime.now()
        self.peso = peso
        self.gordura = gordura
        self.gordura_visceral = gordura_visceral
        self.idade = idade
        self.idade_corporal = idade_corporal
        self.imc = imc
        self.met_basal = met_basal
        self.musculo = musculo
        self.cadastro_id = cadastro_id
