"""
Exemplos avançados de uso com AWS, SQLAlchemy, Loguru e RabbitMQ
"""

# =============================================================================
# AWS S3 - Exemplos
# =============================================================================

def exemplo_s3_upload_download():
    """Exemplo de upload e download com S3"""
    from automacoes_python_base_td import S3Client
    
    s3 = S3Client()
    
    # Upload de arquivo
    success = s3.upload_file(
        file_path="/path/to/local/file.csv",
        bucket="meu-bucket",
        key="data/file.csv",
        metadata={"tipo": "relatorio", "data": "2025-10-28"}
    )
    print(f"Upload: {'✓' if success else '✗'}")
    
    # Download de arquivo
    success = s3.download_file(
        bucket="meu-bucket",
        key="data/file.csv",
        file_path="/path/to/download/file.csv"
    )
    print(f"Download: {'✓' if success else '✗'}")
    
    # Upload de bytes (útil para dados em memória)
    import json
    data = {"usuarios": [{"nome": "João", "idade": 30}]}
    json_bytes = json.dumps(data).encode('utf-8')
    
    s3.upload_bytes(
        data=json_bytes,
        bucket="meu-bucket",
        key="data/usuarios.json",
        content_type="application/json"
    )
    
    # Download de bytes
    content = s3.download_bytes("meu-bucket", "data/usuarios.json")
    if content:
        data = json.loads(content.decode('utf-8'))
        print(data)
    
    # Listar arquivos
    files = s3.list_files("meu-bucket", prefix="data/")
    print(f"Arquivos encontrados: {len(files)}")
    for file in files:
        print(f"  - {file}")
    
    # Verificar se arquivo existe
    exists = s3.file_exists("meu-bucket", "data/file.csv")
    print(f"Arquivo existe: {exists}")


def exemplo_s3_helper():
    """Exemplo usando funções helper de S3"""
    from automacoes_python_base_td import upload_to_s3, download_from_s3
    
    # Upload rápido
    upload_to_s3("/path/file.csv", "meu-bucket", "data/file.csv")
    
    # Download rápido
    download_from_s3("meu-bucket", "data/file.csv", "/path/download.csv")


# =============================================================================
# AWS CloudWatch - Exemplos
# =============================================================================

def exemplo_cloudwatch():
    """Exemplo de envio de logs para CloudWatch"""
    from automacoes_python_base_td import CloudWatchClient
    
    cw = CloudWatchClient()
    
    # Criar log group e stream
    cw.create_log_group("minha-aplicacao")
    cw.create_log_stream("minha-aplicacao", "stream-producao")
    
    # Enviar logs
    mensagens = [
        "Aplicação iniciada",
        "Conectado ao banco de dados",
        "Processamento iniciado",
    ]
    
    cw.put_log_events("minha-aplicacao", "stream-producao", mensagens)
    
    # Buscar logs
    from datetime import datetime, timedelta
    start = datetime.now() - timedelta(hours=1)
    logs = cw.get_log_events(
        "minha-aplicacao",
        "stream-producao",
        start_time=start,
        limit=100
    )
    
    for log in logs:
        print(f"{log['timestamp']}: {log['message']}")


def exemplo_cloudwatch_helper():
    """Exemplo usando helper de CloudWatch"""
    from automacoes_python_base_td import send_logs_to_cloudwatch
    
    send_logs_to_cloudwatch(
        log_group="minha-app",
        log_stream="producao",
        messages=["Log 1", "Log 2", "Log 3"]
    )


# =============================================================================
# SQLAlchemy - Exemplos
# =============================================================================

def exemplo_sqlalchemy_setup():
    """Exemplo de setup do SQLAlchemy"""
    from automacoes_python_base_td import init_db, Base
    from sqlalchemy import Column, String, Integer, Boolean
    
    # Definir models
    class User(Base):
        __tablename__ = "users"
        
        id = Column(Integer, primary_key=True)
        name = Column(String(100), nullable=False)
        email = Column(String(100), unique=True)
        active = Column(Boolean, default=True)
        
        def __repr__(self):
            return f"<User(id={self.id}, name='{self.name}')>"
    
    # Inicializar banco e criar tabelas
    init_db(
        database_url="postgresql://user:pass@localhost:5432/mydb",
        echo=True,  # Mostra SQL queries
        create_tables=True  # Cria as tabelas automaticamente
    )


