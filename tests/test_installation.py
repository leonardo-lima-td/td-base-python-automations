#!/usr/bin/env python3
"""
Script de teste para validar a instalação do pacote automacoes-python-base-td
Execute: python test_installation.py
"""

def test_imports():
    """Testa se todos os módulos podem ser importados"""
    print("=" * 60)
    print("TESTE DE INSTALAÇÃO - automacoes-python-base-td")
    print("=" * 60)
    print()
    
    success_count = 0
    total_count = 0
    
    # Teste 1: Importar pacote
    print("1. Testando importação do pacote...")
    total_count += 1
    try:
        import automacoes_python_base_td
        print(f"   ✓ Pacote importado com sucesso!")
        print(f"   ✓ Versão: {automacoes_python_base_td.__version__}")
        success_count += 1
    except ImportError as e:
        print(f"   ✗ Erro ao importar pacote: {e}")
    print()
    
    # Teste 2: Database (psycopg2)
    print("2. Testando módulo database (PostgreSQL)...")
    total_count += 1
    try:
        from automacoes_python_base_td import (
            get_connection,
            fetch_all,
            fetch_one,
            execute_query,
            execute_many,
            DatabaseConnection,
        )
        print("   ✓ Todas as funções de database importadas!")
        success_count += 1
    except ImportError as e:
        print(f"   ✗ Erro: {e}")
    print()
    
    # Teste 3: SQLAlchemy
    print("3. Testando módulo SQLAlchemy...")
    total_count += 1
    try:
        from automacoes_python_base_td import (
            Base,
            BaseModel,
            DatabaseSessionManager,
            init_db,
            get_session,
            get_db_manager,
            get_db_dependency,
        )
        print("   ✓ Todas as funções de SQLAlchemy importadas!")
        success_count += 1
    except ImportError as e:
        print(f"   ✗ Erro: {e}")
    print()
    
    # Teste 4: AWS
    print("4. Testando módulo AWS (S3 e CloudWatch)...")
    total_count += 1
    try:
        from automacoes_python_base_td import (
            S3Client,
            CloudWatchClient,
            upload_to_s3,
            download_from_s3,
            send_logs_to_cloudwatch,
        )
        print("   ✓ Todas as funções de AWS importadas!")
        success_count += 1
    except ImportError as e:
        print(f"   ✗ Erro: {e}")
    print()
    
    # Teste 5: Logger
    print("5. Testando módulo Logger (Loguru)...")
    total_count += 1
    try:
        from automacoes_python_base_td import (
            logger,
            setup_logger,
            get_logger,
        )
        print("   ✓ Logger importado!")
        # Teste básico de logging
        import sys
        from io import StringIO
        old_stderr = sys.stderr
        sys.stderr = StringIO()
        logger.info("Teste de log")
        sys.stderr = old_stderr
        print("   ✓ Log funcionando!")
        success_count += 1
    except ImportError as e:
        print(f"   ✗ Erro: {e}")
    print()
    
    # Teste 6: RabbitMQ
    print("6. Testando módulo RabbitMQ...")
    total_count += 1
    try:
        from automacoes_python_base_td import (
            RabbitMQPublisher,
            RabbitMQConsumer,
            publish_message,
            consume_messages,
        )
        print("   ✓ Todas as funções de RabbitMQ importadas!")
        success_count += 1
    except ImportError as e:
        print(f"   ✗ Erro: {e}")
    print()
    
    # Teste 7: Dependências
    print("7. Testando dependências instaladas...")
    total_count += 1
    dependencies = [
        ("psycopg2", "PostgreSQL"),
        ("sqlalchemy", "SQLAlchemy"),
        ("boto3", "AWS"),
        ("loguru", "Loguru"),
        ("pika", "RabbitMQ"),
    ]
    
    deps_ok = True
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"   ✓ {name} ({module}) instalado")
        except ImportError:
            print(f"   ✗ {name} ({module}) NÃO instalado")
            deps_ok = False
    
    if deps_ok:
        success_count += 1
    print()
    
    # Resumo
    print("=" * 60)
    print(f"RESULTADO: {success_count}/{total_count} testes passaram")
    print("=" * 60)
    print()
    
    if success_count == total_count:
        print("🎉 SUCESSO! Todos os módulos estão funcionando!")
        print()
        print("Próximos passos:")
        print("  1. Leia QUICK_START.md para começar")
        print("  2. Configure .env com suas credenciais")
        print("  3. Execute examples_advanced.py para ver exemplos")
        print()
        return True
    else:
        print("⚠️  ATENÇÃO! Alguns testes falharam.")
        print()
        print("Solução:")
        print("  1. Reinstale o pacote: pip install -e .")
        print("  2. Instale as dependências: pip install -r requirements.txt")
        print("  3. Execute este teste novamente")
        print()
        return False


def test_basic_functionality():
    """Testa funcionalidades básicas sem precisar de conexões"""
    print("\n" + "=" * 60)
    print("TESTE DE FUNCIONALIDADES BÁSICAS")
    print("=" * 60)
    print()
    
    # Teste Logger
    print("1. Testando Logger...")
    try:
        from automacoes_python_base_td import logger
        import sys
        from io import StringIO
        
        # Capturar output
        old_stderr = sys.stderr
        sys.stderr = StringIO()
        
        logger.info("Teste INFO")
        logger.warning("Teste WARNING")
        logger.error("Teste ERROR")
        
        sys.stderr = old_stderr
        print("   ✓ Logger funcionando corretamente!")
    except Exception as e:
        print(f"   ✗ Erro: {e}")
    print()
    
    # Teste Utils
    print("2. Testando Utils...")
    try:
        from automacoes_python_base_td.utils import format_timestamp, log_message
        
        timestamp = format_timestamp()
        print(f"   ✓ Timestamp: {timestamp}")
        
        # log_message imprime no console
        import sys
        from io import StringIO
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        log_message("Teste", "INFO")
        sys.stdout = old_stdout
        
        print("   ✓ Utils funcionando!")
    except Exception as e:
        print(f"   ✗ Erro: {e}")
    print()
    
    print("=" * 60)
    print("Testes básicos concluídos!")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    
    # Teste de importação
    success = test_imports()
    
    # Teste de funcionalidades básicas
    if success:
        test_basic_functionality()
    
    # Exit code
    sys.exit(0 if success else 1)

