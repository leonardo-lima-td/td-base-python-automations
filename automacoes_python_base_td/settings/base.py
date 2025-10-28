"""
Configurações base usando Pydantic Settings
Extensível para adicionar suas próprias configurações
"""
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseAppSettings(BaseSettings):
    """
    Configurações base da aplicação.
    Herda desta classe para criar suas próprias configurações.
    
    Exemplo:
        class MyAppSettings(BaseAppSettings):
            api_key: str  # obrigatório (sem default)
            debug: bool = Field(default=False)  # opcional
        
        settings = MyAppSettings()
        print(settings.api_key)
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # Configurações gerais
    env: str = Field(default="development")
    debug: bool = Field(default=False)
    app_name: str = Field(default="TD App")


# Instância global de configurações
_settings: Optional[BaseAppSettings] = None


def get_settings() -> BaseAppSettings:
    """
    Retorna a instância global de configurações.
    
    Returns:
        BaseAppSettings configurado
    
    Exemplo:
        settings = get_settings()
        print(settings.environment)
    """
    global _settings
    if _settings is None:
        _settings = BaseAppSettings()
    return _settings
