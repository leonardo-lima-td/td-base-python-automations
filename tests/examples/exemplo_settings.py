"""
Exemplo de uso das Settings (Configurações com Pydantic)
"""
from automacoes_python_base_td import (
    get_settings, DatabaseSettings, AWSSettings, 
    RabbitMQSettings, LoggerSettings, logger
)
from dotenv import load_dotenv

load_dotenv()

logger.info("=== Exemplo de Settings ===")

# Obter as configurações (singleton)
settings = get_settings()

# ===================================
# Configurações gerais da aplicação
# ===================================
logger.info("\n### Configurações Gerais ###")
logger.info(f"APP_NAME: {settings.APP_NAME}")
logger.info(f"ENV: {settings.ENV}")
logger.info(f"DEBUG: {settings.DEBUG}")

# ===================================
# Configurações do Database
# ===================================
logger.info("\n### Configurações do Database ###")
logger.info(f"DB_HOST: {settings.database.DB_HOST}")
logger.info(f"DB_PORT: {settings.database.DB_PORT}")
logger.info(f"DB_NAME: {settings.database.DB_NAME}")
logger.info(f"DB_USER: {settings.database.DB_USER}")
# Não mostrar a senha por segurança
logger.info(f"DB_PASSWORD: {'*' * len(settings.database.DB_PASSWORD)}")

# Connection string
logger.info(f"Connection String: {settings.database.connection_string}")

# ===================================
# Configurações do AWS
# ===================================
logger.info("\n### Configurações do AWS ###")
logger.info(f"AWS_REGION: {settings.aws.AWS_REGION}")
logger.info(f"AWS_ACCESS_KEY_ID: {settings.aws.AWS_ACCESS_KEY_ID[:8]}...")
logger.info(f"AWS_S3_BUCKET: {settings.aws.AWS_S3_BUCKET}")
logger.info(f"AWS_CLOUDWATCH_LOG_GROUP: {settings.aws.AWS_CLOUDWATCH_LOG_GROUP}")

# ===================================
# Configurações do RabbitMQ
# ===================================
logger.info("\n### Configurações do RabbitMQ ###")
logger.info(f"RABBITMQ_HOST: {settings.rabbitmq.RABBITMQ_HOST}")
logger.info(f"RABBITMQ_PORT: {settings.rabbitmq.RABBITMQ_PORT}")
logger.info(f"RABBITMQ_USER: {settings.rabbitmq.RABBITMQ_USER}")
logger.info(f"RABBITMQ_VHOST: {settings.rabbitmq.RABBITMQ_VHOST}")

# Connection string
logger.info(f"Connection String: {settings.rabbitmq.connection_string}")

# ===================================
# Configurações do Logger
# ===================================
logger.info("\n### Configurações do Logger ###")
logger.info(f"LOG_LEVEL: {settings.logger.LOG_LEVEL}")
logger.info(f"LOG_FORMAT: {settings.logger.LOG_FORMAT}")
logger.info(f"LOG_FILE: {settings.logger.LOG_FILE}")
logger.info(f"LOG_ROTATION: {settings.logger.LOG_ROTATION}")

# ===================================
# Validação das configurações
# ===================================
logger.info("\n### Validação ###")

try:
    # As settings já são validadas automaticamente pelo Pydantic
    logger.success("Todas as configurações são válidas!")
    
    # Você pode acessar as configurações de forma segura
    if settings.DEBUG:
        logger.warning("Aplicação rodando em modo DEBUG")
    else:
        logger.info("Aplicação rodando em modo PRODUCTION")
        
except Exception as e:
    logger.error(f"Erro nas configurações: {e}")

logger.info("\nDica: Configure suas variáveis de ambiente no arquivo .env")

