"""
Database Settings
"""
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Configurações de banco de dados"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    # PostgreSQL
    db_host: str = Field(default="localhost")
    db_port: int = Field(default=5432)
    db_name: str = Field(default="postgres")
    db_user: str = Field(default="postgres")
    db_password: str = Field(default="")
    
    # SQLAlchemy
    database_url: Optional[str] = Field(default=None)
    database_url_tdax: Optional[str] = Field(default=None)
    database_url_automation: Optional[str] = Field(default=None)
    
    @property
    def postgres_url(self) -> str:
        """Constrói a URL do PostgreSQL"""
        if self.database_url:
            return self.database_url
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    @property
    def tdax_url(self) -> str:
        """URL do banco TDAX"""
        if self.database_url_tdax:
            return self.database_url_tdax
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/tdax"
    
    @property
    def automations_url(self) -> str:
        """URL do banco Automations"""
        if self.database_url_automation:
            return self.database_url_automation
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/automacoes"


__all__ = ["DatabaseSettings"]
