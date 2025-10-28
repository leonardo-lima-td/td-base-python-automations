"""
Cliente base AWS
"""
import os
from typing import Optional
import boto3
from ..settings import AWSSettings


class AWSClient:
    """
    Cliente base para serviços AWS.
    Gerencia credenciais e configuração comum.
    """
    
    def __init__(
        self,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        region_name: Optional[str] = None,
        settings: Optional[AWSSettings] = None,
    ):
        """
        Inicializa o cliente AWS.
        
        Args:
            aws_access_key_id: AWS Access Key
            aws_secret_access_key: AWS Secret Key
            region_name: Região AWS
            settings: Objeto AWSSettings (opcional)
        """
        if settings:
            self.aws_access_key_id = aws_access_key_id or settings.aws_access_key_id
            self.aws_secret_access_key = aws_secret_access_key or settings.aws_secret_access_key
            self.region_name = region_name or settings.aws_region
        else:
            self.aws_access_key_id = aws_access_key_id or os.getenv("AWS_ACCESS_KEY_ID")
            self.aws_secret_access_key = aws_secret_access_key or os.getenv("AWS_SECRET_ACCESS_KEY")
            self.region_name = region_name or os.getenv("AWS_REGION", "us-east-1")
    
    def get_client(self, service_name: str):
        """
        Retorna um cliente boto3 para o serviço especificado.
        
        Args:
            service_name: Nome do serviço ('s3', 'logs', 'dynamodb', etc)
        
        Returns:
            Cliente boto3
        """
        return boto3.client(
            service_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name,
        )
    
    def get_resource(self, service_name: str):
        """
        Retorna um resource boto3 para o serviço especificado.
        
        Args:
            service_name: Nome do serviço ('s3', 'dynamodb', etc)
        
        Returns:
            Resource boto3
        """
        return boto3.resource(
            service_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name,
        )

