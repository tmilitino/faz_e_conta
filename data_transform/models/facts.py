from connection import connection
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import AbstractConcreteBase

Base = connection.get_base()

class ModelBase(AbstractConcreteBase, Base):
    id             = Column(Integer, primary_key=True)
    ano            = Column(String)
    cod_legislacao = Column(String)


class FatTotalGastosParlamentar(ModelBase):
    __tablename__ = "fat_total_gastos_parlamentar"

    nome          = Column(String(255))
    sg_uf         = Column(String(4))
    sg_partido    = Column(String)
    valor_liquido = Column(Float)
    
# FatTotalGastosParlamentar.__table__.drop(connection.get_engine())

class FatDistribuicaoPartido(ModelBase):
    __tablename__ = "fat_distribuicao_partido"
    
    sg_partido        = Column(String)
    valor_liquido     = Column(Float)
    total_parlamentar = Column(Integer)

class FatRankingPartido(ModelBase):
    __tablename__ = "fat_ranking_partido"
    
    sg_partido    = Column(String)
    valor_medio   = Column(Float)
    valor_liquido = Column(Float)

class FatTimeSeiresCandidato(ModelBase):
    __tablename__ = "fat_time_seires_candidato"

    nome          = Column(String(255))
    mes_ano       = Column(String)
    valor_liquido = Column(Float)

class FatDespesaPartido(ModelBase):
    __tablename__ = "fat_despesa_partido"

    sg_partido        = Column(String(255))
    descricao_despesa = Column(String)
    valor_liquido     = Column(Float)

class migrate():
    def __init__(self):
        connection.create_tables(Base)
