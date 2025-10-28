# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

## [0.2.0] - 2025-10-28

### Adicionado
- **AWS S3**: Cliente completo para upload, download, listagem e gerenciamento de arquivos
- **AWS CloudWatch**: Cliente para envio e leitura de logs
- **SQLAlchemy**: Suporte completo com session management, models base e FastAPI integration
- **Loguru**: Sistema de logging avançado com rotação, JSON, e contexto
- **RabbitMQ**: Publisher e Consumer para mensageria com suporte a exchanges e routing
- Funções helper para uso rápido de todas as funcionalidades
- Arquivos de exemplo avançados (`examples_advanced.py`)
- Documentação completa (`README_COMPLETO.md`)
- Arquivo de exemplo com todas as variáveis de ambiente (`.env.complete`)

### Atualizado
- Dependências atualizadas no `pyproject.toml`:
  - sqlalchemy>=2.0.0
  - boto3>=1.28.0
  - loguru>=0.7.0
  - pika>=1.3.0
- Versão do pacote: 0.1.0 → 0.2.0
- `__init__.py` com todas as novas exportações

## [0.1.0] - 2025-10-28

### Adicionado
- Estrutura inicial do projeto
- Módulo `database.py` com funções para PostgreSQL (psycopg2):
  - `get_connection()` - Context manager para conexões
  - `fetch_all()` - Buscar múltiplos registros
  - `fetch_one()` - Buscar um registro
  - `execute_query()` - INSERT/UPDATE/DELETE
  - `execute_many()` - Múltiplos INSERTs
  - `DatabaseConnection` - Classe para gerenciar conexões
- Módulo `utils.py` com funções utilitárias
- Configuração via variáveis de ambiente
- Suporte a transações automáticas
- Documentação básica (`README.md`)
- Guia de instalação (`GUIA_INSTALACAO.md`)
- Exemplos de uso (`example_usage.py`)
- Arquivos de configuração:
  - `pyproject.toml` - Configuração moderna do pacote
  - `setup.py` - Compatibilidade
  - `MANIFEST.in` - Arquivos para distribuição
  - `.gitignore` - Arquivos ignorados
  - `LICENSE` - MIT License

