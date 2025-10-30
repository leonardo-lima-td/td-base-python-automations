# 🧪 Testes Automatizados

## 📋 Estrutura de Testes

Os testes estão organizados por módulo, seguindo a mesma estrutura do pacote:

```
tests/
├── conftest.py                    # Configurações e fixtures compartilhadas
├── test_core/                     # Testes do módulo core
│   └── test_exceptions.py         # Testes de exceções e logging
├── test_database/                 # Testes do módulo database
│   ├── test_connection.py         # Testes de conexão PostgreSQL
│   └── test_crud.py              # Testes de CRUD genérico
├── test_aws/                      # Testes do módulo AWS
│   └── test_s3.py                # Testes do cliente S3
├── test_rabbitmq/                 # Testes do módulo RabbitMQ
│   └── test_connection.py         # Testes de conexão RabbitMQ
├── test_settings/                 # Testes do módulo settings
│   └── test_base.py              # Testes de configurações Pydantic
├── test_utils/                    # Testes do módulo utils
│   ├── test_string_utils.py       # Testes de utilitários de string
│   └── test_date_utils.py         # Testes de utilitários de data
└── test_logger/                   # Testes do módulo logger
    └── test_config.py             # Testes de configuração do Loguru
```

## 🎯 O que os Testes Cobrem

### 1. **Funcionalidade**
- Testes de comportamento esperado
- Testes de casos normais de uso
- Testes com diferentes parâmetros

### 2. **Exceções**
- Verifica se exceções corretas são lançadas
- Valida código e detalhes das exceções
- Testa hierarquia de exceções

### 3. **Logging**
- Verifica se logs são emitidos corretamente
- Valida nível e mensagem dos logs
- Testa logging automático nas exceções

## 🚀 Como Rodar os Testes

### Instalar dependências de teste:
```bash
pip install -e ".[dev]"
```

### Rodar todos os testes:
```bash
pytest
```

### Rodar testes de um módulo específico:
```bash
# Testes de exceções
pytest tests/test_core/

# Testes de database
pytest tests/test_database/

# Testes de AWS
pytest tests/test_aws/

# Testes de utils
pytest tests/test_utils/
```

### Rodar um arquivo específico:
```bash
pytest tests/test_core/test_exceptions.py
```

### Rodar com cobertura:
```bash
pytest --cov=automacoes_python_base_td --cov-report=html
```

### Rodar com verbose:
```bash
pytest -v
```

### Rodar testes que contêm uma palavra:
```bash
pytest -k "exception"
pytest -k "database"
```

## 📊 Fixtures Disponíveis

### `capture_logs`
Captura logs durante os testes para validação.

```python
def test_exception_logs(capture_logs):
    raise DatabaseConnectionError("Erro")
    assert "DatabaseConnectionError" in capture_logs.records[0].message
```

### `mock_db_connection`
Mock de conexão PostgreSQL.

```python
def test_with_db(mock_db_connection):
    conn, cursor = mock_db_connection
    # Use conn e cursor mockados
```

### `mock_psycopg2_connect`
Mock automático do psycopg2.connect.

```python
def test_connection(mock_psycopg2_connect):
    # psycopg2.connect já está mockado
    db = DatabaseConnection()
    conn = db.connect()
```

### `mock_boto3_client`
Mock do cliente boto3 para AWS.

```python
def test_s3(mock_boto3_client):
    # boto3.client já está mockado
    s3 = S3Client()
```

### `mock_pika_connection`
Mock da conexão RabbitMQ.

```python
def test_rabbitmq(mock_pika_connection):
    # pika.BlockingConnection já está mockado
    conn = RabbitMQConnection()
```

## 📝 Exemplo de Teste Completo

```python
def test_database_connection_error(caplog):
    """
    Testa se:
    1. Exceção correta é lançada
    2. Código da exceção está correto
    3. Detalhes estão presentes
    4. Log foi emitido
    """
    import logging
    caplog.set_level(logging.ERROR)
    
    # 1. Verifica se lança exceção correta
    with pytest.raises(DatabaseConnectionError) as exc_info:
        raise DatabaseConnectionError(
            "Falha ao conectar",
            details={"host": "localhost", "port": 5432}
        )
    
    # 2. Verifica código
    exc = exc_info.value
    assert exc.code == "DB_CONNECTION"
    
    # 3. Verifica detalhes
    assert exc.details["host"] == "localhost"
    assert exc.details["port"] == 5432
    
    # 4. Verifica log
    assert any("DatabaseConnectionError" in record.message 
               for record in caplog.records)
```

## 🎨 Boas Práticas

1. **Nome descritivo**: `test_exception_logs_correctly`
2. **Docstring**: Explique o que está testando
3. **AAA Pattern**: Arrange, Act, Assert
4. **Um conceito por teste**: Teste uma coisa de cada vez
5. **Use fixtures**: Evite duplicação de código
6. **Mock externo**: Mock APIs externas (DB, AWS, etc)

## 📈 Cobertura de Código

Para visualizar a cobertura:

```bash
pytest --cov=automacoes_python_base_td --cov-report=html
# Abra htmlcov/index.html no navegador
```

## ⚡ Testes Rápidos

Para rodar apenas testes rápidos (sem mocks lentos):

```bash
pytest -m "not slow"
```

## 🐛 Debug de Testes

Para debugar um teste específico:

```bash
pytest tests/test_core/test_exceptions.py::TestBaseAppException::test_exception_logs_by_default -v -s
```

Flags úteis:
- `-v`: verbose
- `-s`: mostra prints
- `-x`: para no primeiro erro
- `--pdb`: abre debugger no erro
- `--lf`: roda apenas os últimos testes que falharam

## 📚 Documentação

- [Pytest](https://docs.pytest.org/)
- [Unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [Pytest-cov](https://pytest-cov.readthedocs.io/)

