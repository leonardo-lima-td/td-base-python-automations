"""
EXEMPLO 6: LOGGER
=================

Como usar o sistema de logs (Loguru).

PRÉ-REQUISITOS:
- Pacote instalado: pip install automacoes-python-base-td
- Variáveis no .env: LOG_LEVEL, DEBUG_MODE (opcional)
"""

from automacoes_python_base_td.logger import setup_logger, get_logger
import time

# Configurar logger (opcional, já é feito automaticamente)
setup_logger(log_level="INFO")

# Obter instância do logger
logger = get_logger()

class LoggerFunctions:
    """Funções de log"""
    def __init__(self):
        print("LoggerFunctions initialized\n")
    
    
    def __finally__(self):
        print("LoggerFunctions finally\n")


# ====================================================================
# NÍVEIS DE LOG
# ====================================================================

    def exemplo_niveis_log(self):
        """Diferentes níveis de severidade"""
        logger.debug("🔍 DEBUG - Informação técnica detalhada")
        logger.info("ℹ️  INFO - Informação geral do sistema")
        logger.warning("⚠️  WARNING - Alerta, algo pode dar errado")
        logger.error("❌ ERROR - Erro ocorreu!")
        logger.critical("🔥 CRITICAL - Erro crítico, sistema comprometido!")
        logger.success("✅ SUCCESS - Ação concluída com sucesso!")


# ====================================================================
# LOGS EM FUNÇÕES
# ====================================================================

    def processar_arquivo(self, arquivo):
        """Processa arquivo com logs"""
        logger.info(f"📂 Iniciando processamento: {arquivo}")
        
        try:
        # Simular processamento
            logger.debug(f"Lendo arquivo {arquivo}...")
            time.sleep(1)
            
            logger.debug("Validando dados...")
            time.sleep(1)
            
            logger.debug("Transformando dados...")
            time.sleep(1)
            
            logger.success(f"✅ Arquivo {arquivo} processado com sucesso!")
            return True
            
        except FileNotFoundError:
            logger.error(f"❌ Arquivo não encontrado: {arquivo}")
            raise
            
        except Exception as e:
            logger.critical(f"🔥 Erro crítico ao processar {arquivo}: {e}")
            raise


# ====================================================================
# LOGS COM CONTEXTO
# ====================================================================

    def processar_pedido(self, pedido_id, cliente_id, valor):
        """Processa pedido com contexto"""
        logger.info(f"🛒 Processando pedido #{pedido_id}")
        logger.debug(f"   Cliente: {cliente_id}")
        logger.debug(f"   Valor: R$ {valor:.2f}")
        
        try:
        # Validar
            logger.debug(f"Validando pedido #{pedido_id}...")
            if valor <= 0:
                raise ValueError("Valor inválido")
            
        # Processar pagamento
            logger.info(f"💳 Processando pagamento...")
            time.sleep(1)
            
        # Atualizar estoque
            logger.info(f"📦 Atualizando estoque...")
            time.sleep(1)
            
            logger.success(f"✅ Pedido #{pedido_id} concluído!")
            return True
            
        except ValueError as e:
            logger.warning(f"⚠️  Pedido #{pedido_id} inválido: {e}")
            return False
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar pedido #{pedido_id}: {e}")
            return False


# ====================================================================
# MEDIR TEMPO DE EXECUÇÃO
# ====================================================================

    def operacao_demorada(self):
        """Operação com log de tempo"""
        logger.info("⏱️  Iniciando operação demorada...")
        start = time.time()
        
    # Fazer algo...
        time.sleep(2)
        
        elapsed = time.time() - start
        logger.success(f"✅ Operação concluída em {elapsed:.2f}s")


# ====================================================================
# LOGS EM LOOP
# ====================================================================

    def processar_lote(self, items):
        """Processa lote de items"""
        total = len(items)
        logger.info(f"📋 Processando lote de {total} items...")
        
        for i, item in enumerate(items, 1):
            logger.debug(f"Processando item {i}/{total}: {item}")
        # Processar...
            time.sleep(0.1)
            
        # Log a cada 10 items
            if i % 10 == 0:
                logger.info(f"   ⏳ Progresso: {i}/{total} ({i/total*100:.0f}%)")
        
        logger.success(f"✅ Lote processado: {total} items")


# ====================================================================
# LOG DE ERRO COM STACK TRACE
# ====================================================================

    def funcao_com_erro(self):
        """Exemplo de log de erro com stack trace"""
        try:
        # Simular erro
            resultado = 10 / 0
        except ZeroDivisionError as e:
            logger.critical(f"❌ Erro de divisão: {e}", exc_info=True)
        # exc_info=True inclui o stack trace completo


# ====================================================================
# EXECUTAR EXEMPLOS
# ====================================================================

if __name__ == "__main__":
    logger_functions = LoggerFunctions()

    logger.info("=" * 50)
    logger.info("=== Exemplo de Logging ===")
    logger.info("=" * 50)
    
# 1. Níveis de log
    logger.info("📝 Testando níveis de log:")
    logger_functions.exemplo_niveis_log()
    
# 2. Processar arquivo
    logger.info("📂 Testando processamento de arquivo:")
    logger_functions.processar_arquivo("dados.csv")
    
# 3. Processar pedido
    logger.info("🛒 Testando processamento de pedido:")
    logger_functions.processar_pedido(12345, 678, 1500.00)
    
# 4. Operação demorada
    logger.info("⏱️  Testando medição de tempo:")
    logger_functions.operacao_demorada()
    
# 5. Processar lote
    logger.info("📋 Testando processamento em lote:")
    items = [f"item_{i}" for i in range(25)]
    logger_functions.processar_lote(items)
    
# 6. Erro com stack trace
    logger.info("❌ Testando erro com stack trace:")
    logger_functions.funcao_com_erro()
    
    logger.info("=" * 50)
    logger.success("✅ Todos os exemplos concluídos!")
    logger.info("=" * 50)
