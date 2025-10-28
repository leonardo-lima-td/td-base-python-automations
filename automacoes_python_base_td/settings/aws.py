"""
AWS Settings
"""
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AWSSettings(BaseSettings):
    """Configurações AWS"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    aws_access_key_id: Optional[str] = Field(default=None)
    aws_secret_access_key: Optional[str] = Field(default=None)
    aws_region: str = Field(default="us-east-1")
    aws_s3_bucket: Optional[str] = Field(default=None)


__all__ = ["AWSSettings"]
