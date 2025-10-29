"""
Testes para CRUD genérico
Testa funcionalidade, exceções e logs
"""
import pytest
from unittest.mock import MagicMock, Mock
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.exc import SQLAlchemyError
from automacoes_python_base_td.database.models.base import Base
from automacoes_python_base_td.database.repositories.crud import CRUDBase, crud_factory
from automacoes_python_base_td.core.exceptions import (
    DatabaseQueryError,
    ModelNotFoundError,
)


# Model de teste
class TestUser(Base):
    """Model de teste para CRUD"""
    __tablename__ = "test_users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    ativo = Column(Boolean, default=True)


class TestCRUDBase:
    """Testes para classe CRUDBase"""
    
    def test_crud_factory(self):
        """Testa criação de CRUD via factory"""
        crud = crud_factory(TestUser)
        
        assert isinstance(crud, CRUDBase)
        assert crud.model == TestUser
    
    def test_get_active_only(self):
        """Testa get retorna apenas ativos por padrão"""
        mock_session = MagicMock()
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        
        user = TestUser(id=1, name="Test", ativo=True)
        mock_query.first.return_value = user
        
        crud = CRUDBase(TestUser)
        result = crud.get(mock_session, 1)
        
        # Verifica que filtrou por ativo=True
        assert mock_query.filter.called
        assert result == user
    
    def test_get_include_inactive(self):
        """Testa get com include_inactive=True"""
        mock_session = MagicMock()
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        
        user = TestUser(id=1, name="Test", ativo=False)
        mock_query.first.return_value = user
        
        crud = CRUDBase(TestUser)
        result = crud.get(mock_session, 1, include_inactive=True)
        
        assert result == user
    
    def test_create_success(self):
        """Testa criação de registro"""
        mock_session = MagicMock()
        
        crud = CRUDBase(TestUser)
        data = {"name": "John", "email": "john@test.com"}
        
        result = crud.create(mock_session, data)
        
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()
    
    def test_create_failure_raises_exception(self, loguru_caplog):
        """Testa se erro ao criar lança DatabaseQueryError"""
        import logging
        loguru_caplog.set_level(logging.ERROR)
        
        mock_session = MagicMock()
        # Simula erro SQLAlchemy
        mock_session.commit.side_effect = SQLAlchemyError("Constraint violation")
        
        crud = CRUDBase(TestUser)
        data = {"name": "John"}
        
        with pytest.raises(DatabaseQueryError) as exc_info:
            crud.create(mock_session, data)
        
        # Verifica rollback foi chamado
        mock_session.rollback.assert_called_once()
        
        # Verifica exceção
        exc = exc_info.value
        assert exc.code == "DB_QUERY"
        assert "TestUser" in exc.message
        
        # Verifica log
        assert any("DatabaseQueryError" in record.message for record in loguru_caplog.records)
    
    def test_update_success(self):
        """Testa atualização de registro"""
        mock_session = MagicMock()
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        
        user = TestUser(id=1, name="Old Name", ativo=True)
        mock_query.first.return_value = user
        
        crud = CRUDBase(TestUser)
        result = crud.update(mock_session, 1, {"name": "New Name"})
        
        mock_session.commit.assert_called_once()
        assert result.name == "New Name"
    
    def test_update_not_found_raises_exception(self, loguru_caplog):
        """Testa se update de registro inexistente lança ModelNotFoundError"""
        import logging
        loguru_caplog.set_level(logging.ERROR)
        
        mock_session = MagicMock()
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None  # Não encontrou
        
        crud = CRUDBase(TestUser)
        
        with pytest.raises(ModelNotFoundError) as exc_info:
            crud.update(mock_session, 999, {"name": "New Name"})
        
        exc = exc_info.value
        assert exc.code == "MODEL_NOT_FOUND"
        assert exc.details["id"] == 999
        
        # Verifica log
        assert any("ModelNotFoundError" in record.message for record in loguru_caplog.records)
    
    def test_delete_soft_delete(self, loguru_caplog):
        """Testa soft delete (marca ativo=False)"""
        import logging
        loguru_caplog.set_level(logging.ERROR)
        
        mock_session = MagicMock()
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        
        user = TestUser(id=1, name="Test", ativo=True)
        mock_query.first.return_value = user
        
        crud = CRUDBase(TestUser)
        result = crud.delete(mock_session, 1)
        
        assert result is True
        assert user.ativo is False
        mock_session.commit.assert_called_once()
    
    def test_delete_not_found_raises_exception(self, loguru_caplog):
        """Testa se delete de registro inexistente lança ModelNotFoundError"""
        import logging
        loguru_caplog.set_level(logging.ERROR)
        
        mock_session = MagicMock()
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        
        crud = CRUDBase(TestUser)
        
        with pytest.raises(ModelNotFoundError) as exc_info:
            crud.delete(mock_session, 999)
        
        exc = exc_info.value
        assert exc.code == "MODEL_NOT_FOUND"
        
        # Verifica log
        assert any("ModelNotFoundError" in record.message for record in loguru_caplog.records)
    
    def test_count_active_only(self):
        """Testa count retorna apenas ativos por padrão"""
        mock_session = MagicMock()
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.count.return_value = 5
        
        crud = CRUDBase(TestUser)
        result = crud.count(mock_session)
        
        assert result == 5
        assert mock_query.filter.called
    
    def test_exists_active_only(self):
        """Testa exists retorna apenas ativos por padrão"""
        mock_session = MagicMock()
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = TestUser(id=1, ativo=True)
        
        crud = CRUDBase(TestUser)
        result = crud.exists(mock_session, 1)
        
        assert result is True

