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
# from .cliente import Cliente
# from .produto import Produto
# from .pedido import Pedido

__all__ = []

