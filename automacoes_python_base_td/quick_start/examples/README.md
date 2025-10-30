# 📚 Exemplos de Uso - automacoes-python-base-td

Exemplos práticos de como usar o pacote `automacoes-python-base-td` em seus projetos.

## 🚀 Antes de Começar

### 1. Instalar o pacote

```bash
# Via pip (quando publicado)
pip install automacoes-python-base-td

# Ou via Git
pip install git+https://github.com/seu-usuario/python-base-TD.git

# Ou arquivo .whl
pip install automacoes_python_base_td-0.1.0-py3-none-any.whl
```

### 2. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do seu projeto:

```bash
# Aplicação
APP_NAME=meu_projeto
ENV=dev
DEBUG_MODE=true

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=meu_banco
DB_USER=usuario
DB_PASSWORD=senha

# AWS (opcional)
AWS_ACCESS_KEY_ID=sua_key
AWS_SECRET_ACCESS_KEY=sua_secret
AWS_REGION=us-east-1

# RabbitMQ (opcional)
RABBIT_USAGE=false
```

### 3. Usar nos seus scripts

Agora é só importar e usar! Veja os exemplos abaixo.

---

## 📋 Índice de Exemplos

| Exemplo | Descrição | Arquivo |
|---------|-----------|---------|
| **01** | Configurações básicas | [01_basic_usage.py](01_basic_usage.py) |
| **02** | Database com psycopg2 | [02_database_basic.py](02_database_basic.py) |
| **03** | SQLAlchemy ORM e CRUD | [03_database_sqlalchemy.py](03_database_sqlalchemy.py) |
| **04** | AWS S3 operações | [04_aws_s3.py](04_aws_s3.py) |
| **05** | RabbitMQ mensageria | [05_rabbitmq.py](05_rabbitmq.py) |
| **06** | Sistema de logs | [06_logger.py](06_logger.py) |
| **07** | Utilitários diversos | [07_utils.py](07_utils.py) |
| **08** | Tratamento de erros | [08_exceptions.py](08_exceptions.py) |

---

## 🎯 Quick Start

### Exemplo Mínimo

```python
# meu_script.py
from automacoes_python_base_td import settings
from automacoes_python_base_td.logger import get_logger

# Configurar logger
logger = get_logger()

# Usar configurações
logger.info(f"App: {settings.app_name}")
logger.info(f"Ambiente: {settings.env}")

if settings.is_production():
    logger.warning("⚠️ Rodando em PRODUÇÃO!")
else:
    logger.info("🔧 Ambiente de desenvolvimento")
```

### Usar Database

```python
from automacoes_python_base_td.database import get_session, CRUDBase
from sqlalchemy import Column, String, Float

# Seu model
class Product(BaseModel):
    __tablename__ = "products"
    name = Column(String(100))
    price = Column(Float)

# CRUD
crud = CRUDBase(Product)

with get_session("tdax") as session:
    # Criar
    produto = crud.create(session, {"name": "Notebook", "price": 3500})
    
    # Buscar
    produto = crud.get(session, produto.id)
    print(f"Produto: {produto.name}")
```

### Usar AWS S3

```python
from automacoes_python_base_td.aws import S3Client

s3 = S3Client(bucket_name="meu-bucket")

# Upload
s3.upload_file("relatorio.pdf", "uploads/relatorio.pdf")

# Download
s3.download_file("uploads/relatorio.pdf", "downloads/relatorio.pdf")
```

---

## 📝 Casos de Uso Comuns

### 1. Script de ETL (Extract, Transform, Load)

```python
# etl_vendas.py
from automacoes_python_base_td.database import get_connection
from automacoes_python_base_td.aws import S3Client
from automacoes_python_base_td.logger import get_logger
from automacoes_python_base_td.utils import format_timestamp
from datetime import datetime

logger = get_logger()

def extrair_vendas():
    """Extrai vendas do banco"""
    logger.info("Extraindo vendas...")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vendas WHERE data = CURRENT_DATE")
        return cursor.fetchall()

def processar_vendas(vendas):
    """Processa e transforma dados"""
    logger.info(f"Processando {len(vendas)} vendas...")
    # Processar...
    return vendas

def enviar_para_s3(dados):
    """Envia para S3"""
    filename = f"vendas_{format_timestamp(datetime.now(), '%Y%m%d')}.csv"
    logger.info(f"Enviando para S3: {filename}")
    
    s3 = S3Client(bucket_name="datalake")
    s3.upload_file("temp.csv", f"vendas/{filename}")

# Executar
vendas = extrair_vendas()
dados = processar_vendas(vendas)
enviar_para_s3(dados)
```

