"""
Configuração do Loguru (apenas console)
"""
import os
import sys
from typing import Optional
from loguru import logger
from ..settings import settings


def setup_logger(
    log_level: Optional[str] = None,
    format_string: Optional[str] = None,
) -> None:
    """
    Configura o logger com Loguru (apenas console).
    
    Args:
        log_level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL). Se None, usa settings.effective_log_level
        format_string: Formato customizado do log
    
    Exemplo:
        setup_logger(log_level="DEBUG")
    """
    # Usa settings global se não fornecido
    if log_level is None:
        log_level = settings.effective_log_level
    if format_string is None and settings.log_format != "default":
        format_string = settings.log_format
    
    # Remove handlers padrão
    logger.remove()
    
    # Formato padrão
    if format_string is None:
        format_string = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )
    
    # Adiciona handler para console
    logger.add(
        sys.stderr,
        format=format_string,
        level=log_level,
        colorize=True,
        backtrace=True,
        diagnose=True,
    )


def get_logger():
    """
    Retorna a instância do logger.
    
    Exemplo:
        log = get_logger()
        log.info("Mensagem informativa")
        log.error("Erro ocorreu")
    """
    return logger


# Configuração automática com variável de ambiente
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    level=os.getenv("LOG_LEVEL", "INFO"),
    colorize=True,
)

