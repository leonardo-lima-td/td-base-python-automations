"""
Exemplo da Nova Estrutura Modular
Demonstra o uso de todas as funcionalidades organizadas
"""

# =============================================================================
# 1. SETTINGS COM PYDANTIC
# =============================================================================

def exemplo_pydantic_settings():
    """Exemplo de uso do Pydantic Settings"""
    from automacoes_python_base_td import DatabaseSettings, AWSSettings
    
    # Carregar settings do .env automaticamente
    db_settings = DatabaseSettings()
    print(f"Database Host: {db_settings.db_host}")
    print(f"Database URL: {db_settings.postgres_url}")
    
    aws_settings = AWSSettings()
    print(f"AWS Region: {aws_settings.aws_region}")


def exemplo_custom_settings():
    """Exemplo de settings personalizadas"""
    from automacoes_python_base_td import BaseAppSettings
    from pydantic import Field
    
    class MyAppSettings(BaseAppSettings):
        """Settings personalizadas da sua aplicação"""
        api_key: str = Field(..., env="API_KEY", description="Chave da API")
        max_retries: int = Field(3, env="MAX_RETRIES")
        timeout: int = Field(30, env="TIMEOUT")
    
    # Usa .env automaticamente
    # settings = MyAppSettings()
    # print(f"API Key: {settings.api_key}")
    print("Settings personalizadas criadas!")


# =============================================================================
# 2. DATABASE COM CRUD PLUG AND PLAY
# =============================================================================

def exemplo_crud_generico():
    """Exemplo de CRUD genérico (funciona com qualquer model!)"""
    from automacoes_python_base_td import (
        init_db,
        BaseModel,
        get_session,
        crud_factory,
    )
    from sqlalchemy import Column, String, Integer, Boolean
    
    # Definir models
    class Product(BaseModel):
        __tablename__ = "products"
        
        name = Column(String(100), nullable=False)
        price = Column(Integer, nullable=False)
        stock = Column(Integer, default=0)
    
    class User(BaseModel):
        __tablename__ = "users"
        
        name = Column(String(100))
        email = Column(String(100), unique=True)
        active = Column(Boolean, default=True)
    
    # Inicializar database
    # init_db(create_tables=True)
    
    # Criar CRUDs (plug and play!)
    product_crud = crud_factory(Product)
    user_crud = crud_factory(User)
    
    # Usar CRUD de Product
    with get_session() as session:
        # CREATE
        product = product_crud.create(session, {
            "name": "Notebook Dell",
            "price": 3500,
            "stock": 10
        })
        print(f"Produto criado: {product.name}")
        
        # READ
        products = product_crud.get_all(session, limit=10)
        product = product_crud.get(session, id=1)
        products_filtered = product_crud.filter(session, price=3500)
        
        # UPDATE
        updated = product_crud.update(session, 1, {"price": 3200})
        
        # DELETE
        deleted = product_crud.delete(session, 1)
        
        # COUNT
        total = product_crud.count(session)
        expensive = product_crud.count(session, price=3000)
        
        # EXISTS
        exists = product_crud.exists(session, id=1)
    
    # Usar CRUD de User
    with get_session() as session:
        user = user_crud.create(session, {
            "name": "João Silva",
            "email": "joao@example.com"
        })
        print(f"Usuário criado: {user.name}")


def exemplo_queries_personalizadas():
    """Exemplo de queries personalizadas"""
    from automacoes_python_base_td import get_session, BaseModel
    from sqlalchemy import Column, String, Integer
    
    class Product(BaseModel):
        __tablename__ = "products"
        name = Column(String(100))
        price = Column(Integer)
        stock = Column(Integer)
    
    with get_session() as session:
        # Query personalizada
        products_in_stock = session.query(Product).filter(
            Product.stock > 0
        ).all()
        
        # Query com múltiplos filtros
        expensive_available = session.query(Product).filter(
            Product.price >= 1000,
            Product.stock > 0
        ).all()
        
        # Agregar
        from sqlalchemy import func
        total_stock = session.query(func.sum(Product.stock)).scalar()
        avg_price = session.query(func.avg(Product.price)).scalar()


# =============================================================================
# 3. UTILS DE ARQUIVOS
# =============================================================================

def exemplo_file_utils():
    """Exemplo de utilitários de arquivos"""
    from automacoes_python_base_td import (
        listdir,
        exists,
        getsize,
        create_dir,
        write_file,
        read_file,
        isfile,
        isdir,
    )
    
    # Listar arquivos
    files = listdir(".", filter_ext=".py")
    print(f"Arquivos Python: {len(files)}")
    
    # Verificar existência
    if exists("README.md"):
        size = getsize("README.md")
        print(f"README.md: {size / 1024:.2f} KB")
    
    # Criar diretório e arquivo
    create_dir("/tmp/test_dir")
    write_file("/tmp/test_dir/test.txt", "Hello World!")
    
    # Ler arquivo
    content = read_file("/tmp/test_dir/test.txt")
    print(f"Conteúdo: {content}")
    
    # Verificar tipo
    print(f"É arquivo? {isfile('/tmp/test_dir/test.txt')}")
    print(f"É diretório? {isdir('/tmp/test_dir')}")


