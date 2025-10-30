"""
SPED Retificado model.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..base import BaseModel


class SpedRetificado(BaseModel):
    __tablename__ = 'speds_retificados'
    schema = 'public'
    
    # id = Column(BigInteger, primary_key=True, autoincrement=True)
    data_retificacao = Column(String)
    periodo = Column(String)
    tipo_de_arquivo = Column(String(255), nullable=False)
    path_s3_txt = Column(String(255), nullable=False)
    path_s3_excel = Column(String(255))
    cnpj = Column(String(255))
    id_retificacao_id = Column(Integer, nullable=False, index=True)
    sped_origem_id = Column(Integer, ForeignKey('speds.id'), index=True)
    vpc_connection_link = Column(String(255))
    status_retificacao_id = Column(Integer, nullable=False, index=True)
    status_validacao = Column(String(255))
    mensagem_sqs = Column(Text)
    tempo_execucao_segundos = Column(Integer)
    usuario_retificacao_id = Column(Integer, index=True)
    data_validacao = Column(String)
    sped_size = Column(Integer)
    creditos_ressarciveis = Column(Integer)
    creditos_restituiveis = Column(Integer)
    saldo_conta_grafica = Column(Integer)
    ativo = Column(Integer, nullable=False)
    data_transmissao = Column(String)
    status_transmissao = Column(String(255))
    observacao_pva = Column(String(255))
    traceback = Column(Text)
    bloco_1000 = Column(Text)
    bloco_m = Column(Text)
    usuario_transmissao_id = Column(Integer, index=True)
    usuario_validacao_id = Column(Integer, index=True)
    path_s3_revisao = Column(String(255))
    path_s3_parquet = Column(Text)
    path_s3_excel_origem = Column(Text)
    path_s3_temp = Column(Text)

    # Relationships
    sped_origem = relationship("Sped", back_populates="speds_retificados")
