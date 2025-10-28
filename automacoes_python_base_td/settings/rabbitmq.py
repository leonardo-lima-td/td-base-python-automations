"""
RabbitMQ Settings
"""
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RabbitMQSettings(BaseSettings):
    """Configurações RabbitMQ"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    rabbitmq_host: str = Field(default="localhost")
    rabbitmq_port: int = Field(default=5672)
    rabbitmq_user: str = Field(default="guest")
    rabbitmq_password: str = Field(default="guest")
    rabbitmq_vhost: str = Field(default="/")


__all__ = ["RabbitMQSettings"]
