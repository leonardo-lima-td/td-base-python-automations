from sqlalchemy import Column, BigInteger, Integer, String, DateTime, Date, Boolean, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..base import BaseModel

class Organizacoes(BaseModel):
    __tablename__ = "organizacoes"
    schema = "public"
    
    # id = Column(BigInteger, primary_key=True, autoincrement=True)
    cnpj = Column(String(18), nullable=False)
    nome = Column(String(255), nullable=False)
    nome_arquivo = Column(String(255), nullable=True)
    valido_de = Column(Date, nullable=True)
    valido_ate = Column(Date, nullable=True)
    descricao = Column(Text, nullable=True)
    senha = Column(String(255), nullable=True)
    imported_at = Column(DateTime(timezone=True), nullable=True)
    apelido = Column(String(15), nullable=False)
    cpf_padrao = Column(String(11), nullable=True)
    path_s3_logo = Column(String(255), nullable=True)
    certificate_id = Column(Integer, ForeignKey('certificates.id', ondelete='SET NULL'), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    ativo = Column(Boolean, nullable=False)
    verbas_terceiros = Column(Text, nullable=True)
    
    # Relacionamentos
    certificate = relationship("Certificates", back_populates="organizacoes")
    users = relationship("Users", back_populates="default_organization")
