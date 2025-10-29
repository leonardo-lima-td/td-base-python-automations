"""
Exemplo de uso do Logger (Loguru)
"""
from automacoes_python_base_td import logger, setup_logger
from dotenv import load_dotenv

load_dotenv()

# Configurar o logger (opcional - já vem configurado por padrão)
setup_logger()

# Exemplos de uso
logger.info("Iniciando aplicação")
logger.debug("Mensagem de debug")
logger.warning("Atenção: algo pode estar errado")
logger.success("Operação concluída com sucesso!")

try:
    resultado = 10 / 2
    logger.info(f"Resultado da divisão: {resultado}")
except Exception as e:
    logger.error(f"Erro ao processar: {e}")
    logger.exception("Detalhes completos do erro:")

