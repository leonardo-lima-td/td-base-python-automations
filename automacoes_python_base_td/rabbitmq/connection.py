"""
Conexão base RabbitMQ
"""
import os
from typing import Optional
import pika
from pika.exceptions import AMQPConnectionError
from ..settings import settings
from ..core.exceptions import RabbitMQConnectionError


class RabbitMQConnection:
    """
    Classe base para conexão com RabbitMQ
    """
    
    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        virtual_host: Optional[str] = None,
    ):
        """
        Inicializa a conexão com RabbitMQ.
        Se não fornecidos, usa valores do settings global.
        """
        # Usa settings global como fallback (se rabbit_usage=True)
        self.host = host or (settings.rabbitmq_host if settings.rabbit_usage else "localhost")
        self.port = port or (settings.rabbitmq_port if settings.rabbit_usage else 5672)
        self.username = username or (settings.rabbitmq_user if settings.rabbit_usage else "guest")
        self.password = password or (settings.rabbitmq_password if settings.rabbit_usage else "guest")
        self.virtual_host = virtual_host or (settings.rabbitmq_vhost if settings.rabbit_usage else "/")
        
        self.connection = None
        self.channel = None
    
    def connect(self):
        """Estabelece conexão com RabbitMQ"""
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            virtual_host=self.virtual_host,
            credentials=credentials,
            heartbeat=600,
            blocked_connection_timeout=300,
        )
        
        try:
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            return True
        except AMQPConnectionError as e:
            raise RabbitMQConnectionError(
                "Falha ao conectar ao RabbitMQ",
                details={
                    "host": self.host,
                    "port": self.port,
                    "vhost": self.virtual_host,
                    "error": str(e)
                }
            ) from e
    
    def close(self):
        """Fecha a conexão"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

