"""
RabbitMQ Consumer
"""
from typing import Callable, Optional, Dict, Any
from .connection import RabbitMQConnection


class RabbitMQConsumer(RabbitMQConnection):
    """
    Consumer para consumir mensagens do RabbitMQ
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
    
    def consume(
        self,
        queue_name: str,
        callback: Callable,
        auto_ack: bool = False,
        prefetch_count: int = 1,
    ):
        """
        Inicia o consumo de mensagens.
        
        Exemplo:
            def processar_mensagem(ch, method, properties, body):
                data = json.loads(body)
                print(f"Recebido: {data}")
                ch.basic_ack(delivery_tag=method.delivery_tag)
            
            consumer = RabbitMQConsumer()
            consumer.connect()
            consumer.consume("users", processar_mensagem)
        """
        self.declare_queue(queue_name)
        self.channel.basic_qos(prefetch_count=prefetch_count)
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=auto_ack,
        )
        
        print(f" [*] Aguardando mensagens na fila '{queue_name}'. CTRL+C para sair.")
        
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
    
    def get_message(
        self,
        queue_name: str,
        auto_ack: bool = False,
    ) -> Optional[Dict[str, Any]]:
        """
        Obtém uma única mensagem da fila (não-bloqueante).
        
        Exemplo:
            consumer = RabbitMQConsumer()
            consumer.connect()
            msg = consumer.get_message("users")
            if msg:
                data = json.loads(msg['body'])
                consumer.ack_message(msg['method'].delivery_tag)
        """
        self.declare_queue(queue_name)
        
        method_frame, properties, body = self.channel.basic_get(
            queue=queue_name,
            auto_ack=auto_ack,
        )
        
        if method_frame:
            return {
                "method": method_frame,
                "properties": properties,
                "body": body.decode("utf-8"),
            }
        
        return None
    
    def ack_message(self, delivery_tag: int):
        """Confirma o recebimento de uma mensagem"""
        self.channel.basic_ack(delivery_tag=delivery_tag)
    
    def nack_message(self, delivery_tag: int, requeue: bool = True):
        """Rejeita uma mensagem"""
        self.channel.basic_nack(delivery_tag=delivery_tag, requeue=requeue)


def consume_messages(queue_name: str, callback: Callable):
    """Helper para consumir mensagens rapidamente"""
    consumer = RabbitMQConsumer()
    consumer.connect()
    consumer.consume(queue_name, callback)

