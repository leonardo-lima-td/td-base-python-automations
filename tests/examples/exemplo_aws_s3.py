"""
Exemplo de uso do AWS S3
"""
from automacoes_python_base_td import S3Client, upload_to_s3, download_from_s3, logger
from dotenv import load_dotenv
import os

load_dotenv()

# Configurações
BUCKET_NAME = os.getenv("AWS_S3_BUCKET", "meu-bucket")
FILE_PATH = "test.txt"
S3_KEY = "uploads/test.txt"

logger.info("=== Exemplo de uso do S3 ===")

# Forma 1: Usando a classe S3Client
s3_client = S3Client()

# Upload de arquivo
logger.info(f"Fazendo upload do arquivo {FILE_PATH}")
# s3_client.upload_file(FILE_PATH, BUCKET_NAME, S3_KEY)
# logger.success(f"Arquivo enviado para s3://{BUCKET_NAME}/{S3_KEY}")

# Download de arquivo
logger.info(f"Fazendo download do arquivo {S3_KEY}")
# s3_client.download_file(BUCKET_NAME, S3_KEY, "downloaded_test.txt")
# logger.success("Arquivo baixado com sucesso!")

# Listar arquivos no bucket
logger.info(f"Listando arquivos no bucket {BUCKET_NAME}")
# files = s3_client.list_files(BUCKET_NAME, prefix="uploads/")
# for file in files:
#     logger.info(f"  - {file}")

# Deletar arquivo
# s3_client.delete_file(BUCKET_NAME, S3_KEY)
# logger.success(f"Arquivo {S3_KEY} deletado")

# Forma 2: Usando funções diretas
logger.info("\n=== Usando funções diretas ===")

# Upload direto
# upload_to_s3(FILE_PATH, BUCKET_NAME, S3_KEY)
# logger.success("Upload realizado!")

# Download direto
# download_from_s3(BUCKET_NAME, S3_KEY, "downloaded_test2.txt")
# logger.success("Download realizado!")

logger.info("Operações S3 concluídas!")

