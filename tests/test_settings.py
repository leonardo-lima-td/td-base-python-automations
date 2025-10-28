"""
Testes para módulo settings
"""
import pytest
import os
from automacoes_python_base_td.settings import (
    DatabaseSettings,
    AWSSettings,
    RabbitMQSettings,
    LoggerSettings,
)


class TestDatabaseSettings:
    """Testes para DatabaseSettings"""
    
    def test_default_values(self):
        """Testa valores padrão"""
        settings = DatabaseSettings()
        assert settings.db_host == "localhost"
        assert settings.db_port == 5432
        assert settings.db_name == "postgres"
    
    def test_postgres_url(self):
        """Testa construção da URL PostgreSQL"""
        settings = DatabaseSettings(
            db_host="testhost",
            db_port=5433,
            db_name="testdb",
            db_user="testuser",
            db_password="testpass"
        )
        url = settings.postgres_url
        assert "postgresql://" in url
        assert "testhost" in url
        assert "testdb" in url


class TestAWSSettings:
    """Testes para AWSSettings"""
    
    def test_default_region(self):
        """Testa região padrão"""
        settings = AWSSettings()
        assert settings.aws_region == "us-east-1"


class TestRabbitMQSettings:
    """Testes para RabbitMQSettings"""
    
    def test_default_values(self):
        """Testa valores padrão"""
        settings = RabbitMQSettings()
        assert settings.rabbitmq_host == "localhost"
        assert settings.rabbitmq_port == 5672
        assert settings.rabbitmq_vhost == "/"


class TestLoggerSettings:
    """Testes para LoggerSettings"""
    
    def test_default_values(self):
        """Testa valores padrão"""
        settings = LoggerSettings()
        assert settings.log_level == "INFO"
        assert settings.log_rotation == "100 MB"

