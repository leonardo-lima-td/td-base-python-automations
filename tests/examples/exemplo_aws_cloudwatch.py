"""
Exemplo de uso do AWS CloudWatch
"""
from automacoes_python_base_td import CloudWatchClient, send_logs_to_cloudwatch, logger
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

logger.info("=== Exemplo de uso do CloudWatch ===")

# Configurações
LOG_GROUP = "/aws/lambda/minha-aplicacao"
LOG_STREAM = f"execucao-{datetime.now().strftime('%Y-%m-%d')}"

# Forma 1: Usando a classe CloudWatchClient
cloudwatch = CloudWatchClient()

# Enviar log para CloudWatch
log_message = f"Aplicação iniciada em {datetime.now()}"
logger.info(f"Enviando log para CloudWatch: {log_message}")

# cloudwatch.send_log(LOG_GROUP, LOG_STREAM, log_message)
# logger.success("Log enviado para CloudWatch com sucesso!")

# Enviar múltiplos logs
logs = [
    f"[INFO] Processamento iniciado - {datetime.now()}",
    f"[INFO] Processando dados...",
    f"[SUCCESS] Processamento concluído - {datetime.now()}"
]

# for log in logs:
#     cloudwatch.send_log(LOG_GROUP, LOG_STREAM, log)
# logger.success(f"{len(logs)} logs enviados!")

# Forma 2: Usando função direta
logger.info("\n=== Usando função direta ===")

# send_logs_to_cloudwatch(
#     log_group=LOG_GROUP,
#     log_stream=LOG_STREAM,
#     message="Log enviado pela função direta"
# )
# logger.success("Log enviado via função direta!")

# Enviar métricas customizadas
# cloudwatch.put_metric(
#     namespace="MinhAplicacao",
#     metric_name="ProcessamentosConcluidos",
#     value=1,
#     unit="Count"
# )
# logger.success("Métrica enviada para CloudWatch!")

logger.info("Operações CloudWatch concluídas!")

