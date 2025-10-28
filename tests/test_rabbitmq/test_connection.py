"""
Testes para conexão RabbitMQ
Testa funcionalidade, exceções e logs
"""
import pytest
from unittest.mock import patch, MagicMock
from pika.exceptions import AMQPConnectionError
from automacoes_python_base_td.rabbitmq.connection import RabbitMQConnection
from automacoes_python_base_td.core.exceptions import RabbitMQConnectionError


class TestRabbitMQConnection:
    """Testes para RabbitMQConnection"""
    
    def test_init_with_params(self):
        """Testa inicialização com parâmetros"""
        conn = RabbitMQConnection(
            host="testhost",
            port=5673,
            username="testuser",
            password="testpass",
            virtual_host="/test"
        )
        
        assert conn.host == "testhost"
        assert conn.port == 5673
        assert conn.username == "testuser"
        assert conn.password == "testpass"
        assert conn.virtual_host == "/test"
    
    @patch('pika.BlockingConnection')
    def test_connect_success(self, mock_blocking_connection):
        """Testa conexão bem-sucedida"""
        mock_connection = MagicMock()
        mock_channel = MagicMock()
        mock_connection.channel.return_value = mock_channel
        mock_blocking_connection.return_value = mock_connection
        
        conn = RabbitMQConnection(
            host="localhost",
            username="guest",
            password="guest"
        )
        
        result = conn.connect()
        
        assert result is True
        assert conn.connection == mock_connection
        assert conn.channel == mock_channel
    
    @patch('pika.BlockingConnection')
    def test_connect_failure_raises_exception(self, mock_blocking_connection, caplog):
        """Testa se falha na conexão lança RabbitMQConnectionError"""
        import logging
        caplog.set_level(logging.ERROR)
        
        # Simula erro de conexão
        mock_blocking_connection.side_effect = AMQPConnectionError("Connection refused")
        
        conn = RabbitMQConnection(
            host="localhost",
            username="guest",
            password="guest"
        )
        
        with pytest.raises(RabbitMQConnectionError) as exc_info:
            conn.connect()
        
        # Verifica exceção
        exc = exc_info.value
        assert exc.code == "RABBITMQ_CONNECTION"
        assert "host" in exc.details
        assert exc.details["host"] == "localhost"
        
        # Verifica log
        assert any("RabbitMQConnectionError" in record.message for record in caplog.records)
    
    @patch('pika.BlockingConnection')
    def test_close_connection(self, mock_blocking_connection):
        """Testa fechamento de conexão"""
        mock_connection = MagicMock()
        mock_connection.is_closed = False
        mock_channel = MagicMock()
        mock_connection.channel.return_value = mock_channel
        mock_blocking_connection.return_value = mock_connection
        
        conn = RabbitMQConnection()
        conn.connect()
        conn.close()
        
        mock_connection.close.assert_called_once()

