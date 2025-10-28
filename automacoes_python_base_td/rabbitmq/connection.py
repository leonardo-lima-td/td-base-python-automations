"""
Conexão base RabbitMQ
"""
import os
from typing import Optional
import pika
from pika.exceptions import AMQPConnectionError
from ..settings import RabbitMQSettings
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
        settings: Optional[RabbitMQSettings] = None,
    ):
        """Inicializa a conexão com RabbitMQ"""
        if settings:
            self.host = host or settings.rabbitmq_host
            self.port = port or settings.rabbitmq_port
            self.username = username or settings.rabbitmq_user
            self.password = password or settings.rabbitmq_password
            self.virtual_host = virtual_host or settings.rabbitmq_vhost
        else:
            self.host = host or os.getenv("RABBITMQ_HOST", "localhost")
            self.port = port or int(os.getenv("RABBITMQ_PORT", "5672"))
            self.username = username or os.getenv("RABBITMQ_USER", "guest")
            self.password = password or os.getenv("RABBITMQ_PASSWORD", "guest")
            self.virtual_host = virtual_host or os.getenv("RABBITMQ_VHOST", "/")
        
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

