"""
Testes para CRUD genérico
"""
import pytest
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from automacoes_python_base_td.database import Base, BaseModel, CRUDBase


# Model de teste
class TestProduct(BaseModel):
    __tablename__ = "test_products"
    
    name = Column(String(100))
    price = Column(Integer)
    stock = Column(Integer, default=0)


@pytest.fixture
def db_session():
    """Fixture para sessão de banco de dados em memória"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


class TestCRUDBase:
    """Testes para CRUDBase"""
    
    def test_create(self, db_session):
        """Testa criação de registro"""
        crud = CRUDBase(TestProduct)
        
        product = crud.create(db_session, {
            "name": "Test Product",
            "price": 100,
            "stock": 10
        })
        
        assert product.id is not None
        assert product.name == "Test Product"
        assert product.price == 100
    
    def test_get(self, db_session):
        """Testa busca por ID"""
        crud = CRUDBase(TestProduct)
        
        # Criar
        product = crud.create(db_session, {
            "name": "Test Product",
            "price": 100
        })
        
        # Buscar
        found = crud.get(db_session, product.id)
        assert found is not None
        assert found.id == product.id
    
    def test_get_all(self, db_session):
        """Testa busca de todos os registros"""
        crud = CRUDBase(TestProduct)
        
        # Criar vários
        for i in range(5):
            crud.create(db_session, {
                "name": f"Product {i}",
                "price": i * 100
            })
        
        # Buscar todos
        products = crud.get_all(db_session)
        assert len(products) == 5
    
    def test_update(self, db_session):
        """Testa atualização de registro"""
        crud = CRUDBase(TestProduct)
        
        # Criar
        product = crud.create(db_session, {
            "name": "Test Product",
            "price": 100
        })
        
        # Atualizar
        updated = crud.update(db_session, product.id, {
            "price": 200
        })
        
        assert updated.price == 200
        assert updated.name == "Test Product"
    
    def test_delete(self, db_session):
        """Testa deleção de registro"""
        crud = CRUDBase(TestProduct)
        
        # Criar
        product = crud.create(db_session, {
            "name": "Test Product",
            "price": 100
        })
        
        # Deletar
        result = crud.delete(db_session, product.id)
        assert result is True
        
        # Verificar se foi deletado
        found = crud.get(db_session, product.id)
        assert found is None
    
    def test_filter(self, db_session):
        """Testa filtro de registros"""
        crud = CRUDBase(TestProduct)
        
        # Criar vários
        crud.create(db_session, {"name": "Product A", "price": 100})
        crud.create(db_session, {"name": "Product B", "price": 200})
        crud.create(db_session, {"name": "Product C", "price": 100})
        
        # Filtrar
        products = crud.filter(db_session, price=100)
        assert len(products) == 2
    
    def test_count(self, db_session):
        """Testa contagem de registros"""
        crud = CRUDBase(TestProduct)
        
        # Criar vários
        for i in range(3):
            crud.create(db_session, {
                "name": f"Product {i}",
                "price": 100
            })
        
        # Contar
        count = crud.count(db_session)
        assert count == 3
    
    def test_exists(self, db_session):
        """Testa verificação de existência"""
        crud = CRUDBase(TestProduct)
        
        # Criar
        product = crud.create(db_session, {
            "name": "Test Product",
            "price": 100
        })
        
        # Verificar
        assert crud.exists(db_session, product.id) is True
        assert crud.exists(db_session, 9999) is False

