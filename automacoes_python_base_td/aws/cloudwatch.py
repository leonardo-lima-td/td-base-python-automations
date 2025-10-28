"""
Cliente CloudWatch
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from botocore.exceptions import ClientError
from .client import AWSClient


class CloudWatchClient(AWSClient):
    """
    Cliente para operações com AWS CloudWatch Logs
    """
    
    def __init__(self, **kwargs):
        """Inicializa o cliente CloudWatch"""
        super().__init__(**kwargs)
        self.client = self.get_client("logs")
    
    def create_log_group(self, log_group_name: str) -> bool:
        """Cria um log group no CloudWatch"""
        try:
            self.client.create_log_group(logGroupName=log_group_name)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceAlreadyExistsException":
                return True
            print(f"Erro ao criar log group: {e}")
            return False
    
    def create_log_stream(self, log_group_name: str, log_stream_name: str) -> bool:
        """Cria um log stream no CloudWatch"""
        try:
            self.client.create_log_stream(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
            )
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceAlreadyExistsException":
                return True
            print(f"Erro ao criar log stream: {e}")
            return False
    
    def put_log_events(
        self,
        log_group_name: str,
        log_stream_name: str,
        messages: List[str],
    ) -> bool:
        """
        Envia eventos de log para o CloudWatch.
        
        Args:
            log_group_name: Nome do log group
            log_stream_name: Nome do log stream
            messages: Lista de mensagens para enviar
        
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            log_events = [
                {
                    "message": msg,
                    "timestamp": int(datetime.now().timestamp() * 1000),
                }
                for msg in messages
            ]
            
            self.client.put_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                logEvents=log_events,
            )
            return True
        except ClientError as e:
            print(f"Erro ao enviar logs: {e}")
            return False
    
    def get_log_events(
        self,
        log_group_name: str,
        log_stream_name: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Obtém eventos de log do CloudWatch"""
        try:
            if start_time is None:
                start_time = datetime.now() - timedelta(days=1)
            if end_time is None:
                end_time = datetime.now()
            
            response = self.client.get_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                startTime=int(start_time.timestamp() * 1000),
                endTime=int(end_time.timestamp() * 1000),
                limit=limit,
            )
            
            return response.get("events", [])
        except ClientError as e:
            print(f"Erro ao obter logs: {e}")
            return []


# Helper function
def send_logs_to_cloudwatch(
    log_group: str,
    log_stream: str,
    messages: List[str],
) -> bool:
    """Helper para enviar logs rapidamente para CloudWatch"""
    cw = CloudWatchClient()
    cw.create_log_group(log_group)
    cw.create_log_stream(log_group, log_stream)
    return cw.put_log_events(log_group, log_stream, messages)

