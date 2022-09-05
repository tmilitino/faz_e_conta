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

    sg_uf          = Column(String(4))
    sg_partido     = Column(String)
    nome           = Column(String(255))
    valor_liquido  = Column(Float)
    
# FatTotalGastosParlamentar.__table__.drop(connection.get_engine())

class FatDistribuicaoPartido(ModelBase):
    __tablename__ = "fat_distribuicao_partido"
    
    sg_partido        = Column(String)
    valor_liquido     = Column(Float)
    total_parlamentar = Column(Integer)

class FatRankingPartido(ModelBase):
    __tablename__ = "fat_ranking_partido"
    
    sg_partido    = Column(String)
    valor_liquido = Column(Float)
    valor_medio   = Column(Float)

class migrate():
    def __init__(self):
        connection.create_tables(Base)
