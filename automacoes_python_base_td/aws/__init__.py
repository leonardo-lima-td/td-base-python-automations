"""
Módulo AWS - S3 e CloudWatch
"""
from .client import AWSClient
from .s3 import S3Client, upload_to_s3, download_from_s3
from .cloudwatch import CloudWatchClient, send_logs_to_cloudwatch

__all__ = [
    "AWSClient",
    "S3Client",
    "CloudWatchClient",
    "upload_to_s3",
    "download_from_s3",
    "send_logs_to_cloudwatch",
]

