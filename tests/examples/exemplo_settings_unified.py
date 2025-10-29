"""
Exemplos de uso do AppSettings unificado
Demonstra as funcionalidades condicionais e propriedades computadas
"""

# ==========================================
# Exemplo 1: Uso básico
# ==========================================
print("=" * 50)
print("EXEMPLO 1: Uso Básico")
print("=" * 50)

from automacoes_python_base_td.settings import settings

print(f"Ambiente: {settings.env}")
print(f"App Name: {settings.app_name}")
print(f"Debug Mode: {settings.debug_mode}")
print(f"Log Level Efetivo: {settings.effective_log_level}")
print(f"Log Destination: {settings.log_destination}")
print(f"Log Stream Name: {settings.log_stream_name}")
print()

# ==========================================
# Exemplo 2: URLs de Database (computadas)
# ==========================================
print("=" * 50)
print("EXEMPLO 2: URLs de Database")
print("=" * 50)

print(f"PostgreSQL URL: {settings.postgres_url}")
print(f"TDAX URL: {settings.tdax_url}")
print(f"Automations URL: {settings.automations_url}")
print()

# ==========================================
# Exemplo 3: Verificação de Ambiente
# ==========================================
print("=" * 50)
print("EXEMPLO 3: Verificação de Ambiente")
print("=" * 50)

print(f"É Development? {settings.is_development}")
print(f"É Staging? {settings.is_staging}")
print(f"É Production? {settings.is_production}")
print()

# ==========================================
# Exemplo 4: CloudWatch (condicional)
# ==========================================
print("=" * 50)
print("EXEMPLO 4: CloudWatch")
print("=" * 50)

print(f"Usar CloudWatch? {settings.use_cloudwatch}")
if settings.use_cloudwatch:
    print(f"Log Group: {settings.cloudwatch_log_group}")
    print(f"Log Stream: {settings.log_stream_name}")
    print(f"Region: {settings.cloudwatch_region}")
else:
    print("CloudWatch não habilitado (dev mode ou não configurado)")
print()

# ==========================================
# Exemplo 5: RabbitMQ (condicional)
# ==========================================
print("=" * 50)
print("EXEMPLO 5: RabbitMQ")
print("=" * 50)

print(f"Usar RabbitMQ? {settings.rabbit_usage}")
if settings.rabbit_usage:
    print(f"RabbitMQ URL: {settings.rabbitmq_connection_url}")
    print(f"Host: {settings.rabbitmq_host}")
    print(f"Port: {settings.rabbitmq_port}")
    print(f"VHost: {settings.rabbitmq_vhost}")
else:
    print("RabbitMQ não habilitado")
print()

# ==========================================
# Exemplo 6: Criando settings customizado
# ==========================================
print("=" * 50)
print("EXEMPLO 6: Settings Customizado")
print("=" * 50)

from automacoes_python_base_td.settings import AppSettings
import os

# Sobrescrever com variáveis de ambiente
os.environ["ENV"] = "production"
os.environ["DEBUG_MODE"] = "true"
os.environ["APP_NAME"] = "Minha App"
os.environ["DB_HOST"] = "prod-db.example.com"
os.environ["DB_USER"] = "prod_user"
os.environ["DB_PASSWORD"] = "prod_pass"

custom_settings = AppSettings()
print(f"Ambiente: {custom_settings.env}")
print(f"Debug Mode: {custom_settings.debug_mode}")
print(f"Log Level Efetivo: {custom_settings.effective_log_level}")
print(f"Log Stream: {custom_settings.log_stream_name}")
print(f"Database Host: {custom_settings.db_host}")
print()

# ==========================================
# Exemplo 7: Integração com Logger
# ==========================================
print("=" * 50)
print("EXEMPLO 7: Integração com Logger")
print("=" * 50)

from automacoes_python_base_td.logger import setup_logger, get_logger

# Configura logger baseado em settings
setup_logger(
    level=settings.effective_log_level,
    log_format=settings.log_format,
    use_cloudwatch=settings.use_cloudwatch,
)

logger = get_logger()
logger.info(f"🚀 Aplicação iniciada: {settings.app_name}")
logger.info(f"📝 Ambiente: {settings.env}")
logger.info(f"🎯 Logs indo para: {settings.log_destination}")

if settings.debug_mode:
    logger.debug("🔍 Debug mode ativo - logs detalhados habilitados")

print()

# ==========================================
# Exemplo 8: Validação de RabbitMQ
# ==========================================
print("=" * 50)
print("EXEMPLO 8: Validação RabbitMQ")
print("=" * 50)

try:
    # Tentar criar settings com rabbit_usage=true mas sem configurações
    os.environ["RABBIT_USAGE"] = "true"
    os.environ.pop("RABBITMQ_HOST", None)  # Remove configuração
    
    invalid_settings = AppSettings()
except ValueError as e:
    print(f"✅ Validação funcionando: {e}")
    
# Restaurar variáveis
os.environ["RABBIT_USAGE"] = "false"
print()

# ==========================================
# Exemplo 9: Todas as propriedades computadas
# ==========================================
print("=" * 50)
print("EXEMPLO 9: Todas as Propriedades Computadas")
print("=" * 50)

print("Database:")
print(f"  - postgres_url: {settings.postgres_url}")
print(f"  - tdax_url: {settings.tdax_url}")
print(f"  - automations_url: {settings.automations_url}")
print()

print("Logger:")
print(f"  - use_cloudwatch: {settings.use_cloudwatch}")
print(f"  - log_destination: {settings.log_destination}")
print(f"  - log_stream_name: {settings.log_stream_name}")
print(f"  - effective_log_level: {settings.effective_log_level}")
print()

print("RabbitMQ:")
print(f"  - rabbitmq_connection_url: {settings.rabbitmq_connection_url}")
print()

print("Helpers:")
print(f"  - is_development: {settings.is_development}")
print(f"  - is_staging: {settings.is_staging}")
print(f"  - is_production: {settings.is_production}")
print()

print("✅ Todos os exemplos executados com sucesso!")

