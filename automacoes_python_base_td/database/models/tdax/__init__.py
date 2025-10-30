"""
Models do banco TDAX

Adicione seus models do banco TDAX aqui.

Exemplo:
    from sqlalchemy import Column, String, Integer, Boolean, Date
    from ...base import BaseModel
    
    class Cliente(BaseModel):
        __tablename__ = "tdax_clientes"
        
        codigo = Column(String(20), unique=True, nullable=False)
        nome = Column(String(100), nullable=False)
        cpf_cnpj = Column(String(18), unique=True)
        email = Column(String(100))
        telefone = Column(String(20))
        ativo = Column(Boolean, default=True)
    
    class Produto(BaseModel):
        __tablename__ = "tdax_produtos"
        
        codigo = Column(String(20), unique=True, nullable=False)
        descricao = Column(String(200), nullable=False)
        preco = Column(Integer, nullable=False)
        estoque = Column(Integer, default=0)
        ativo = Column(Boolean, default=True)
"""

# Importe seus models do TDAX aqui
from .auto_dctf_download import DctfDownloadAll, DctfDownloadUnit
from .auto_dctf_retificacoes import DctfRetificacao
from .certificate import Certificates
from .empresas import Empresas
from .organizacoes import Organizacoes
from .privilegios import Privilegios
from .session_gov import SessionGov
from .payments import Payment
from .sped import Sped
from .speds_retificados import SpedRetificado
from .users import Users

__all__ = [
    'Certificates',
    'DctfRetificacao',
    'DctfDownloadAll',
    'DctfDownloadUnit',
    'Empresas',
    'Organizacoes',
    'Payment',
    'Privilegios',
    'SessionGov',
    'Sped',
    'SpedRetificado',
    'Users',
]