def exemplo_sqlalchemy_crud():
    """Exemplo de operações CRUD com SQLAlchemy"""
    from automacoes_python_base_td import get_session, Base
    from sqlalchemy import Column, String, Integer
    
    # Model
    class Product(Base):
        __tablename__ = "products"
        
        id = Column(Integer, primary_key=True)
        name = Column(String(100))
        price = Column(Integer)
    
    # CREATE
    with get_session() as session:
        product = Product(name="Notebook", price=3500)
        session.add(product)
        # commit automático ao sair do bloco
    
    # READ
    with get_session() as session:
        # Buscar todos
        products = session.query(Product).all()
        
        # Buscar por ID
        product = session.query(Product).filter_by(id=1).first()
        
        # Buscar com filtros
        expensive = session.query(Product).filter(Product.price > 2000).all()
    
    # UPDATE
    with get_session() as session:
        product = session.query(Product).filter_by(id=1).first()
        if product:
            product.price = 3200
        # commit automático
    
    # DELETE
    with get_session() as session:
        product = session.query(Product).filter_by(id=1).first()
        if product:
            session.delete(product)


def exemplo_sqlalchemy_basemodel():
    """Exemplo usando BaseModel (com created_at e updated_at)"""
    from automacoes_python_base_td import BaseModel, get_session
    from sqlalchemy import Column, String
    
    class Customer(BaseModel):  # Herda id, created_at, updated_at
        __tablename__ = "customers"
        
        name = Column(String(100))
        email = Column(String(100))
    
    with get_session() as session:
        customer = Customer(name="João", email="joao@example.com")
        session.add(customer)
    
    # created_at e updated_at são preenchidos automaticamente!


# =============================================================================
# Loguru - Exemplos
# =============================================================================

def exemplo_logger_basico():
    """Exemplo básico de logging com Loguru"""
    from automacoes_python_base_td import logger
    
    logger.debug("Mensagem de debug")
    logger.info("Mensagem informativa")
    logger.warning("Aviso")
    logger.error("Erro ocorreu")
    logger.critical("Erro crítico!")
    
    # Log com contexto
    user_id = 123
    logger.info(f"Usuário {user_id} fez login")
    
    # Log de exceção
    try:
        resultado = 10 / 0
    except Exception as e:
        logger.exception("Erro ao calcular")  # Inclui stack trace


def exemplo_logger_configurado():
    """Exemplo de configuração personalizada do logger"""
    from automacoes_python_base_td import setup_logger, logger
    
    # Configurar logger com arquivo
    setup_logger(
        log_file="app.log",
        log_level="DEBUG",
        rotation="50 MB",  # Rotaciona quando arquivo atingir 50MB
        retention="7 days",  # Mantém logs por 7 dias
    )
    
    logger.info("Logger configurado!")
    
    # Logs JSON (útil para análise)
    setup_logger(
        log_file="app_json.log",
        serialize=True,  # Formato JSON
    )


def exemplo_logger_com_contexto():
    """Exemplo de logging com contexto adicional"""
    from automacoes_python_base_td import logger
    
    # Adicionar contexto
    with logger.contextualize(request_id="abc-123", user="joao"):
        logger.info("Processando requisição")
        logger.info("Salvando no banco")
    
    # Bind permanente
    log = logger.bind(service="api", version="1.0")
    log.info("API iniciada")


# =============================================================================
# RabbitMQ - Exemplos
# =============================================================================

def exemplo_rabbitmq_publisher():
    """Exemplo de publicação de mensagens no RabbitMQ"""
    from automacoes_python_base_td import RabbitMQPublisher
    
    publisher = RabbitMQPublisher()
    publisher.connect()
    
    # Publicar mensagem simples
    publisher.publish(
        message={"user_id": 123, "action": "login"},
        queue_name="events"
    )
    
    # Publicar múltiplas mensagens
    mensagens = [
        {"tipo": "email", "para": "joao@example.com"},
        {"tipo": "sms", "para": "+5511999999999"},
    ]
    count = publisher.publish_batch(mensagens, queue_name="notifications")
    print(f"{count} mensagens publicadas")
    
    # Com exchange e routing key
    publisher.declare_exchange("logs", exchange_type="topic")
    publisher.publish(
        message="Erro ao processar",
        exchange="logs",
        routing_key="error.database"
    )
    
    publisher.close()


def exemplo_rabbitmq_consumer():
    """Exemplo de consumo de mensagens do RabbitMQ"""
    from automacoes_python_base_td import RabbitMQConsumer
    import json
    
    def processar_mensagem(ch, method, properties, body):
        """Callback para processar mensagem"""
        try:
            data = json.loads(body)
            print(f"Processando: {data}")
            
            # Simular processamento
            # ... seu código aqui ...
            
            # Confirmar processamento (ACK)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except Exception as e:
            print(f"Erro ao processar: {e}")
            # Rejeitar e não reenviar (NACK)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    
    consumer = RabbitMQConsumer()
    consumer.connect()
    
    # Consumir mensagens continuamente
    consumer.consume(
        queue_name="events",
        callback=processar_mensagem,
        auto_ack=False,  # Manual ACK
        prefetch_count=1  # Processar 1 por vez
    )


