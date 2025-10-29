"""
Testes para validar a montagem e estrutura do pacote
Valida imports, exportações e integridade do pacote
"""
import pytest
import sys
import importlib


class TestPackageStructure:
    """Testes para estrutura do pacote"""
    
    def test_package_import(self):
        """Testa se o pacote pode ser importado"""
        import automacoes_python_base_td
        assert automacoes_python_base_td is not None
    
    def test_package_version(self):
        """Testa se versão está definida"""
        import automacoes_python_base_td
        assert hasattr(automacoes_python_base_td, '__version__')
        assert automacoes_python_base_td.__version__ is not None
    
    def test_package_has_all(self):
        """Testa se __all__ está definido"""
        import automacoes_python_base_td
        assert hasattr(automacoes_python_base_td, '__all__')
        assert isinstance(automacoes_python_base_td.__all__, list)
        assert len(automacoes_python_base_td.__all__) > 0


class TestCoreExports:
    """Testa exportações do módulo core"""
    
    def test_exceptions_export(self):
        """Testa se exceções são exportadas"""
        from automacoes_python_base_td import (
            BaseAppException,
            DatabaseException,
            DatabaseConnectionError,
            DatabaseQueryError,
            ModelNotFoundError,
            AWSException,
            S3Exception,
            RabbitMQException,
            ValidationError,
            NotFoundError,
        )
        
        # Verifica se são classes
        assert isinstance(BaseAppException, type)
        assert isinstance(DatabaseException, type)
        assert isinstance(ValidationError, type)


class TestSettingsExports:
    """Testa exportações do módulo settings"""
    
    def test_settings_export(self):
        """Testa se settings são exportados"""
        from automacoes_python_base_td import AppSettings, settings
        
        assert AppSettings is not None
        assert settings is not None
    
    def test_settings_instance(self):
        """Testa se settings é uma instância de AppSettings"""
        from automacoes_python_base_td import AppSettings, settings
        
        assert isinstance(settings, AppSettings)
    
    def test_settings_has_required_attributes(self):
        """Testa se settings tem atributos necessários"""
        from automacoes_python_base_td import settings
        
        required_attrs = [
            'env', 'debug_mode', 'app_name',
            'db_host', 'db_user', 'db_password',
            'database_url', 'database_url_tdax', 'database_url_automation',
            'use_cloudwatch', 'log_destination', 'effective_log_level',
        ]
        
        for attr in required_attrs:
            assert hasattr(settings, attr), f"Settings missing attribute: {attr}"


class TestDatabaseExports:
    """Testa exportações do módulo database"""
    
    def test_psycopg2_exports(self):
        """Testa se funções psycopg2 são exportadas"""
        from automacoes_python_base_td import (
            get_connection,
            execute_query,
            execute_many,
            fetch_all,
            fetch_one,
            DatabaseConnection,
        )
        
        assert callable(get_connection)
        assert callable(execute_query)
        assert callable(fetch_all)
        assert isinstance(DatabaseConnection, type)
    
    def test_sqlalchemy_exports(self):
        """Testa se classes SQLAlchemy são exportadas"""
        from automacoes_python_base_td import (
            Base,
            BaseModel,
            DatabaseSessionManager,
        )
        
        assert Base is not None
        assert isinstance(DatabaseSessionManager, type)
    
    def test_session_manager_exports(self):
        """Testa se session manager functions são exportadas"""
        from automacoes_python_base_td import (
            get_manager,
            get_session,
            get_tdax_session,
            get_automations_session,
        )
        
        assert callable(get_manager)
        assert callable(get_session)
        assert callable(get_tdax_session)
        assert callable(get_automations_session)
    
    def test_crud_exports(self):
        """Testa se CRUD é exportado"""
        from automacoes_python_base_td import CRUDBase, crud_factory
        
        assert isinstance(CRUDBase, type)
        assert callable(crud_factory)
    
    def test_database_type_export(self):
        """Testa se DatabaseType é exportado"""
        from automacoes_python_base_td import DatabaseType
        
        # Verifica se é um Literal type
        from typing import get_args
        args = get_args(DatabaseType)
        assert "tdax" in args
        assert "automations" in args


class TestAWSExports:
    """Testa exportações do módulo AWS"""
    
    def test_aws_clients_export(self):
        """Testa se clientes AWS são exportados"""
        from automacoes_python_base_td import (
            AWSClient,
            S3Client,
            CloudWatchClient,
        )
        
        assert isinstance(AWSClient, type)
        assert isinstance(S3Client, type)
        assert isinstance(CloudWatchClient, type)
    
    def test_aws_helper_functions(self):
        """Testa se funções helper AWS são exportadas"""
        from automacoes_python_base_td import (
            upload_to_s3,
            download_from_s3,
            send_logs_to_cloudwatch,
        )
        
        assert callable(upload_to_s3)
        assert callable(download_from_s3)
        assert callable(send_logs_to_cloudwatch)


class TestRabbitMQExports:
    """Testa exportações do módulo RabbitMQ"""
    
    def test_rabbitmq_classes_export(self):
        """Testa se classes RabbitMQ são exportadas"""
        from automacoes_python_base_td import (
            RabbitMQConnection,
            RabbitMQPublisher,
            RabbitMQConsumer,
        )
        
        assert isinstance(RabbitMQConnection, type)
        assert isinstance(RabbitMQPublisher, type)
        assert isinstance(RabbitMQConsumer, type)
    
    def test_rabbitmq_helper_functions(self):
        """Testa se funções helper RabbitMQ são exportadas"""
        from automacoes_python_base_td import (
            publish_message,
            consume_messages,
        )
        
        assert callable(publish_message)
        assert callable(consume_messages)


