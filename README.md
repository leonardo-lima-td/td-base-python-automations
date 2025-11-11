# Automações Python Base TD

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-0.1.0-orange.svg)](pyproject.toml)

Pacote Python modular e profissional com funcionalidades para Database (PostgreSQL + SQLAlchemy), AWS (S3 + CloudWatch), RabbitMQ, Logging e muito mais.

---

## 📦 Instalação

### Gerenciamento de Versões Python

Este projeto suporta múltiplas formas de gerenciamento de versões Python:

#### Usando pyenv (Recomendado)

```bash
# Instalar Python 3.12 (ou superior)
pyenv install 3.12

# O arquivo .python-version na raiz do projeto define automaticamente a versão
cd /home/vitorio/Desktop/Pessoal/python-base-TD
python --version  # Deve mostrar Python 3.12.x
```

### Instalação com Poetry

```bash
# Instalar Poetry (se ainda não tiver)
curl -sSL https://install.python-poetry.org | python3 -

# Instalar dependências
poetry install

# Instalar com dependências de desenvolvimento
poetry install --with dev

# Ativar o ambiente virtual
poetry shell
```

### Instalação com pip

#### Instalação Local (Desenvolvimento)

```bash
cd /home/vitorio/Desktop/Pessoal/python-base-TD
pip install -e .
```

#### Instalação via Git

```bash
pip install git+https://github.com/sua-empresa/automacoes-python-base-td.git
```

#### Instalação via Arquivo .whl

```bash
# 1. Construir o pacote
pip install build
python -m build

# 2. Instalar
pip install dist/automacoes_python_base_td-0.2.0-py3-none-any.whl
```

### Dependências

O pacote instalará automaticamente:
- `psycopg2-binary>=2.9.0` - PostgreSQL
- `sqlalchemy>=2.0.0` - ORM
- `boto3>=1.28.0` - AWS
- `loguru>=0.7.0` - Logging
- `pika>=1.3.0` - RabbitMQ
- `pydantic>=2.0.0` - Validação
- `pydantic-settings>=2.0.0` - Settings

### Dependências de Desenvolvimento

```bash
# Com pip
pip install -e ".[dev]"

# Com poetry
poetry install --with dev
```

Inclui: pytest, pytest-cov, black, flake8, ruff, taskipy

---

## 🚀 Início Rápido

### 1. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do seu projeto:

```bash
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mydb
DB_USER=myuser
DB_PASSWORD=mypass

# AWS (opcional)
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1

# RabbitMQ (opcional)
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest

# Logging (opcional)
LOG_LEVEL=INFO
LOG_FILE=app.log
```

### 2. Uso Básico

```python
from automacoes_python_base_td import logger, listdir, slugify

# Logging
logger.info("Aplicação iniciada")

# File utils
files = listdir(".", filter_ext=".py")
print(f"Arquivos Python: {len(files)}")

# String utils
slug = slugify("Hello World!")
print(f"Slug: {slug}")
```

### 3. Database com CRUD Genérico

```python
from automacoes_python_base_td import (
    init_db, BaseModel, get_session, crud_factory
)
from sqlalchemy import Column, String, Integer

# Definir model
class Product(BaseModel):
    __tablename__ = "products"
    name = Column(String(100))
    price = Column(Integer)

# Inicializar
init_db(create_tables=True)

# Criar CRUD automaticamente
product_crud = crud_factory(Product)

# Usar
with get_session() as session:
    # CREATE
    product = product_crud.create(session, {
        "name": "Notebook",
        "price": 3500
    })
    
    # READ
    products = product_crud.get_all(session)
    product = product_crud.get(session, id=1)
    
    # UPDATE
    product_crud.update(session, 1, {"price": 3200})
    
    # DELETE
    product_crud.delete(session, 1)
```

---

## ✨ Principais Funcionalidades

### Pydantic Settings

Configurações validadas automaticamente:

```python
from automacoes_python_base_td import DatabaseSettings

settings = DatabaseSettings()  # Carrega do .env
print(settings.postgres_url)
```

### CRUD Genérico (Plug and Play)

