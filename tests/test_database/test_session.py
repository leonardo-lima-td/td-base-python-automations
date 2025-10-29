"""
Testes para Session Manager Unificado
Testa funcionalidade do DatabaseSessionManager e funções auxiliares
"""
import pytest
from unittest.mock import MagicMock, patch, Mock
from automacoes_python_base_td.database.session import (
    DatabaseType,
    DatabaseSessionManager,
    get_manager,
    get_session,
    get_tdax_session,
    get_automations_session,
    get_tdax_manager,
    get_automations_manager,
)


class TestDatabaseSessionManager:
    """Testes para DatabaseSessionManager unificado"""
    
    def test_create_manager_with_db_type_tdax(self, monkeypatch):
        """Testa criação de manager com db_type='tdax'"""
        monkeypatch.setenv("DATABASE_URL_TDAX", "postgresql://test:test@localhost/tdax")
        
        with patch('automacoes_python_base_td.database.session.create_engine') as mock_engine:
            with patch('automacoes_python_base_td.database.session.sessionmaker') as mock_sessionmaker:
                manager = DatabaseSessionManager(db_type="tdax")
                
                assert manager.db_type == "tdax"
                assert mock_engine.called
                assert mock_sessionmaker.called
    
    def test_create_manager_with_db_type_automations(self, monkeypatch):
        """Testa criação de manager com db_type='automations'"""
        monkeypatch.setenv("DATABASE_URL_AUTOMATION", "postgresql://test:test@localhost/automacoes")
        
        with patch('automacoes_python_base_td.database.session.create_engine') as mock_engine:
            with patch('automacoes_python_base_td.database.session.sessionmaker') as mock_sessionmaker:
                manager = DatabaseSessionManager(db_type="automations")
                
                assert manager.db_type == "automations"
                assert mock_engine.called
    
    def test_create_manager_with_custom_url(self):
        """Testa criação de manager com URL customizada"""
        custom_url = "postgresql://custom:pass@custom-host/custom-db"
        
        with patch('automacoes_python_base_td.database.session.create_engine') as mock_engine:
            with patch('automacoes_python_base_td.database.session.sessionmaker'):
                manager = DatabaseSessionManager(database_url=custom_url)
                
                # Deve usar a URL fornecida
                mock_engine.assert_called_once()
                call_args = mock_engine.call_args
                assert call_args[0][0] == custom_url
    
    def test_get_session_returns_session(self):
        """Testa se get_session retorna uma sessão"""
        with patch('automacoes_python_base_td.database.session.create_engine'):
            with patch('automacoes_python_base_td.database.session.sessionmaker') as mock_sessionmaker:
                mock_session_class = MagicMock()
                mock_sessionmaker.return_value = mock_session_class
                
                manager = DatabaseSessionManager(database_url="postgresql://test/test")
                session = manager.get_session()
                
                mock_session_class.assert_called_once()
    
    def test_session_scope_commits_on_success(self):
        """Testa se session_scope faz commit em caso de sucesso"""
        with patch('automacoes_python_base_td.database.session.create_engine'):
            with patch('automacoes_python_base_td.database.session.sessionmaker') as mock_sessionmaker:
                mock_session = MagicMock()
                mock_session_class = MagicMock(return_value=mock_session)
                mock_sessionmaker.return_value = mock_session_class
                
                manager = DatabaseSessionManager(database_url="postgresql://test/test")
                
                with manager.session_scope() as session:
                    pass  # Operação bem-sucedida
                
                mock_session.commit.assert_called_once()
                mock_session.close.assert_called_once()
    
    def test_session_scope_rollback_on_error(self):
        """Testa se session_scope faz rollback em caso de erro"""
        with patch('automacoes_python_base_td.database.session.create_engine'):
            with patch('automacoes_python_base_td.database.session.sessionmaker') as mock_sessionmaker:
                mock_session = MagicMock()
                mock_session_class = MagicMock(return_value=mock_session)
                mock_sessionmaker.return_value = mock_session_class
                
                manager = DatabaseSessionManager(database_url="postgresql://test/test")
                
                with pytest.raises(ValueError):
                    with manager.session_scope() as session:
                        raise ValueError("Test error")
                
                mock_session.rollback.assert_called_once()
                mock_session.close.assert_called_once()


