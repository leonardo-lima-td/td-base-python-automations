"""
Pacote base de automações TD - Estrutura Modular
Inclui: Core, Database, AWS, RabbitMQ, Logger, Settings (Pydantic) e Utils
"""

__version__ = "0.1.0"

# ===================================
# Core (Exceptions)
# ===================================
from .core import (
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

# ===================================
# Settings (Pydantic v2 - Unificado)
# ===================================
from .settings import (
    AppSettings,
    settings,
)

# ===================================
# Database (PostgreSQL + SQLAlchemy)
# ===================================
from .database import (
    # PostgreSQL (psycopg2)
    get_connection,
    execute_query,
    execute_many,
    fetch_all,
    fetch_one,
    DatabaseConnection,
    # SQLAlchemy - Base
    Base,
    BaseModel,
    # SQLAlchemy - Session Manager
    DatabaseType,
    DatabaseSessionManager,
    get_manager,
    get_session,
    get_tdax_session,
    get_automations_session,
    get_tdax_manager,
    get_automations_manager,
    # SQLAlchemy - FastAPI
    get_db_dependency,
    get_tdax_db_dependency,
    get_automations_db_dependency,
    # CRUD
    CRUDBase,
    crud_factory,
)

# ===================================
# AWS (S3 + CloudWatch)
# ===================================
from .aws import (
    AWSClient,
    S3Client,
    CloudWatchClient,
    upload_to_s3,
    download_from_s3,
    send_logs_to_cloudwatch,
)

# ===================================
# RabbitMQ
# ===================================
from .rabbitmq import (
    RabbitMQConnection,
    RabbitMQPublisher,
    RabbitMQConsumer,
    publish_message,
    consume_messages,
)

# ===================================
# Logger (Loguru)
# ===================================
from .logger import (
    setup_logger,
    get_logger,
    logger,
)

# ===================================
# Utils
# ===================================
from .utils import (
    # File utils
    listdir,
    getdir,
    openfile,
    getsize,
    exists,
    isfile,
    isdir,
    create_dir,
    remove_file,
    remove_dir,
    copy_file,
    move_file,
    read_file,
    write_file,
    # String utils
    slugify,
    truncate,
    capitalize_words,
    # Date utils
    format_timestamp,
    parse_date,
    days_between,
)

# ===================================
# Exportações públicas
# ===================================
__all__ = [
    # Core - Exceptions
    "BaseAppException",
    "DatabaseException",
    "DatabaseConnectionError",
    "DatabaseQueryError",
    "ModelNotFoundError",
    "AWSException",
    "S3Exception",
    "CloudWatchException",
    "RabbitMQException",
    "RabbitMQConnectionError",
    "RabbitMQPublishError",
    "RabbitMQConsumeError",
    "SettingsException",
    "ConfigurationError",
    "ValidationError",
    "NotFoundError",
    "AlreadyExistsError",
    # Settings
    "AppSettings",
    "settings",
    # Database - PostgreSQL
    "get_connection",
    "execute_query",
    "execute_many",
    "fetch_all",
    "fetch_one",
    "DatabaseConnection",
    # Database - SQLAlchemy Base
    "Base",
    "BaseModel",
    # Database - Session Manager
    "DatabaseType",
    "DatabaseSessionManager",
    "get_manager",
    "get_session",
    "get_tdax_session",
    "get_automations_session",
    "get_tdax_manager",
    "get_automations_manager",
    # Database - FastAPI
    "get_db_dependency",
    "get_tdax_db_dependency",
    "get_automations_db_dependency",
    # Database - CRUD
    "CRUDBase",
    "crud_factory",
    # AWS
    "AWSClient",
    "S3Client",
    "CloudWatchClient",
    "upload_to_s3",
    "download_from_s3",
    "send_logs_to_cloudwatch",
    # RabbitMQ
    "RabbitMQConnection",
    "RabbitMQPublisher",
    "RabbitMQConsumer",
    "publish_message",
    "consume_messages",
    # Logger
    "setup_logger",
    "get_logger",
    "logger",
    # Utils - File
    "listdir",
    "getdir",
    "openfile",
    "getsize",
    "exists",
    "isfile",
    "isdir",
    "create_dir",
    "remove_file",
    "remove_dir",
    "copy_file",
    "move_file",
    "read_file",
    "write_file",
    # Utils - String
    "slugify",
    "truncate",
    "capitalize_words",
    # Utils - Date
    "format_timestamp",
    "parse_date",
    "days_between",
]