Funciona com qualquer model SQLAlchemy:

```python
from automacoes_python_base_td import crud_factory

user_crud = crud_factory(User)
product_crud = crud_factory(Product)
order_crud = crud_factory(Order)
```

### File Utils

```python
from automacoes_python_base_td import (
    listdir, exists, create_dir, write_file, read_file
)

files = listdir("/path", filter_ext=".csv")
create_dir("/tmp/mydir")
write_file("/tmp/mydir/file.txt", "Hello!")
content = read_file("/tmp/mydir/file.txt")
```

### String & Date Utils

```python
from automacoes_python_base_td import slugify, format_timestamp

slug = slugify("Hello World!")  # "hello-world"
timestamp = format_timestamp()  # "2025-10-28 14:30:00"
```

### PostgreSQL

```python
from automacoes_python_base_td import fetch_all, execute_query

users = fetch_all("SELECT * FROM users WHERE age > %s", (18,))
execute_query(
    "INSERT INTO users (name, email) VALUES (%s, %s)",
    ("João", "joao@example.com")
)
```

### AWS S3

```python
from automacoes_python_base_td.aws import S3Client

s3 = S3Client()
s3.upload_file("/path/file.csv", "bucket", "data/file.csv")
s3.download_file("bucket", "data/file.csv", "/path/download.csv")
```

### AWS CloudWatch

```python
from automacoes_python_base_td.aws import CloudWatchClient

cw = CloudWatchClient()
cw.put_log_events("log-group", "stream", ["Log 1", "Log 2"])
```

### RabbitMQ

```python
from automacoes_python_base_td import publish_message

publish_message(
    message={"event": "user_created", "id": 123},
    queue_name="events"
)
```

---

## 📁 Estrutura do Projeto

```
automacoes_python_base_td/
├── settings/         # Pydantic Settings
├── database/         # PostgreSQL + SQLAlchemy
│   ├── models/       # Seus models aqui
│   └── queries/      # CRUD genérico
├── aws/              # S3, CloudWatch
├── rabbitmq/         # Publisher, Consumer
├── logger/           # Loguru
└── utils/            # File, String, Date utils
```

---

## 📚 Documentação

Toda documentação está disponível no diretório `docs/`:

- `docs/estrutura_modular.txt` - Detalhes da estrutura
- `docs/guia_rapido.txt` - Guia de uso rápido
- `docs/pydantic_settings.txt` - Configurações
- `docs/crud_generico.txt` - CRUD automático
- `docs/utils.txt` - Utilitários
- `docs/exemplos.txt` - Exemplos de código

### Exemplos de Código

- `example_modular.py` - Exemplos da estrutura modular
- `examples_advanced.py` - Exemplos avançados
- `example_usage.py` - Exemplos básicos

---

## 🧪 Testes

Executar todos os testes:

```bash
pytest
```

Executar com cobertura:

```bash
pytest --cov=automacoes_python_base_td --cov-report=html
```

Executar testes específicos:

```bash
pytest tests/test_utils.py
pytest tests/test_crud.py
pytest tests/test_settings.py
```

---

## 🛠️ Ferramentas de Desenvolvimento

### Taskipy - Gerenciador de Tarefas

O projeto usa Taskipy para automatizar tarefas comuns. Após instalar as dependências de desenvolvimento, você pode usar:

```bash
# Formatar código automaticamente
task format

# Verificar formatação (sem modificar)
task format-check

# Executar linter
task lint

# Executar testes
task test

# Executar testes com cobertura
task test-cov

# Limpar arquivos temporários (__pycache__, .pyc)
task clean

# Construir o pacote
task build

# Instalar em modo desenvolvimento
task install-dev

# Executar todas as verificações (format + lint + test)
task all-checks
```

### Ruff - Linter e Formatter

Ruff é um linter e formatter extremamente rápido para Python. Ele substitui múltiplas ferramentas (Black, isort, flake8, etc.) em uma única ferramenta.

#### Uso Manual

