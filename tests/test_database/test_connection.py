"""
Testes para conexões PostgreSQL
Testa funcionalidade, exceções e logs
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import psycopg2
from automacoes_python_base_td.database.connection import (
    DatabaseConnection,
    get_connection,
    execute_query,
)
from automacoes_python_base_td.core.exceptions import (
    DatabaseConnectionError,
    DatabaseQueryError,
)


class TestDatabaseConnection:
    """Testes para classe DatabaseConnection"""
    
    def test_init_with_params(self):
        """Testa inicialização com parâmetros"""
        db = DatabaseConnection(
            host="testhost",
            port=5433,
            database="testdb",
            user="testuser",
            password="testpass"
        )
        
        assert db.host == "testhost"
        assert db.port == 5433
        assert db.database == "testdb"
        assert db.user == "testuser"
        assert db.password == "testpass"
    
    @patch('psycopg2.connect')
    def test_connect_success(self, mock_connect):
        """Testa conexão bem-sucedida"""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        db = DatabaseConnection(
            host="localhost",
            database="testdb",
            user="testuser",
            password="testpass"
        )
        
        conn = db.connect()
        
        assert conn == mock_conn
        mock_connect.assert_called_once()
    
    @patch('psycopg2.connect')
    def test_connect_failure_raises_exception(self, mock_connect, caplog):
        """Testa se conexão com falha lança DatabaseConnectionError"""
        import logging
        caplog.set_level(logging.ERROR)
        
        # Simula erro de conexão
        mock_connect.side_effect = psycopg2.OperationalError("Connection refused")
        
        db = DatabaseConnection(
            host="localhost",
            database="testdb",
            user="testuser",
            password="testpass"
        )
        
        # Verifica se lança a exceção correta
        with pytest.raises(DatabaseConnectionError) as exc_info:
            db.connect()
        
        # Verifica detalhes da exceção
        exc = exc_info.value
        assert exc.code == "DB_CONNECTION"
        assert "host" in exc.details
        assert exc.details["host"] == "localhost"
        
        # Verifica se log foi emitido
        assert any("DatabaseConnectionError" in record.message for record in caplog.records)
    
    @patch('psycopg2.connect')
    def test_close_connection(self, mock_connect):
        """Testa fechamento de conexão"""
        mock_conn = MagicMock()
        mock_conn.closed = False
        mock_connect.return_value = mock_conn
        
        db = DatabaseConnection()
        db.connect()
        db.close()
        
        mock_conn.close.assert_called_once()


class TestGetConnection:
    """Testes para context manager get_connection"""
    
    @patch('psycopg2.connect')
    def test_get_connection_success(self, mock_connect):
        """Testa get_connection com sucesso"""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        with get_connection(host="localhost") as conn:
            assert conn == mock_conn
        
        # Verifica se commit foi chamado
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
    
    @patch('psycopg2.connect')
    def test_get_connection_rollback_on_error(self, mock_connect, caplog):
        """Testa se rollback é chamado em caso de erro"""
        import logging
        caplog.set_level(logging.ERROR)
        
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        with pytest.raises(DatabaseQueryError):
            with get_connection() as conn:
                # Simula erro psycopg2
                raise psycopg2.Error("Query failed")
        
        # Verifica se rollback foi chamado
        mock_conn.rollback.assert_called_once()
        
        # Verifica log
        assert any("DatabaseQueryError" in record.message for record in caplog.records)


class TestExecuteQuery:
    """Testes para função execute_query"""
    
    @patch('automacoes_python_base_td.database.connection.get_connection')
    def test_execute_query_success(self, mock_get_connection):
        """Testa execução de query com sucesso"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_conn.cursor.return_value.__enter__ = Mock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = Mock(return_value=False)
        
        mock_get_connection.return_value.__enter__ = Mock(return_value=mock_conn)
        mock_get_connection.return_value.__exit__ = Mock(return_value=False)
        
        result = execute_query("INSERT INTO users VALUES (%s)", ("test",))
        
        assert result == 1
        mock_cursor.execute.assert_called_once()
    
    @patch('automacoes_python_base_td.database.connection.get_connection')
    def test_execute_query_failure_raises_exception(self, mock_get_connection, caplog):
        """Testa se erro na query lança DatabaseQueryError"""
        import logging
        caplog.set_level(logging.ERROR)
        
        # Simula erro na query
        mock_get_connection.side_effect = Exception("Query error")
        
        with pytest.raises(DatabaseQueryError) as exc_info:
            execute_query("SELECT * FROM invalid_table")
        
        exc = exc_info.value
        assert exc.code == "DB_QUERY"
        
        # Verifica log
        assert any("DatabaseQueryError" in record.message for record in caplog.records)

