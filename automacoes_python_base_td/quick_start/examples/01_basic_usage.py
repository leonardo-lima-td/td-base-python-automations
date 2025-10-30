"""
EXEMPLO 1: USO BÁSICO
======================

Primeiro script usando o pacote automacoes-python-base-td.

ANTES DE EXECUTAR:
1. Instale o pacote: pip install automacoes-python-base-td
2. Crie um arquivo .env na raiz do seu projeto
3. Configure as variáveis: APP_NAME, ENV, DEBUG_MODE, etc
"""

# Importar o pacote (já instalado via pip)
from automacoes_python_base_td import settings
from automacoes_python_base_td.logger import get_logger

# Configurar logger
logger = get_logger()

# Acessar configurações do seu .env
logger.info(f"🚀 Aplicação: {settings.app_name}")
logger.info(f"🌍 Ambiente: {settings.env}")
logger.info(f"🐛 Debug Mode: {settings.debug_mode}")
logger.info(f"💾 Database: {settings.db_name}")

# Verificar ambiente
if settings.is_production():
    logger.warning("⚠️  ATENÇÃO: Rodando em PRODUÇÃO!")
elif settings.is_development():
    logger.info("🔧 Ambiente de DESENVOLVIMENTO")
else:
    logger.info(f"🔧 Ambiente: {settings.env.upper()}")

# Informações úteis
logger.info(f"📊 Log Level: {settings.effective_log_level}")
logger.info(f"☁️  CloudWatch: {settings.use_cloudwatch}")

# Pronto! Agora você pode usar o pacote em seu projeto
logger.info("✅ Pacote configurado e funcionando!")