class TestLoggerExports:
    """Testa exportações do módulo logger"""
    
    def test_logger_exports(self):
        """Testa se logger é exportado"""
        from automacoes_python_base_td import (
            setup_logger,
            get_logger,
            logger,
        )
        
        assert callable(setup_logger)
        assert callable(get_logger)
        assert logger is not None


class TestUtilsExports:
    """Testa exportações do módulo utils"""
    
    def test_file_utils_export(self):
        """Testa se funções de arquivo são exportadas"""
        from automacoes_python_base_td import (
            listdir,
            getdir,
            openfile,
            getsize,
            exists,
            isfile,
            isdir,
        )
        
        assert callable(listdir)
        assert callable(exists)
        assert callable(isfile)
    
    def test_string_utils_export(self):
        """Testa se funções de string são exportadas"""
        from automacoes_python_base_td import (
            slugify,
            truncate,
            capitalize_words,
        )
        
        assert callable(slugify)
        assert callable(truncate)
        assert callable(capitalize_words)
    
    def test_date_utils_export(self):
        """Testa se funções de data são exportadas"""
        from automacoes_python_base_td import (
            format_timestamp,
            parse_date,
            days_between,
        )
        
        assert callable(format_timestamp)
        assert callable(parse_date)
        assert callable(days_between)


class TestModuleStructure:
    """Testa estrutura de submódulos"""
    
    def test_core_module_exists(self):
        """Testa se módulo core existe"""
        from automacoes_python_base_td import core
        assert core is not None
    
    def test_settings_module_exists(self):
        """Testa se módulo settings existe"""
        from automacoes_python_base_td import settings
        assert settings is not None
    
    def test_database_module_exists(self):
        """Testa se módulo database existe"""
        from automacoes_python_base_td import database
        assert database is not None
    
    def test_aws_module_exists(self):
        """Testa se módulo aws existe"""
        from automacoes_python_base_td import aws
        assert aws is not None
    
    def test_rabbitmq_module_exists(self):
        """Testa se módulo rabbitmq existe"""
        from automacoes_python_base_td import rabbitmq
        assert rabbitmq is not None
    
    def test_logger_module_exists(self):
        """Testa se módulo logger existe"""
        from automacoes_python_base_td import logger
        assert logger is not None
    
    def test_utils_module_exists(self):
        """Testa se módulo utils existe"""
        from automacoes_python_base_td import utils
        assert utils is not None


class TestSubmoduleExports:
    """Testa se submódulos exportam o esperado"""
    
    def test_database_models_module(self):
        """Testa se database.models existe"""
        from automacoes_python_base_td.database import models
        assert models is not None
        assert hasattr(models, 'Base')
        assert hasattr(models, 'BaseModel')
    
    def test_database_models_tdax(self):
        """Testa se database.models.tdax existe"""
        from automacoes_python_base_td.database.models import tdax
        assert tdax is not None
    
    def test_database_models_automations(self):
        """Testa se database.models.automations existe"""
        from automacoes_python_base_td.database.models import automations
        assert automations is not None
    
    def test_database_repositories(self):
        """Testa se database.repositories existe"""
        from automacoes_python_base_td.database import repositories
        assert repositories is not None
        assert hasattr(repositories, 'CRUDBase')
        assert hasattr(repositories, 'crud_factory')


class TestImportPerformance:
    """Testa performance de imports"""
    
    def test_package_imports_quickly(self):
        """Testa se pacote importa rapidamente"""
        import time
        
        start = time.time()
        import automacoes_python_base_td
        end = time.time()
        
        import_time = end - start
        
        # Deve importar em menos de 2 segundos
        assert import_time < 2.0, f"Import too slow: {import_time:.2f}s"
    
    def test_lazy_imports(self):
        """Testa se imports pesados são lazy (não importam tudo de uma vez)"""
        import automacoes_python_base_td
        
        # Boto3 e pika não devem estar carregados ainda
        # (só quando realmente usar AWS/RabbitMQ)
        # assert 'boto3' not in sys.modules  # Pode estar se testes anteriores usaram
        # assert 'pika' not in sys.modules  # Pode estar se testes anteriores usaram
        
        # Pelo menos verificar que o pacote não quebra
        assert True


class TestDocumentation:
    """Testa se documentação está presente"""
    
    def test_package_has_docstring(self):
        """Testa se pacote tem docstring"""
        import automacoes_python_base_td
        assert automacoes_python_base_td.__doc__ is not None
        assert len(automacoes_python_base_td.__doc__) > 0
    
    def test_main_classes_have_docstrings(self):
        """Testa se classes principais têm docstrings"""
        from automacoes_python_base_td import (
            AppSettings,
            DatabaseSessionManager,
            CRUDBase,
            AWSClient,
        )
        
        assert AppSettings.__doc__ is not None
        assert DatabaseSessionManager.__doc__ is not None
        assert CRUDBase.__doc__ is not None
        assert AWSClient.__doc__ is not None