class TestGetManager:
    """Testes para função get_manager"""
    
    def test_get_manager_creates_and_caches(self, monkeypatch):
        """Testa se get_manager cria e cacheia managers"""
        monkeypatch.setenv("DATABASE_URL_TDAX", "postgresql://test/tdax")
        
        # Limpar cache
        from automacoes_python_base_td.database import session
        session._managers.clear()
        
        with patch('automacoes_python_base_td.database.session.create_engine'):
            with patch('automacoes_python_base_td.database.session.sessionmaker'):
                manager1 = get_manager("tdax")
                manager2 = get_manager("tdax")
                
                # Deve retornar a mesma instância (cache)
                assert manager1 is manager2
    
    def test_get_manager_different_types(self, monkeypatch):
        """Testa se get_manager cria managers diferentes para tipos diferentes"""
        monkeypatch.setenv("DATABASE_URL_TDAX", "postgresql://test/tdax")
        monkeypatch.setenv("DATABASE_URL_AUTOMATION", "postgresql://test/automacoes")
        
        # Limpar cache
        from automacoes_python_base_td.database import session
        session._managers.clear()
        
        with patch('automacoes_python_base_td.database.session.create_engine'):
            with patch('automacoes_python_base_td.database.session.sessionmaker'):
                manager_tdax = get_manager("tdax")
                manager_auto = get_manager("automations")
                
                # Deve ser instâncias diferentes
                assert manager_tdax is not manager_auto


class TestGetSession:
    """Testes para função get_session"""
    
    def test_get_session_yields_session(self, monkeypatch):
        """Testa se get_session retorna uma sessão"""
        monkeypatch.setenv("DATABASE_URL_TDAX", "postgresql://test/tdax")
        
        # Limpar cache
        from automacoes_python_base_td.database import session
        session._managers.clear()
        
        with patch('automacoes_python_base_td.database.session.create_engine'):
            with patch('automacoes_python_base_td.database.session.sessionmaker') as mock_sessionmaker:
                mock_session = MagicMock()
                mock_session_class = MagicMock(return_value=mock_session)
                mock_sessionmaker.return_value = mock_session_class
                
                with get_session("tdax") as session:
                    assert session is not None
                
                mock_session.commit.assert_called_once()
                mock_session.close.assert_called_once()


class TestAliases:
    """Testes para funções alias (compatibilidade)"""
    
    def test_get_tdax_session_alias(self, monkeypatch):
        """Testa se get_tdax_session funciona como alias"""
        monkeypatch.setenv("DATABASE_URL_TDAX", "postgresql://test/tdax")
        
        # Limpar cache
        from automacoes_python_base_td.database import session
        session._managers.clear()
        
        with patch('automacoes_python_base_td.database.session.create_engine'):
            with patch('automacoes_python_base_td.database.session.sessionmaker') as mock_sessionmaker:
                mock_session = MagicMock()
                mock_session_class = MagicMock(return_value=mock_session)
                mock_sessionmaker.return_value = mock_session_class
                
                with get_tdax_session() as session:
                    assert session is not None
    
    def test_get_automations_session_alias(self, monkeypatch):
        """Testa se get_automations_session funciona como alias"""
        monkeypatch.setenv("DATABASE_URL_AUTOMATION", "postgresql://test/automacoes")
        
        # Limpar cache
        from automacoes_python_base_td.database import session
        session._managers.clear()
        
        with patch('automacoes_python_base_td.database.session.create_engine'):
            with patch('automacoes_python_base_td.database.session.sessionmaker') as mock_sessionmaker:
                mock_session = MagicMock()
                mock_session_class = MagicMock(return_value=mock_session)
                mock_sessionmaker.return_value = mock_session_class
                
                with get_automations_session() as session:
                    assert session is not None
    
    def test_get_tdax_manager_alias(self, monkeypatch):
        """Testa se get_tdax_manager funciona como alias"""
        monkeypatch.setenv("DATABASE_URL_TDAX", "postgresql://test/tdax")
        
        # Limpar cache
        from automacoes_python_base_td.database import session
        session._managers.clear()
        
        with patch('automacoes_python_base_td.database.session.create_engine'):
            with patch('automacoes_python_base_td.database.session.sessionmaker'):
                manager = get_tdax_manager()
                assert manager is not None
                assert manager.db_type == "tdax"
    
    def test_get_automations_manager_alias(self, monkeypatch):
        """Testa se get_automations_manager funciona como alias"""
        monkeypatch.setenv("DATABASE_URL_AUTOMATION", "postgresql://test/automacoes")
        
        # Limpar cache
        from automacoes_python_base_td.database import session
        session._managers.clear()
        
        with patch('automacoes_python_base_td.database.session.create_engine'):
            with patch('automacoes_python_base_td.database.session.sessionmaker'):
                manager = get_automations_manager()
                assert manager is not None
                assert manager.db_type == "automations"


class TestDatabaseType:
    """Testes para o tipo DatabaseType"""
    
    def test_database_type_literal(self):
        """Testa se DatabaseType aceita valores corretos"""
        from typing import get_args
        
        # Verifica os valores permitidos
        allowed_values = get_args(DatabaseType)
        assert "tdax" in allowed_values
        assert "automations" in allowed_values

