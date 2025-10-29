"""
Exemplo de uso do RabbitMQ - Publisher (Publicador)
"""
from automacoes_python_base_td import RabbitMQPublisher, publish_message, logger
from dotenv import load_dotenv
import json

load_dotenv()

logger.info("=== Exemplo de RabbitMQ Publisher ===")

# Configurações
QUEUE_NAME = "fila_exemplo"
EXCHANGE_NAME = "exchange_exemplo"
ROUTING_KEY = "exemplo.key"

# Forma 1: Usando a classe RabbitMQPublisher
publisher = RabbitMQPublisher()

# Conectar
publisher.connect()

# Publicar mensagem simples
mensagem = {
    "id": 1,
    "tipo": "processamento",
    "dados": "Exemplo de mensagem",
    "timestamp": "2025-10-29T10:00:00"
}

logger.info(f"Publicando mensagem: {mensagem}")
# publisher.publish(QUEUE_NAME, json.dumps(mensagem))
# logger.success("Mensagem publicada com sucesso!")

# Publicar mensagem em exchange com routing key
# publisher.publish_to_exchange(
#     exchange=EXCHANGE_NAME,
#     routing_key=ROUTING_KEY,
#     message=json.dumps(mensagem)
# )
# logger.success(f"Mensagem publicada no exchange {EXCHANGE_NAME}")

# Publicar múltiplas mensagens
for i in range(5):
    msg = {
        "id": i + 1,
        "mensagem": f"Mensagem número {i + 1}"
    }
    # publisher.publish(QUEUE_NAME, json.dumps(msg))
    logger.info(f"Mensagem {i + 1} publicada")

# Fechar conexão
publisher.close()
logger.success("Conexão fechada!")

# Forma 2: Usando função direta
logger.info("\n=== Usando função direta ===")

# publish_message(
#     queue=QUEUE_NAME,
#     message=json.dumps({"teste": "mensagem direta"})
# )
# logger.success("Mensagem publicada via função direta!")

logger.info("Publicação de mensagens concluída!")

