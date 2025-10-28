"""
Logger Settings
"""
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LoggerSettings(BaseSettings):
    """Configurações de logging"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    log_level: str = Field(default="INFO")
    log_format: str = Field(default="default")


__all__ = ["LoggerSettings"]
