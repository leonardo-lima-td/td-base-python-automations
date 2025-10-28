"""
Testes para configuração do logger
Testa funcionalidade e configuração do Loguru
"""
import pytest
from unittest.mock import patch, MagicMock
from automacoes_python_base_td.logger.config import setup_logger, get_logger


class TestSetupLogger:
    """Testes para setup_logger"""
    
    @patch('automacoes_python_base_td.logger.config.logger')
    def test_setup_logger_basic(self, mock_logger):
        """Testa configuração básica do logger"""
        setup_logger(log_level="DEBUG")
        
        # Verifica que remove foi chamado (limpa handlers)
        mock_logger.remove.assert_called()
        
        # Verifica que add foi chamado (adiciona handler)
        mock_logger.add.assert_called()
    
    @patch('automacoes_python_base_td.logger.config.logger')
    def test_setup_logger_with_settings(self, mock_logger):
        """Testa configuração com objeto settings"""
        from automacoes_python_base_td.settings import LoggerSettings
        
        settings = LoggerSettings(log_level="WARNING")
        setup_logger(settings=settings)
        
        # Verifica que foi configurado
        mock_logger.add.assert_called()
    
    def test_get_logger_returns_instance(self):
        """Testa se get_logger retorna instância do logger"""
        logger = get_logger()
        
        assert logger is not None
        # Verifica se tem métodos do logger
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'error')
        assert hasattr(logger, 'warning')

