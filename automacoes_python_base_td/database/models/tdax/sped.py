"""
SPED model.
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..base import BaseModel

class Sped(BaseModel):
    __tablename__ = 'speds'
    schema = 'public'

    # Columns
    # id = Column(Integer, primary_key=True, autoincrement=True)
    data_de_upload = Column(String, nullable=False)
    periodo = Column(String)
    tipo_de_arquivo = Column(String(255), nullable=False)
    path_s3_txt = Column(String(255), nullable=False)
    path_s3_excel = Column(String(255))
    cnpj = Column(String(255), nullable=False)
    transmitido = Column(Boolean, nullable=False)
    retificadora = Column(Boolean, nullable=False)
    num_recibo = Column(String(255))
    digito_recibo = Column(String(255))
    recibo_anterior = Column(String(255))
    importacao_id = Column(Integer)
    aguardando_validacao = Column(Boolean)
    status_validacao = Column(String(255))
    tempo_execucao_segundos = Column(Integer)
    organizacao_id = Column(Integer, ForeignKey('organizacoes.id', deferrable=True, initially='DEFERRED'))
    
    # Relationships
    organizacao = relationship("Organizacoes", foreign_keys=[organizacao_id])
    speds_retificados = relationship("SpedRetificado", back_populates="sped_origem")
    
