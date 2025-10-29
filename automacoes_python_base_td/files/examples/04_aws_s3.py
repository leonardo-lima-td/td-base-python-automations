"""
EXEMPLO 4: AWS S3
=================

Como trabalhar com arquivos no Amazon S3.

PRÉ-REQUISITOS:
- Pacote instalado: pip install automacoes-python-base-td
- Variáveis no .env: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
"""

from automacoes_python_base_td.aws import S3Client
from automacoes_python_base_td.logger import get_logger

logger = get_logger()

# ====================================================================
# CRIAR CLIENTE S3
# ====================================================================

def exemplo_upload():
    """Upload de arquivo para S3"""
    logger.info("Fazendo upload para S3...")
    
    s3 = S3Client(bucket_name="meu-bucket-producao")
    
    # Upload simples
    s3.upload_file(
        local_path="relatorio.pdf",
        s3_key="relatorios/2025/10/vendas.pdf"
    )
    logger.info("✅ Arquivo enviado!")


def exemplo_upload_com_metadata():
    """Upload com metadados customizados"""
    logger.info("Upload com metadados...")
    
    s3 = S3Client(bucket_name="meu-bucket")
    
    s3.upload_file(
        local_path="dados.csv",
        s3_key="exports/clientes_20251029.csv",
        metadata={
            "generated_by": "meu_script",
            "export_date": "2025-10-29",
            "department": "vendas"
        }
    )
    logger.info("✅ Arquivo com metadados enviado!")


def exemplo_download():
    """Download de arquivo do S3"""
    logger.info("Baixando arquivo do S3...")
    
    s3 = S3Client(bucket_name="meu-bucket")
    
    s3.download_file(
        s3_key="relatorios/2025/10/vendas.pdf",
        local_path="downloads/vendas.pdf"
    )
    logger.info("✅ Arquivo baixado!")


def exemplo_listar():
    """Listar arquivos de um prefixo"""
    logger.info("Listando arquivos no S3...")
    
    s3 = S3Client(bucket_name="meu-bucket")
    
    files = s3.list_files(prefix="relatorios/2025/10/")
    logger.info(f"📁 {len(files)} arquivo(s) encontrado(s):")
    for file in files:
        logger.info(f"  - {file}")


def exemplo_deletar():
    """Deletar arquivo do S3"""
    logger.info("Deletando arquivo...")
    
    s3 = S3Client(bucket_name="meu-bucket")
    
    s3.delete_file(s3_key="temp/arquivo_temporario.txt")
    logger.info("🗑️  Arquivo deletado!")


def exemplo_url_assinada():
    """Gerar URL pré-assinada (compartilhar temporariamente)"""
    logger.info("Gerando URL pré-assinada...")
    
    s3 = S3Client(bucket_name="meu-bucket")
    
    url = s3.generate_presigned_url(
        s3_key="relatorios/vendas.pdf",
        expiration=3600  # 1 hora
    )
    logger.info(f"🔗 URL: {url}")


# ====================================================================
# EXECUTAR EXEMPLOS
# ====================================================================

if __name__ == "__main__":
    logger.info("=== Exemplo AWS S3 ===")
    
    # Descomente para testar (configure .env antes!):
    # exemplo_upload()
    # exemplo_upload_com_metadata()
    # exemplo_download()
    # exemplo_listar()
    # exemplo_deletar()
    # exemplo_url_assinada()
    
    logger.info("✅ Exemplos concluídos!")
