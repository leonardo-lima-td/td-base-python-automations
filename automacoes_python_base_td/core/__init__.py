"""
Core - Funcionalidades centrais do pacote
"""
from .exceptions import (
    # Base
    BaseAppException,
    # Database
    DatabaseException,
    DatabaseConnectionError,
    DatabaseQueryError,
    ModelNotFoundError,
    # AWS
    AWSException,
    S3Exception,
    CloudWatchException,
    # RabbitMQ
    RabbitMQException,
    RabbitMQConnectionError,
    RabbitMQPublishError,
    RabbitMQConsumeError,
    # Settings
    SettingsException,
    ConfigurationError,
    # Generic
    ValidationError,
    NotFoundError,
    AlreadyExistsError,
)


__all__ = [
    # Base
    "BaseAppException",
    # Database
    "DatabaseException",
    "DatabaseConnectionError",
    "DatabaseQueryError",
    "ModelNotFoundError",
    # AWS
    "AWSException",
    "S3Exception",
    "CloudWatchException",
    # RabbitMQ
    "RabbitMQException",
    "RabbitMQConnectionError",
    "RabbitMQPublishError",
    "RabbitMQConsumeError",
    # Settings
    "SettingsException",
    "ConfigurationError",
    # Generic
    "ValidationError",
    "NotFoundError",
    "AlreadyExistsError",
]