```bash
# Verificar erros de linting
ruff check .

# Verificar e corrigir automaticamente
ruff check --fix .

# Formatar código
ruff format .

# Verificar formatação sem modificar
ruff format --check .
```

#### Configuração

O Ruff está configurado no `pyproject.toml` com:
- Comprimento máximo de linha: 100 caracteres
- Python alvo: 3.8+
- Regras ativas: pycodestyle, pyflakes, isort, pep8-naming, pyupgrade, flake8-bugbear, flake8-comprehensions

#### Integração com Editor

**VS Code:** Instale a extensão "Ruff" da marketplace

```json
// .vscode/settings.json
{
    "editor.formatOnSave": true,
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff"
    }
}
```

**PyCharm:** Configure em Settings → Tools → External Tools

**Vim/Neovim:** Use o plugin `vim-ruff` ou configure com ALE/LSP

---

## 🔧 Desenvolvimento

### Instalar em Modo Desenvolvimento

```bash
pip install -e ".[dev]"
```

### Estrutura de Diretórios

```
.
├── automacoes_python_base_td/  # Código fonte
├── tests/                       # Testes
├── docs/                        # Documentação
├── examples/                    # Exemplos
├── pyproject.toml              # Configuração do pacote
└── README.md                   # Este arquivo
```

### Usar o Template Quick Start

O diretório `quick_start` contém um template completo para iniciar seu projeto:

```bash
# 1. Copiar o template
cp -r automacoes_python_base_td/quick_start meu-novo-projeto
cd meu-novo-projeto

# 2. Personalizar o pyproject.toml
# Edite e altere: name, authors, dependencies

# 3. Instalar dependências
poetry install  # ou pip install -e ".[dev]"

# 4. Começar a desenvolver!
```

O template inclui:
- ✅ `pyproject.toml` - Configuração completa com Taskipy, Ruff, pytest
- ✅ `.python-version` - Versão Python para pyenv
- ✅ `env.example` - Template de variáveis de ambiente
- ✅ `requirements.txt` - Alternativa ao pyproject.toml
- ✅ `examples/` - Exemplos práticos de uso
- ✅ `.gitignore`, `.dockerignore` - Arquivos auxiliares

### Adicionar Novas Funcionalidades

1. **Models:** Adicione em `database/models/`
2. **Utils:** Adicione em `utils/`
3. **Settings:** Estenda `BaseAppSettings`
4. **Tests:** Adicione em `tests/`

---

## 📤 Distribuição

### Opção 1: Git (Recomendado)

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/sua-empresa/automacoes-python-base-td.git
git push -u origin main

# Outros instalam com:
pip install git+https://github.com/sua-empresa/automacoes-python-base-td.git
```

### Opção 2: PyPI Privado

```bash
# Construir
python -m build

# Upload para PyPI privado
twine upload --repository-url https://pypi.sua-empresa.com dist/*

# Instalar
pip install --index-url https://pypi.sua-empresa.com automacoes-python-base-td
```

### Opção 3: Arquivo .whl

```bash
# Construir
python -m build

# Compartilhar dist/*.whl
# Outros instalam:
pip install automacoes_python_base_td-0.1.0-py3-none-any.whl
```

---

## 🎯 Características

✅ **Modular** - Organização por funcionalidade  
✅ **Type Safe** - Pydantic valida automaticamente  
✅ **CRUD Genérico** - Zero código repetitivo  
✅ **Extensível** - Fácil adicionar funcionalidades  
✅ **Testado** - Testes unitários incluídos  
✅ **Documentado** - Docs completa em `docs/`  

---

## 🤝 Contribuindo

1. Adicione sua funcionalidade
2. Escreva testes em `tests/`
3. Atualize documentação em `docs/`
4. Execute `pytest` para validar
5. Commit e push

---

## 📄 Licença

MIT License - Uso interno TD Company

---

## 📞 Suporte

- **Documentação:** Veja `docs/`
- **Exemplos:** Arquivos `example_*.py`
- **Testes:** Execute `pytest -v`
- **Issues:** Entre em contato com o time de desenvolvimento

---

**Desenvolvido com ❤️ por TD Company**
