"""
Testes para cliente S3
Testa funcionalidade, exceções e logs
"""
import pytest
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError
from automacoes_python_base_td.aws.s3 import S3Client
from automacoes_python_base_td.core.exceptions import S3Exception


class TestS3Client:
    """Testes para S3Client"""
    
    @patch('boto3.client')
    def test_upload_file_success(self, mock_boto_client):
        """Testa upload bem-sucedido"""
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client
        
        s3 = S3Client(
            aws_access_key_id="test",
            aws_secret_access_key="test",
            region_name="us-east-1"
        )
        
        result = s3.upload_file(
            "/path/file.txt",
            "my-bucket",
            "uploads/file.txt"
        )
        
        assert result is True
        mock_client.upload_file.assert_called_once()
    
    @patch('boto3.client')
    def test_upload_file_failure_raises_exception(self, mock_boto_client, caplog):
        """Testa se erro no upload lança S3Exception"""
        import logging
        caplog.set_level(logging.ERROR)
        
        mock_client = MagicMock()
        # Simula erro do boto3
        mock_client.upload_file.side_effect = ClientError(
            {"Error": {"Code": "NoSuchBucket", "Message": "Bucket não existe"}},
            "PutObject"
        )
        mock_boto_client.return_value = mock_client
        
        s3 = S3Client(
            aws_access_key_id="test",
            aws_secret_access_key="test"
        )
        
        with pytest.raises(S3Exception) as exc_info:
            s3.upload_file("/path/file.txt", "my-bucket", "file.txt")
        
        # Verifica exceção
        exc = exc_info.value
        assert exc.code == "S3_ERROR"
        assert "bucket" in exc.details
        assert "key" in exc.details
        
        # Verifica log
        assert any("S3Exception" in record.message for record in caplog.records)
    
    @patch('boto3.client')
    def test_upload_with_metadata(self, mock_boto_client):
        """Testa upload com metadados"""
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client
        
        s3 = S3Client(
            aws_access_key_id="test",
            aws_secret_access_key="test"
        )
        
        metadata = {"author": "test", "version": "1.0"}
        result = s3.upload_file(
            "/path/file.txt",
            "my-bucket",
            "file.txt",
            metadata=metadata
        )
        
        assert result is True
        # Verifica que metadados foram passados
        call_args = mock_client.upload_file.call_args
        assert "ExtraArgs" in call_args[1]
        assert "Metadata" in call_args[1]["ExtraArgs"]

