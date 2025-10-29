"""
EXEMPLO 5: RabbitMQ
===================

Como publicar e consumir mensagens usando RabbitMQ.

PRÉ-REQUISITOS:
- Pacote instalado: pip install automacoes-python-base-td
- RabbitMQ rodando
- Variáveis no .env: RABBIT_USAGE=true, RABBITMQ_HOST, RABBITMQ_PORT, etc
"""

import json
from automacoes_python_base_td.rabbitmq import RabbitMQPublisher, RabbitMQConsumer
from automacoes_python_base_td.logger import get_logger

logger = get_logger()

# ====================================================================
# PUBLICAR MENSAGENS
# ====================================================================

def exemplo_publicar():
    """Publicar mensagem na fila"""
    logger.info("Publicando mensagem...")
    
    publisher = RabbitMQPublisher()
    
    # Sua mensagem
    message = {
        "tipo": "pedido_criado",
        "pedido_id": 12345,
        "cliente_id": 678,
        "valor": 1500.00
    }
    
    publisher.publish(
        queue_name="pedidos_novos",
        message=json.dumps(message)
    )
    logger.info("✅ Mensagem publicada!")
    
    publisher.close()


# ====================================================================
# CONSUMIR MENSAGENS
# ====================================================================

def processar_pedido(ch, method, properties, body):
    """
    Função callback chamada para cada mensagem recebida.
    
    IMPORTANTE: Confirme (ACK) após processar com sucesso!
    """
    try:
        # Parsear mensagem
        pedido = json.loads(body)
        logger.info(f"🔔 Novo pedido: #{pedido['pedido_id']}")
        logger.info(f"   Cliente: {pedido['cliente_id']}")
        logger.info(f"   Valor: R$ {pedido['valor']:.2f}")
        
        # Processar pedido aqui...
        # ...
        
        # Confirmar processamento (ACK)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.info("✅ Pedido processado!")
        
    except Exception as e:
        logger.error(f"❌ Erro ao processar: {e}")
        # Rejeitar mensagem (volta para fila)
        ch.basic_nack(delivery_tag=method.delivery_tag)


def exemplo_consumir():
    """
    Consumir mensagens da fila.
    ATENÇÃO: Este script fica rodando até você parar (Ctrl+C)
    """
    logger.info("Iniciando consumer...")
    
    consumer = RabbitMQConsumer()
    consumer.consume(
        queue_name="pedidos_novos",
        callback=processar_pedido
    )
    
    logger.info("🎧 Aguardando mensagens... (Ctrl+C para parar)")


# ====================================================================
# SISTEMA COMPLETO: Notificações
# ====================================================================

def enviar_notificacao(destinatario, assunto, mensagem):
    """Envia notificação via RabbitMQ"""
    logger.info(f"Enviando notificação para {destinatario}...")
    
    pub = RabbitMQPublisher()
    
    notificacao = {
        "tipo": "email",
        "destinatario": destinatario,
        "assunto": assunto,
        "mensagem": mensagem
    }
    
    pub.publish("notificacoes", json.dumps(notificacao))
    pub.close()
    
    logger.info("✅ Notificação enviada!")


def processar_notificacao(ch, method, properties, body):
    """Processa notificações"""
    try:
        dados = json.loads(body)
        logger.info(f"📧 Enviando email...")
        logger.info(f"   Para: {dados['destinatario']}")
        logger.info(f"   Assunto: {dados['assunto']}")
        
        # Enviar email aqui...
        # ...
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        logger.error(f"Erro: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)


def worker_notificacoes():
    """Worker que processa notificações"""
    consumer = RabbitMQConsumer()
    consumer.consume("notificacoes", processar_notificacao)


# ====================================================================
# EXECUTAR EXEMPLOS
# ====================================================================

if __name__ == "__main__":
    logger.info("=== Exemplo RabbitMQ ===")
    
    # Escolha um:
    
    # 1. Publicar mensagem
    # exemplo_publicar()
    
    # 2. Consumir mensagens (fica rodando)
    # exemplo_consumir()
    
    # 3. Sistema de notificações
    # enviar_notificacao("user@example.com", "Teste", "Olá!")
    # worker_notificacoes()
    
    logger.info("✅ Exemplo concluído!")
