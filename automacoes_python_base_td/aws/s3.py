"""
Cliente S3
"""
from typing import Optional, Dict, List
from botocore.exceptions import ClientError
from .client import AWSClient
from ..core.exceptions import S3Exception


class S3Client(AWSClient):
    """
    Cliente para operações com AWS S3
    """
    
    def __init__(self, **kwargs):
        """Inicializa o cliente S3"""
        super().__init__(**kwargs)
        self.client = self.get_client("s3")
    
    def upload_file(
        self,
        file_path: str,
        bucket: str,
        key: str,
        metadata: Optional[Dict[str, str]] = None,
    ) -> bool:
        """
        Faz upload de um arquivo para o S3.
        
        Args:
            file_path: Caminho do arquivo local
            bucket: Nome do bucket S3
            key: Chave (caminho) do arquivo no S3
            metadata: Metadados opcionais
        
        Returns:
            True se sucesso, False caso contrário
        
        Exemplo:
            s3 = S3Client()
            s3.upload_file("/path/file.csv", "my-bucket", "data/file.csv")
        """
        try:
            extra_args = {}
            if metadata:
                extra_args["Metadata"] = metadata
            
            self.client.upload_file(file_path, bucket, key, ExtraArgs=extra_args)
            return True
        except ClientError as e:
            raise S3Exception(
                f"Erro ao fazer upload para S3",
                details={"file": file_path, "bucket": bucket, "key": key, "error": str(e)}
            ) from e
    
    def download_file(self, bucket: str, key: str, file_path: str) -> bool:
        """
        Faz download de um arquivo do S3.
        
        Args:
            bucket: Nome do bucket S3
            key: Chave do arquivo no S3
            file_path: Caminho para salvar o arquivo localmente
        
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            self.client.download_file(bucket, key, file_path)
            return True
        except ClientError as e:
            print(f"Erro ao fazer download: {e}")
            return False
    
    def upload_bytes(
        self,
        data: bytes,
        bucket: str,
        key: str,
        content_type: Optional[str] = None,
    ) -> bool:
        """
        Faz upload de bytes para o S3.
        
        Args:
            data: Dados em bytes
            bucket: Nome do bucket S3
            key: Chave do arquivo no S3
            content_type: Tipo de conteúdo (ex: 'application/json')
        
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            extra_args = {}
            if content_type:
                extra_args["ContentType"] = content_type
            
            self.client.put_object(Bucket=bucket, Key=key, Body=data, **extra_args)
            return True
        except ClientError as e:
            print(f"Erro ao fazer upload: {e}")
            return False
    
    def download_bytes(self, bucket: str, key: str) -> Optional[bytes]:
        """
        Faz download de bytes do S3.
        
        Args:
            bucket: Nome do bucket S3
            key: Chave do arquivo no S3
        
        Returns:
            Bytes do arquivo ou None se erro
        """
        try:
            response = self.client.get_object(Bucket=bucket, Key=key)
            return response["Body"].read()
        except ClientError as e:
            print(f"Erro ao fazer download: {e}")
            return None
    
    def list_files(self, bucket: str, prefix: str = "") -> List[str]:
        """
        Lista arquivos em um bucket S3.
        
        Args:
            bucket: Nome do bucket S3
            prefix: Prefixo para filtrar arquivos
        
        Returns:
            Lista de chaves dos arquivos
        """
        try:
            response = self.client.list_objects_v2(Bucket=bucket, Prefix=prefix)
            if "Contents" in response:
                return [obj["Key"] for obj in response["Contents"]]
            return []
        except ClientError as e:
            print(f"Erro ao listar arquivos: {e}")
            return []
    
    def file_exists(self, bucket: str, key: str) -> bool:
        """Verifica se um arquivo existe no S3"""
        try:
            self.client.head_object(Bucket=bucket, Key=key)
            return True
        except ClientError:
            return False


# Funções helper
def upload_to_s3(file_path: str, bucket: str, key: str) -> bool:
    """Helper para fazer upload rápido para S3"""
    s3 = S3Client()
    return s3.upload_file(file_path, bucket, key)


def download_from_s3(bucket: str, key: str, file_path: str) -> bool:
    """Helper para fazer download rápido do S3"""
    s3 = S3Client()
    return s3.download_file(bucket, key, file_path)

