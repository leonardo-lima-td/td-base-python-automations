"""
Configurações unificadas usando Pydantic Settings v2
Todas as configurações em um único arquivo com validações condicionais
"""
from datetime import datetime
from typing import Optional, Literal
from pydantic import Field, computed_field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """
    Configurações unificadas da aplicação.
    Extensível para adicionar suas próprias configurações.
    
    Características:
    - Logs condicionais baseados em ambiente (dev = local, prod = CloudWatch)
    - Log stream dinâmico com app_name + env + data
    - Debug mode para logs detalhados
    - RabbitMQ condicional (rabbit_usage)
    
    Exemplo:
        from automacoes_python_base_td.settings import settings
        
        print(settings.env)
        print(settings.log_destination)  # "local" ou "cloudwatch"
        print(settings.log_stream_name)  # "minha-app-dev-29102025"
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # ==========================================
    # CONFIGURAÇÕES GERAIS
    # ==========================================
    env: Literal["dev", "staging", "prd"] = Field(default="dev")
    debug_mode: bool = Field(default=False)
    app_name: str = Field(default="td-base-python-automations")
    
    # ==========================================
    # DATABASE - PostgreSQL
    # ==========================================
    db_host: str
    db_port: int = Field(default=5432)
    db_user: str
    db_password: str
    db_name: str = Field(default="tdax")
    
    # SQLAlchemy - URLs customizadas (opcional)
    database_url: Optional[str] = Field(default=None)
    database_url_tdax: Optional[str] = Field(default=None)
    database_url_automation: Optional[str] = Field(default=None)
    
    # ==========================================
    # AWS
    # ==========================================
    aws_access_key_id: Optional[str] = Field(default=None)
    aws_secret_access_key: Optional[str] = Field(default=None)
    aws_region: str = Field(default="us-east-1")
    aws_s3_bucket: Optional[str] = Field(default=None)
    
    # ==========================================
    # LOGGER
    # ==========================================
    log_level: str = Field(default="INFO")
    log_format: Literal["default", "json", "simple"] = Field(default="default")
    
    # CloudWatch (condicional - usado apenas se env != dev)
    cloudwatch_region: Optional[str] = Field(default=None)
    
    # ==========================================
    # RABBITMQ (Condicional)
    # ==========================================
    rabbit_usage: bool = Field(default=False)
    rabbitmq_host: Optional[str] = Field(default=None)
    rabbitmq_port: Optional[int] = Field(default=None)
    rabbitmq_user: Optional[str] = Field(default=None)
    rabbitmq_password: Optional[str] = Field(default=None)
    rabbitmq_vhost: Optional[str] = Field(default=None)
    
    # ==========================================
    # VALIDAÇÕES CONDICIONAIS
    # ==========================================
    
    @model_validator(mode='after')
    def validate_rabbitmq_if_enabled(self):
        """
        Se rabbit_usage=True, todas as variáveis do RabbitMQ são obrigatórias.
        Se rabbit_usage=False, as variáveis são opcionais.
        """
        if self.rabbit_usage:
            required_fields = {
                'rabbitmq_host': self.rabbitmq_host,
                'rabbitmq_port': self.rabbitmq_port,
                'rabbitmq_user': self.rabbitmq_user,
                'rabbitmq_password': self.rabbitmq_password,
                'rabbitmq_vhost': self.rabbitmq_vhost,
            }
            
            missing = [field for field, value in required_fields.items() if value is None]
            
            if missing:
                raise ValueError(
                    f"rabbit_usage=True requer as seguintes variáveis: {', '.join(missing)}"
                )
        
        return self
    
    @model_validator(mode='after')
    def validate_cloudwatch_if_production(self):
        """
        Se env != dev e cloudwatch estiver configurado, valida campos obrigatórios.
        """
        if self.env != "dev":
            if not self.cloudwatch_region:
                self.cloudwatch_region = self.aws_region
        
        return self
    
    # ==========================================
    # PROPRIEDADES COMPUTADAS - DATABASE
    # ==========================================
    
    @computed_field
    @property
    def postgres_url(self) -> str:
        """Constrói a URL do PostgreSQL"""
        if self.database_url:
            return self.database_url
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    @computed_field
    @property
    def tdax_url(self) -> str:
        """URL do banco TDAX"""
        if self.database_url_tdax:
            return self.database_url_tdax
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/tdax"
    
    @computed_field
    @property
    def automations_url(self) -> str:
        """URL do banco Automations"""
        if self.database_url_automation:
            return self.database_url_automation
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/automacoes"
    
    # ==========================================
    # PROPRIEDADES COMPUTADAS - LOGGER
    # ==========================================
    
    @computed_field
    @property
    def use_cloudwatch(self) -> bool:
        """
        Determina se deve usar CloudWatch baseado no ambiente.
        - dev: sempre local
        - staging/production: CloudWatch se configurado
        """
        if self.env == "dev":
            return False
        
        return bool(self.cloudwatch_region)
    
    @computed_field
    @property
    def log_destination(self) -> Literal["local", "cloudwatch"]:
        """Retorna o destino dos logs"""
        return "cloudwatch" if self.use_cloudwatch else "local"
    
    @computed_field
    @property
    def log_stream_name(self) -> str:
        """
        Gera o nome do log stream dinamicamente.
        Formato: {app_name}-{env}-{DDMMYYYY}
        Exemplo: td-app-production-29102025
        """
        date_str = datetime.now().strftime("%d%m%Y")
        app_slug = self.app_name.lower().replace(" ", "-").replace("_", "-")
        return f"{app_slug}-{self.env}-{date_str}"

    @computed_field
    @property
    def cloudwatch_log_group(self) -> str:
        """
        Gera o nome do log group dinamicamente.
        Formato: /automacoes/{app_slug}
        Exemplo: /automacoes/td-base-python-automations
        """
        app_slug = self.app_name.lower().replace(" ", "-").replace("_", "-")
        return f"/automacoes/{app_slug}"
    
    @computed_field
    @property
    def effective_log_level(self) -> str:
        """
        Determina o nível de log efetivo baseado em debug_mode.
        Se debug_mode=True, força DEBUG.
        Caso contrário, usa log_level configurado.
        """
        if self.debug_mode:
            return "DEBUG"
        return self.log_level.upper()
    
    # ==========================================
    # PROPRIEDADES COMPUTADAS - RABBITMQ
    # ==========================================
    
    @computed_field
    @property
    def rabbitmq_connection_url(self) -> Optional[str]:
        """
        Constrói a URL de conexão do RabbitMQ.
        Retorna None se rabbit_usage=False.
        """
        if not self.rabbit_usage:
            return None
        
        return f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}@{self.rabbitmq_host}:{self.rabbitmq_port}{self.rabbitmq_vhost}"
    
    # ==========================================
    # HELPERS
    # ==========================================
    
    @property
    def is_development(self) -> bool:
        """Verifica se está em ambiente de desenvolvimento"""
        return self.env == "dev"
    
    @property
    def is_production(self) -> bool:
        """Verifica se está em ambiente de produção"""
        return self.env == "prd"
    
    @property
    def is_staging(self) -> bool:
        """Verifica se está em ambiente de staging"""
        return self.env == "staging"


# ==========================================
# INSTÂNCIA GLOBAL
# ==========================================

# Instância global única (Singleton pattern)
settings = AppSettings()

if __name__ == "__main__":
    print(settings.dump())
    # print(settings.env)
    # print(settings.log_destination)
    # print(settings.log_stream_name)
    # print(settings.postgres_url)
    # print(settings.tdax_url)
    # print(settings.automations_url)
    # print(settings.rabbitmq_connection_url)
    # print(settings.is_development)
    # print(settings.is_production)
    # print(settings.is_staging)
    # print(settings.use_cloudwatch)
    # print(settings.effective_log_level)
    # print(settings.log_format)
    # print(settings.log_level)
    # print(settings.log_destination)
    # print(settings.log_stream_name)
    # print(settings.postgres_url)
    # print(settings.tdax_url)
    # print(settings.automations_url)


__all__ = ["AppSettings", "settings"]