### 2. Worker de Processamento

```python
# worker.py
from automacoes_python_base_td.rabbitmq import RabbitMQConsumer
from automacoes_python_base_td.logger import get_logger
import json

logger = get_logger()

def processar_pedido(ch, method, properties, body):
    """Processa pedidos recebidos pela fila"""
    pedido = json.loads(body)
    logger.info(f"Processando pedido #{pedido['id']}")
    
    try:
        # Processar pedido...
        logger.info(f"Pedido #{pedido['id']} processado!")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.error(f"Erro ao processar: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)

# Iniciar worker
consumer = RabbitMQConsumer()
consumer.consume("pedidos", processar_pedido)
```

### 3. API com FastAPI

```python
# api.py
from fastapi import FastAPI, Depends
from automacoes_python_base_td.database import get_session
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/produtos")
def listar_produtos(session: Session = Depends(get_session)):
    """Lista produtos"""
    produtos = session.query(Product).filter_by(ativo=True).all()
    return {"produtos": produtos}
```

---

## 🔧 Customização

### Criar Seus Próprios Models

```python
# models.py
from automacoes_python_base_td.database import BaseModel
from sqlalchemy import Column, String, Float, Integer

class Cliente(BaseModel):
    __tablename__ = "clientes"
    
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    telefone = Column(String(20))

class Pedido(BaseModel):
    __tablename__ = "pedidos"
    
    cliente_id = Column(Integer, nullable=False)
    valor_total = Column(Float, default=0)
    status = Column(String(20), default="pendente")
```

### Criar Exceções Customizadas

```python
# exceptions.py
from automacoes_python_base_td.core.exceptions import create_custom_exception

# Exceções do seu domínio
PedidoInvalidoError = create_custom_exception(
    "PedidoInvalidoError",
    default_code="PEDIDO_001"
)

PagamentoRecusadoError = create_custom_exception(
    "PagamentoRecusadoError",
    default_code="PAGAMENTO_001"
)
```

---

## 💡 Dicas e Boas Práticas

### ✅ DO (Faça)

- Configure o `.env` antes de usar
- Use `with get_session()` para auto-commit/rollback
- Use logs para rastrear operações
- Trate exceções apropriadamente
- Use soft delete (padrão do CRUD)

### ❌ DON'T (Não Faça)

- Não commite o arquivo `.env`
- Não use credenciais hardcoded
- Não esqueça de fechar conexões
- Não ignore exceções
- Não delete registros diretamente (use soft delete)

---

## 🆘 Precisa de Ajuda?

### Documentação

Cada exemplo tem comentários explicativos. Leia os arquivos:

- `01_basic_usage.py` - Começar aqui
- `02_database_basic.py` - Database básico
- `03_database_sqlalchemy.py` - ORM completo
- E assim por diante...

### Estrutura do Projeto

```
seu_projeto/
├── .env                    # Suas configurações
├── requirements.txt        # automacoes-python-base-td==0.1.0
├── seu_script.py          # Seus scripts
└── models.py              # Seus models (opcional)
```

### Verificar Instalação

```python
import automacoes_python_base_td
print(automacoes_python_base_td.__version__)  # 0.1.0
```

---

## 📦 O Que Está Incluso

✅ **Core**
- Exceções customizadas com log automático
- Factory de exceções

✅ **Settings**
- Configuração via `.env`
- Múltiplos ambientes (dev/hom/prd)
- Validação automática

✅ **Database**
- Conexão psycopg2
- SQLAlchemy ORM
- CRUD pronto para usar
- Soft delete automático
- Suporte a múltiplos bancos

✅ **AWS**
- S3 Client (upload/download/list/delete)
- CloudWatch (logs)

✅ **RabbitMQ**
- Publisher (publicar mensagens)
- Consumer (consumir mensagens)

✅ **Logger**
- Loguru configurado
- Níveis de log
- Formatação customizável

✅ **Utils**
- String utils (slugify, truncate, remove_accents)
- Date utils (format, parse, days_between)
- File utils (ensure_dir, exists, size)

---

## 🎉 Começar Agora!

1. Instale o pacote: `pip install automacoes-python-base-td`
2. Configure o `.env`
3. Copie um exemplo e adapte ao seu caso
4. Execute e seja feliz! 🚀

**Boa codificação!**
