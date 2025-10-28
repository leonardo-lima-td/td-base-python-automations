"""
Configurações compartilhadas para todos os testes
"""
import pytest
from unittest.mock import Mock, MagicMock
import psycopg2
import pika


# Fixtures para captura de logs
@pytest.fixture
def capture_logs(caplog):
    """Fixture para capturar logs durante os testes"""
    import logging
    caplog.set_level(logging.ERROR)
    return caplog


# Fixtures para mock de banco de dados
@pytest.fixture
def mock_db_connection():
    """Mock de conexão PostgreSQL"""
    conn = MagicMock()
    cursor = MagicMock()
    conn.cursor.return_value = cursor
    cursor.__enter__ = Mock(return_value=cursor)
    cursor.__exit__ = Mock(return_value=False)
    return conn, cursor


@pytest.fixture
def mock_psycopg2_connect(monkeypatch, mock_db_connection):
    """Mock do psycopg2.connect"""
    conn, cursor = mock_db_connection
    
    def mock_connect(*args, **kwargs):
        return conn
    
    monkeypatch.setattr(psycopg2, "connect", mock_connect)
    return conn, cursor


# Fixtures para mock de SQLAlchemy
@pytest.fixture
def mock_sqlalchemy_session():
    """Mock de sessão SQLAlchemy"""
    session = MagicMock()
    return session


# Fixtures para mock de AWS
@pytest.fixture
def mock_boto3_client(monkeypatch):
    """Mock do boto3 client"""
    mock_client = MagicMock()
    
    import boto3
    
    def mock_client_func(service_name, **kwargs):
        return mock_client
    
    monkeypatch.setattr(boto3, "client", mock_client_func)
    return mock_client


# Fixtures para mock de RabbitMQ
@pytest.fixture
def mock_pika_connection(monkeypatch):
    """Mock de conexão RabbitMQ"""
    mock_connection = MagicMock()
    mock_channel = MagicMock()
    mock_connection.channel.return_value = mock_channel
    
    def mock_blocking_connection(*args, **kwargs):
        return mock_connection
    
    monkeypatch.setattr(pika, "BlockingConnection", mock_blocking_connection)
    return mock_connection, mock_channel


# Fixture para verificar se log foi emitido
def assert_log_contains(caplog, level, message_part):
    """
    Verifica se um log com nível e mensagem específicos foi emitido
    
    Args:
        caplog: fixture caplog do pytest
        level: nível do log (ERROR, WARNING, etc)
        message_part: parte da mensagem para buscar
    
    Returns:
        bool: True se encontrou o log
    """
    for record in caplog.records:
        if record.levelname == level and message_part in record.message:
            return True
    return False

