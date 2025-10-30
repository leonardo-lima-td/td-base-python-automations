"""
EXEMPLO 3: SQLAlchemy ORM
==========================

Como usar SQLAlchemy com models e CRUD operations.
Recomendado para projetos novos e manutenção fácil.

PRÉ-REQUISITOS:
- Pacote instalado: pip install automacoes-python-base-td
- Database configurado no .env
"""

from automacoes_python_base_td.database import (
    BaseModel,
    get_session,
    CRUDBase
)
from automacoes_python_base_td.logger import get_logger
from sqlalchemy import Column, String, Float, Integer

logger = get_logger()

# ====================================================================
# 1. DEFINIR SEU MODEL
# ====================================================================

class Product(BaseModel):
    """
    Seu model de produto.
    Herda de BaseModel para ter: id, created_at, updated_at, ativo
    """
    __tablename__ = "products"
    
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    category = Column(String(50))


# ====================================================================
# 2. USAR CRUD PRONTO
# ====================================================================

def exemplo_crud_completo():
    """Exemplo de todas operações CRUD"""
    
    # Criar instância do CRUD
    product_crud = CRUDBase(Product)
    
    # Usar sessão do banco (tdax ou automations)
    with get_session("tdax") as session:
        
        # CREATE - Criar novo produto
        logger.info("Criando produto...")
        novo_produto = product_crud.create(session, {
            "name": "Notebook Dell Inspiron 15",
            "price": 3500.00,
            "stock": 10,
            "category": "Informática"
        })
        logger.info(f"✅ Produto criado: ID {novo_produto.id}")
        
        # READ - Buscar por ID
        logger.info(f"Buscando produto {novo_produto.id}...")
        produto = product_crud.get(session, novo_produto.id)
        logger.info(f"📦 {produto.name} - R$ {produto.price:.2f}")
        
        # UPDATE - Atualizar
        logger.info("Atualizando estoque...")
        atualizado = product_crud.update(session, produto.id, {
            "stock": 8  # Vendeu 2 unidades
        })
        logger.info(f"✏️  Novo estoque: {atualizado.stock}")
        
        # LIST - Listar todos ativos
        logger.info("Listando produtos...")
        produtos = product_crud.get_all(session, limit=10)
        logger.info(f"📋 Total: {len(produtos)} produto(s)")
        
        # DELETE - Soft delete (marca ativo=False)
        logger.info("Deletando produto (soft delete)...")
        product_crud.delete(session, produto.id)
        logger.info("🗑️  Produto marcado como inativo")
        
        # Verificar se existe (não encontra inativos por padrão)
        existe = product_crud.exists(session, produto.id)
        logger.info(f"Produto ainda existe? {existe}")  # False


# ====================================================================
# 3. MÚLTIPLOS BANCOS
# ====================================================================

def exemplo_multiplos_bancos():
    """Como trabalhar com múltiplos bancos"""
    product_crud = CRUDBase(Product)
    
    # Banco TDAX
    with get_session("tdax") as session:
        produtos_tdax = product_crud.get_all(session)
        logger.info(f"TDAX: {len(produtos_tdax)} produto(s)")
    
    # Banco Automations
    with get_session("automations") as session:
        produtos_auto = product_crud.get_all(session)
        logger.info(f"Automations: {len(produtos_auto)} produto(s)")


# ====================================================================
# EXECUTAR EXEMPLOS
# ====================================================================

if __name__ == "__main__":
    logger.info("=== Exemplo SQLAlchemy ORM ===")
    
    # Descomente para testar:
    # exemplo_crud_completo()
    # exemplo_multiplos_bancos()
    
    logger.info("✅ Exemplos concluídos!")
