"""
RabbitMQ Publisher
"""
import json
from typing import Optional, Any
import pika
from .connection import RabbitMQConnection


class RabbitMQPublisher(RabbitMQConnection):
    """
    Publisher para enviar mensagens ao RabbitMQ
    """
    
    def declare_queue(
        self,
        queue_name: str,
        durable: bool = True,
        auto_delete: bool = False,
    ) -> bool:
        """Declara uma fila"""
        try:
            self.channel.queue_declare(
                queue=queue_name,
                durable=durable,
                auto_delete=auto_delete,
            )
            return True
        except Exception as e:
            print(f"Erro ao declarar fila: {e}")
            return False
    
    def declare_exchange(
        self,
        exchange_name: str,
        exchange_type: str = "direct",
        durable: bool = True,
    ) -> bool:
        """Declara uma exchange"""
        try:
            self.channel.exchange_declare(
                exchange=exchange_name,
                exchange_type=exchange_type,
                durable=durable,
            )
            return True
        except Exception as e:
            print(f"Erro ao declarar exchange: {e}")
            return False
    
    def publish(
        self,
        message: Any,
        queue_name: Optional[str] = None,
        exchange: str = "",
        routing_key: Optional[str] = None,
        properties: Optional[pika.BasicProperties] = None,
        ensure_queue: bool = True,
    ) -> bool:
        """
        Publica uma mensagem.
        
        Exemplo:
            pub = RabbitMQPublisher()
            pub.connect()
            pub.publish({"name": "João"}, queue_name="users")
        """
        try:
            if routing_key is None:
                routing_key = queue_name or ""
            
            if ensure_queue and queue_name:
                self.declare_queue(queue_name)
            
            if isinstance(message, (dict, list)):
                body = json.dumps(message)
            else:
                body = str(message)
            
            if properties is None:
                properties = pika.BasicProperties(
                    delivery_mode=2,
                    content_type="application/json",
                )
            
            self.channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=body,
                properties=properties,
            )
            
            return True
        except Exception as e:
            print(f"Erro ao publicar mensagem: {e}")
            return False
    
    def publish_batch(
        self,
        messages: list,
        queue_name: str,
        exchange: str = "",
    ) -> int:
        """Publica múltiplas mensagens"""
        success_count = 0
        for message in messages:
            if self.publish(message, queue_name=queue_name, exchange=exchange):
                success_count += 1
        return success_count


def publish_message(message: Any, queue_name: str) -> bool:
    """Helper para publicar mensagem rapidamente"""
    with RabbitMQPublisher() as publisher:
        publisher.connect()
        return publisher.publish(message, queue_name=queue_name)

