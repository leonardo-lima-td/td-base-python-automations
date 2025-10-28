# 🚀 Quick Start

## Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/python-base-TD.git
cd python-base-TD

# Instale em modo desenvolvimento
pip install -e ".[dev]"
```

## Uso Básico

### 1. Exceções com Logging Automático

```python
from automacoes_python_base_td import DatabaseConnectionError

# Exceção emite log automaticamente
try:
    raise DatabaseConnectionError(
        "Falha ao conectar",
        details={"host": "localhost", "port": 5432}
    )
except DatabaseConnectionError as e:
    print(e.to_dict())  # {'error': 'DatabaseConnectionError', ...}
```

### 2. Conexão com PostgreSQL

```python
from automacoes_python_base_td import get_connection

with get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
```

### 3. CRUD Genérico (Plug & Play)

```python
from automacoes_python_base_td import crud_factory, get_tdax_session
from your_models import User

# Criar CRUD
user_crud = crud_factory(User)

# Usar
with get_tdax_session() as session:
    # Create
    user = user_crud.create(session, {"name": "João", "email": "joao@test.com"})
    
    # Read
    user = user_crud.get(session, id=1)
    users = user_crud.get_all(session)
    
    # Update
    user = user_crud.update(session, id=1, data={"name": "João Silva"})
    
    # Delete (soft delete - marca ativo=False)
    user_crud.delete(session, id=1)
```

### 4. Upload para S3

```python
from automacoes_python_base_td import S3Client

s3 = S3Client(
    aws_access_key_id="your-key",
    aws_secret_access_key="your-secret"
)

s3.upload_file(
    "/path/local/file.csv",
    "my-bucket",
    "uploads/file.csv"
)
```

### 5. RabbitMQ Publisher

```python
from automacoes_python_base_td import RabbitMQPublisher

publisher = RabbitMQPublisher(
    host="localhost",
    username="guest",
    password="guest"
)

publisher.connect()
publisher.publish_message("my_queue", {"task": "process_data"})
publisher.close()
```

### 6. Logger com Loguru

```python
from automacoes_python_base_td import setup_logger, get_logger

# Configurar
setup_logger(log_level="DEBUG")

# Usar
log = get_logger()
log.info("Aplicação iniciada")
log.error("Erro ocorreu")
```

### 7. Pydantic Settings

```python
from automacoes_python_base_td import DatabaseSettings

# Carrega de variáveis de ambiente (.env)
settings = DatabaseSettings()

print(settings.db_host)  # localhost
print(settings.db_port)  # 5432
print(settings.postgres_url)  # postgresql://...
```

### 8. Utilitários

```python
from automacoes_python_base_td import (
    # String utils
    slugify,
    truncate,
    capitalize_words,
    
    # Date utils
    format_timestamp,
    parse_date,
    days_between,
    
    # File utils
    listdir,
    exists,
    read_file,
)

# Exemplos
slug = slugify("Hello World!")  # "hello-world"
short = truncate("Long text...", 10)  # "Long te..."
date = format_timestamp()  # "2025-10-28 14:30:45"
```

## Build e Testes

```bash
# Build do pacote
./build.sh all

# Rodar testes
./run_tests.sh all

# Testes com cobertura
./run_tests.sh coverage
```

## Estrutura do Projeto

```
python-base-TD/
├── automacoes_python_base_td/  # Código-fonte
│   ├── core/                   # Exceções
│   ├── database/               # Database (PostgreSQL + SQLAlchemy)
│   ├── aws/                    # AWS (S3 + CloudWatch)
│   ├── rabbitmq/               # RabbitMQ
│   ├── logger/                 # Loguru
│   ├── settings/               # Pydantic Settings
│   └── utils/                  # Utilitários
├── tests/                      # Testes
├── docs/                       # Documentação
├── build.sh                    # Script de build
├── run_tests.sh                # Script de testes
└── README.md                   # Documentação principal
```

## Próximos Passos

1. ✅ Leia o [README.md](README.md) completo
2. ✅ Veja os exemplos em `example_*.py`
3. ✅ Configure suas variáveis de ambiente no `.env`
4. ✅ Crie seus modelos em `database/models/`
5. ✅ Use o CRUD genérico para operações no banco
6. ✅ Rode os testes com `./run_tests.sh all`

## Links Úteis

- **Repositório**: https://github.com/seu-usuario/python-base-TD
- **Documentação**: [docs/](docs/)
- **Issues**: https://github.com/seu-usuario/python-base-TD/issues

