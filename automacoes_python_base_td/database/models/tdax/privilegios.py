from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from ..base import BaseModel

class Privilegios(BaseModel):
    __tablename__ = "privilegios"
    schema = 'public'
    
    # id = Column(Integer, primary_key=True, autoincrement=True)
    cnpj = Column(String(20), nullable=False)
    json_file = Column(JSON, nullable=True)
    empresa_id = Column(
        Integer,
        ForeignKey('empresas.id'),
        nullable=True
    )
    
    # Relationship
    empresa = relationship("Empresas", back_populates="privilegios")