# =============================================================================
# 4. UTILS DE STRING E DATA
# =============================================================================

def exemplo_string_date_utils():
    """Exemplo de utils de string e data"""
    from automacoes_python_base_td import (
        slugify,
        truncate,
        capitalize_words,
        format_timestamp,
        parse_date,
        days_between,
    )
    from datetime import datetime
    
    # String utils
    slug = slugify("Hello World! 123")
    print(f"Slug: {slug}")  # "hello-world-123"
    
    short_text = truncate("Este é um texto muito longo para exibir", 20)
    print(f"Truncado: {short_text}")
    
    title = capitalize_words("hello world from python")
    print(f"Capitalizado: {title}")
    
    # Date utils
    timestamp = format_timestamp()
    print(f"Timestamp: {timestamp}")
    
    date_only = format_timestamp(format="%Y-%m-%d")
    print(f"Data: {date_only}")
    
    parsed = parse_date("2025-10-28")
    print(f"Data parseada: {parsed}")
    
    d1 = datetime(2025, 10, 1)
    d2 = datetime(2025, 10, 28)
    days = days_between(d1, d2)
    print(f"Dias entre datas: {days}")


# =============================================================================
# 5. AWS (ESTRUTURA ORGANIZADA)
# =============================================================================

def exemplo_aws_modular():
    """Exemplo de uso dos clients AWS organizados"""
    from automacoes_python_base_td.aws import S3Client, CloudWatchClient
    
    # S3
    s3 = S3Client()
    # s3.upload_file("/path/file.csv", "bucket", "data/file.csv")
    # files = s3.list_files("bucket", prefix="data/")
    print("S3Client pronto!")
    
    # CloudWatch
    cw = CloudWatchClient()
    # cw.put_log_events("log-group", "stream", ["Log 1", "Log 2"])
    print("CloudWatchClient pronto!")


# =============================================================================
# 6. EXEMPLO COMPLETO - INTEGRANDO TUDO
# =============================================================================

def exemplo_completo():
    """Exemplo integrando todas as funcionalidades"""
    from automacoes_python_base_td import (
        logger,
        DatabaseSettings,
        init_db,
        BaseModel,
        get_session,
        crud_factory,
        write_file,
        format_timestamp,
    )
    from sqlalchemy import Column, String, Integer
    import json
    
    logger.info("Iniciando processamento completo")
    
    # 1. Carregar configurações
    db_settings = DatabaseSettings()
    logger.info(f"Conectando ao database: {db_settings.db_host}")
    
    # 2. Definir model
    class Order(BaseModel):
        __tablename__ = "orders"
        order_number = Column(String(50))
        customer_name = Column(String(100))
        total = Column(Integer)
    
    # 3. Inicializar database
    # init_db(settings=db_settings, create_tables=True)
    logger.info("Database inicializado")
    
    # 4. Criar CRUD
    order_crud = crud_factory(Order)
    
    # 5. Processar pedido
    order_data = {
        "order_number": "ORD-001",
        "customer_name": "João Silva",
        "total": 350
    }
    
    try:
        # Salvar no banco
        with get_session() as session:
            order = order_crud.create(session, order_data)
            logger.success(f"Pedido {order.order_number} salvo no banco")
        
        # Exportar para arquivo
        timestamp = format_timestamp(format="%Y%m%d_%H%M%S")
        filename = f"/tmp/order_{timestamp}.json"
        write_file(filename, json.dumps(order_data, indent=2))
        logger.info(f"Pedido exportado para {filename}")
        
        # Upload para S3 (exemplo)
        # from automacoes_python_base_td.aws import S3Client
        # s3 = S3Client()
        # s3.upload_file(filename, "bucket", f"orders/{timestamp}.json")
        # logger.info("Pedido enviado para S3")
        
        # Publicar evento (exemplo)
        # from automacoes_python_base_td import publish_message
        # publish_message({"event": "order_created", "order_id": order.id}, "orders")
        # logger.info("Evento publicado no RabbitMQ")
        
        logger.success("Processamento completo concluído!")
        
    except Exception as e:
        logger.exception(f"Erro no processamento: {e}")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("EXEMPLOS DA ESTRUTURA MODULAR")
    print("=" * 70)
    print()
    
    # Descomente os exemplos que deseja executar
    
    print("1. Pydantic Settings")
    # exemplo_pydantic_settings()
    # exemplo_custom_settings()
    print()
    
    print("2. CRUD Genérico (Plug and Play)")
    # exemplo_crud_generico()
    # exemplo_queries_personalizadas()
    print()
    
    print("3. File Utils")
    exemplo_file_utils()
    print()
    
    print("4. String e Date Utils")
    exemplo_string_date_utils()
    print()
    
    print("5. AWS Modular")
    # exemplo_aws_modular()
    print()
    
    print("6. Exemplo Completo")
    # exemplo_completo()
    print()
    
    print("=" * 70)
    print("✓ Exemplos executados com sucesso!")
    print("=" * 70)
    print()
    print("Veja ESTRUTURA_MODULAR.md para mais detalhes!")