def exemplo_rabbitmq_get_one():
    """Exemplo de buscar uma mensagem por vez (não-bloqueante)"""
    from automacoes_python_base_td import RabbitMQConsumer
    import json
    
    consumer = RabbitMQConsumer()
    consumer.connect()
    
    # Buscar uma mensagem
    msg = consumer.get_message("events", auto_ack=False)
    
    if msg:
        data = json.loads(msg['body'])
        print(f"Mensagem: {data}")
        
        # Processar...
        
        # Confirmar
        consumer.ack_message(msg['method'].delivery_tag)
    else:
        print("Fila vazia")
    
    consumer.close()


def exemplo_rabbitmq_helper():
    """Exemplo usando funções helper do RabbitMQ"""
    from automacoes_python_base_td import publish_message, consume_messages
    import json
    
    # Publicar rapidamente
    publish_message(
        message={"evento": "usuario_criado", "id": 123},
        queue_name="events"
    )
    
    # Consumir (bloqueante)
    def callback(ch, method, properties, body):
        data = json.loads(body)
        print(f"Recebido: {data}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    consume_messages("events", callback)


# =============================================================================
# Exemplo Completo - Integração de Tudo
# =============================================================================

def exemplo_completo_integracao():
    """Exemplo integrando todas as funcionalidades"""
    from automacoes_python_base_td import (
        logger, setup_logger,
        get_session, BaseModel,
        S3Client,
        RabbitMQPublisher,
        send_logs_to_cloudwatch,
    )
    from sqlalchemy import Column, String, Integer
    import json
    
    # 1. Configurar logger
    setup_logger(log_file="app.log", log_level="INFO")
    logger.info("Aplicação iniciada")
    
    # 2. Definir model
    class Order(BaseModel):
        __tablename__ = "orders"
        
        order_number = Column(String(50))
        customer_name = Column(String(100))
        total = Column(Integer)
    
    # 3. Processar pedido
    order_data = {"order_number": "ORD-001", "customer_name": "João", "total": 150}
    
    try:
        # Salvar no banco
        with get_session() as session:
            order = Order(**order_data)
            session.add(order)
            logger.info(f"Pedido {order.order_number} salvo no banco")
        
        # Fazer upload para S3
        s3 = S3Client()
        order_json = json.dumps(order_data).encode('utf-8')
        s3.upload_bytes(
            data=order_json,
            bucket="pedidos-bucket",
            key=f"pedidos/{order_data['order_number']}.json",
            content_type="application/json"
        )
        logger.info(f"Pedido enviado para S3")
        
        # Publicar evento no RabbitMQ
        publisher = RabbitMQPublisher()
        publisher.connect()
        publisher.publish(
            message={"evento": "pedido_criado", "order_number": order_data['order_number']},
            queue_name="order_events"
        )
        publisher.close()
        logger.info(f"Evento publicado no RabbitMQ")
        
        # Enviar logs para CloudWatch
        send_logs_to_cloudwatch(
            "minha-aplicacao",
            "pedidos",
            [f"Pedido {order_data['order_number']} processado com sucesso"]
        )
        
        logger.success("Pedido processado completamente!")
        
    except Exception as e:
        logger.exception(f"Erro ao processar pedido: {e}")
        raise


if __name__ == "__main__":
    print("=" * 60)
    print("EXEMPLOS AVANÇADOS - automacoes-python-base-td")
    print("=" * 60)
    
    # Descomente os exemplos que deseja executar
    
    # AWS S3
    # exemplo_s3_upload_download()
    # exemplo_s3_helper()
    
    # AWS CloudWatch
    # exemplo_cloudwatch()
    # exemplo_cloudwatch_helper()
    
    # SQLAlchemy
    # exemplo_sqlalchemy_setup()
    # exemplo_sqlalchemy_crud()
    # exemplo_sqlalchemy_basemodel()
    
    # Loguru
    # exemplo_logger_basico()
    # exemplo_logger_configurado()
    # exemplo_logger_com_contexto()
    
    # RabbitMQ
    # exemplo_rabbitmq_publisher()
    # exemplo_rabbitmq_consumer()
    # exemplo_rabbitmq_get_one()
    # exemplo_rabbitmq_helper()
    
    # Integração completa
    # exemplo_completo_integracao()
    
    print("\nVeja o código fonte deste arquivo para mais detalhes!")

