"""
Módulo de configurações usando Pydantic Settings v2

NOVO: Settings unificado com validações condicionais
- Importação simplificada: `from automacoes_python_base_td.settings import settings`
- Todas as configurações em um único lugar
- Propriedades computadas e validações condicionais

ANTIGO (deprecated): Arquivos separados ainda disponíveis para compatibilidade
- BaseAppSettings, DatabaseSettings, AWSSettings, RabbitMQSettings, LoggerSettings
"""

# Novo settings unificado (RECOMENDADO)
from .settings import AppSettings, settings

__all__ = [
    "AppSettings",
    "settings"
]

