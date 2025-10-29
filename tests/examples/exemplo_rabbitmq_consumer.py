"""
Exemplo de uso do RabbitMQ - Consumer (Consumidor)
"""
from automacoes_python_base_td import RabbitMQConsumer, consume_messages, logger
from dotenv import load_dotenv
import json

load_dotenv()

logger.info("=== Exemplo de RabbitMQ Consumer ===")

# Configurações
QUEUE_NAME = "fila_exemplo"

# Forma 1: Usando a classe RabbitMQConsumer
consumer = RabbitMQConsumer()

# Conectar
consumer.connect()

# Callback para processar mensagens
def processar_mensagem(ch, method, properties, body):
    """Função callback que processa cada mensagem recebida"""
    try:
        # Decodificar a mensagem
        mensagem = json.loads(body.decode('utf-8'))
        logger.info(f"Mensagem recebida: {mensagem}")
        
        # Processar a mensagem
        logger.info(f"Processando mensagem ID: {mensagem.get('id')}")
        
        # Fazer algo com a mensagem...
        # ...
        
        # Confirmar o processamento (ACK)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.success("Mensagem processada com sucesso!")
        
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {e}")
        # Rejeitar a mensagem (NACK)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

# Consumir mensagens
logger.info(f"Aguardando mensagens da fila '{QUEUE_NAME}'...")
logger.info("Pressione CTRL+C para parar")

try:
    # Iniciar consumo (fica em loop infinito)
    # consumer.consume(QUEUE_NAME, callback=processar_mensagem)
    pass
except KeyboardInterrupt:
    logger.warning("Consumo interrompido pelo usuário")
    consumer.close()
    logger.info("Conexão fechada")

# Forma 2: Usando função direta com callback
logger.info("\n=== Usando função direta ===")

def callback_simples(ch, method, properties, body):
    mensagem = body.decode('utf-8')
    logger.info(f"Mensagem recebida: {mensagem}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

try:
    # consume_messages(queue=QUEUE_NAME, callback=callback_simples)
    pass
except KeyboardInterrupt:
    logger.warning("Consumo finalizado")

logger.info("Exemplo de consumer concluído!")

