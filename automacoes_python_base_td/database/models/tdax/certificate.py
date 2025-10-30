from sqlalchemy import Column, Integer, BigInteger, String, Date, DateTime, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from ..base import BaseModel


class Certificates(BaseModel):
    __tablename__ = "certificates"
    schema = "public"
    
    # id = Column(Integer, primary_key=True, autoincrement=True)
    cnpj = Column(String(18), nullable=False)
    name = Column(String(255), nullable=False)
    file_name = Column(String(255), nullable=False)
    valid_start_date = Column(Date, nullable=False)
    valid_end_date = Column(Date, nullable=False)
    description = Column(Text, nullable=True)
    password = Column(String(255), nullable=False)
    imported_at = Column(DateTime(timezone=True), nullable=False)
    responsible_id = Column(BigInteger, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    certificado_serpro = Column(Text, nullable=True)
    xml_atualizado = Column(DateTime(timezone=True), nullable=True)
    xml_validade = Column(DateTime(timezone=True), nullable=True)
    
    # Relacionamentos
    responsible = relationship("Users", back_populates="certificates")
    organizacoes = relationship("Organizacoes", back_populates="certificate")


