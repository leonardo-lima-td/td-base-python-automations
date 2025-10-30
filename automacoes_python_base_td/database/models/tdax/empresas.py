from sqlalchemy import Column, BigInteger, Integer, String, Text, DateTime, Date, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..base import BaseModel

class Empresas(BaseModel):
    __tablename__ = "empresas"
    schema = 'public'
    
    # id = Column(Integer, primary_key=True, autoincrement=True)
    cnpj = Column(String(18), nullable=False)
    nome = Column(String(200), nullable=False)
    vigencia_inicio = Column(Date, nullable=True)
    vigencia_fim = Column(Date, nullable=True)
    email = Column(String(254), nullable=True)
    monitorar = Column(Boolean, nullable=True)
    tem_procuracao = Column(Boolean, nullable=True)
    path_certificado_s3 = Column(String(255), nullable=True)
    obs_situacao = Column(Text, nullable=True)
    procuracao = Column(Text, nullable=True)
    atualizacao_procuracao = Column(DateTime(timezone=True), nullable=True)
    numero_telefone = Column(String(20), nullable=True)
    agencia = Column(String(100), nullable=True)
    codigo = Column(String(100), nullable=True)
    conta = Column(String(100), nullable=True)
    dv = Column(String(10), nullable=True)
    tipo_conta = Column(String(100), nullable=True)
    organizacao_id = Column(BigInteger, nullable=True)
    ultimo_monitoramento = Column(DateTime(timezone=True), nullable=True)
    date_email_notification = Column(DateTime(timezone=True), nullable=True)
    sitfis_s3_path = Column(String(255), nullable=True)
    date_sitfis_upload = Column(Date, nullable=True)
    representante_responsavel_id = Column(BigInteger, nullable=True)
    atualizacao_dte = Column(DateTime(timezone=True), nullable=True)
    status_dte = Column(String(300), nullable=True)
    status_sitfis = Column(String(255), nullable=True)
    rubrica = Column(String(35), nullable=True)
    cnae_fiscal = Column(String(10), nullable=True)
    cnae_fiscal_descricao = Column(String(500), nullable=True)
    descricao_identificador_matriz_filial = Column(String(100), nullable=True)
    estado = Column(String(100), nullable=True)
    municipio = Column(String(200), nullable=True)
    regime_tributario = Column(String(100), nullable=True)
    situacao_cadastral = Column(String(100), nullable=True)
    desativada = Column(Boolean, nullable=False)
    
    # Relationships
    privilegios = relationship("Privilegios", back_populates="empresa")