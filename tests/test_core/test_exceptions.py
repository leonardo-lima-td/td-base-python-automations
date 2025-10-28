"""
Testes para o módulo de exceções
Testa funcionalidade, logging e hierarquia de exceções
"""
import pytest
from automacoes_python_base_td.core.exceptions import (
    BaseAppException,
    DatabaseException,
    DatabaseConnectionError,
    DatabaseQueryError,
    ModelNotFoundError,
    AWSException,
    S3Exception,
    CloudWatchException,
    RabbitMQException,
    RabbitMQConnectionError,
    RabbitMQPublishError,
    ValidationError,
    NotFoundError,
    AlreadyExistsError,
    create_custom_exception,
)


class TestBaseAppException:
    """Testes para BaseAppException"""
    
    def test_exception_with_message(self):
        """Testa criação de exceção com mensagem"""
        exc = BaseAppException("Erro teste", log_error=False)
        assert exc.message == "Erro teste"
        assert exc.code is None
        assert exc.details == {}
    
    def test_exception_with_code_and_details(self):
        """Testa criação de exceção com código e detalhes"""
        exc = BaseAppException(
            "Erro teste",
            code="TEST_001",
            details={"user": 123},
            log_error=False
        )
        assert exc.message == "Erro teste"
        assert exc.code == "TEST_001"
        assert exc.details == {"user": 123}
    
    def test_exception_str(self):
        """Testa conversão para string"""
        exc = BaseAppException(
            "Erro teste",
            code="TEST_001",
            details={"user": 123},
            log_error=False
        )
        result = str(exc)
        assert "Erro teste" in result
        assert "[TEST_001]" in result
        assert "Details" in result
    
    def test_exception_to_dict(self):
        """Testa conversão para dicionário"""
        exc = BaseAppException(
            "Erro teste",
            code="TEST_001",
            details={"user": 123},
            log_error=False
        )
        result = exc.to_dict()
        assert result["error"] == "BaseAppException"
        assert result["message"] == "Erro teste"
        assert result["code"] == "TEST_001"
        assert result["details"] == {"user": 123}
    
    def test_exception_logs_by_default(self, caplog):
        """Testa se exceção emite log por padrão"""
        import logging
        caplog.set_level(logging.ERROR)
        
        exc = BaseAppException("Erro com log", code="LOG_001")
        
        # Verifica se log foi emitido
        assert len(caplog.records) > 0
        assert caplog.records[0].levelname == "ERROR"
        assert "BaseAppException" in caplog.records[0].message
        assert "Erro com log" in caplog.records[0].message
    
    def test_exception_no_log_when_disabled(self, caplog):
        """Testa se log pode ser desabilitado"""
        import logging
        caplog.set_level(logging.ERROR)
        
        exc = BaseAppException("Erro sem log", log_error=False)
        
        # Verifica que nenhum log foi emitido
        assert len(caplog.records) == 0


class TestDatabaseExceptions:
    """Testes para exceções de banco de dados"""
    
    def test_database_connection_error(self, caplog):
        """Testa DatabaseConnectionError"""
        import logging
        caplog.set_level(logging.ERROR)
        
        with pytest.raises(DatabaseConnectionError) as exc_info:
            raise DatabaseConnectionError(
                "Falha ao conectar",
                details={"host": "localhost", "port": 5432}
            )
        
        exc = exc_info.value
        assert exc.code == "DB_CONNECTION"
        assert exc.details["host"] == "localhost"
        assert exc.details["port"] == 5432
        
        # Verifica log
        assert any("DatabaseConnectionError" in record.message for record in caplog.records)
    
    def test_database_query_error(self, caplog):
        """Testa DatabaseQueryError"""
        import logging
        caplog.set_level(logging.ERROR)
        
        with pytest.raises(DatabaseQueryError) as exc_info:
            raise DatabaseQueryError(
                "Erro na query",
                details={"query": "SELECT * FROM users"}
            )
        
        exc = exc_info.value
        assert exc.code == "DB_QUERY"
        assert "query" in exc.details
    
    def test_model_not_found_error(self, caplog):
        """Testa ModelNotFoundError"""
        import logging
        caplog.set_level(logging.ERROR)
        
        with pytest.raises(ModelNotFoundError) as exc_info:
            raise ModelNotFoundError("User", 999)
        
        exc = exc_info.value
        assert exc.code == "MODEL_NOT_FOUND"
        assert "User" in exc.message
        assert exc.details["id"] == 999
    
    def test_database_exception_hierarchy(self):
        """Testa hierarquia de exceções de banco"""
        # DatabaseConnectionError é DatabaseException
        assert issubclass(DatabaseConnectionError, DatabaseException)
        
        # DatabaseQueryError é DatabaseException
        assert issubclass(DatabaseQueryError, DatabaseException)
        
        # ModelNotFoundError é DatabaseException
        assert issubclass(ModelNotFoundError, DatabaseException)
        
        # Todas são BaseAppException
        assert issubclass(DatabaseException, BaseAppException)


class TestAWSExceptions:
    """Testes para exceções AWS"""
    
    def test_s3_exception(self, caplog):
        """Testa S3Exception"""
        import logging
        caplog.set_level(logging.ERROR)
        
        with pytest.raises(S3Exception) as exc_info:
            raise S3Exception(
                "Erro no upload",
                details={"bucket": "my-bucket", "key": "file.txt"}
            )
        
        exc = exc_info.value
        assert exc.code == "S3_ERROR"
        assert exc.details["bucket"] == "my-bucket"
    
    def test_cloudwatch_exception(self, caplog):
        """Testa CloudWatchException"""
        import logging
        caplog.set_level(logging.ERROR)
        
        with pytest.raises(CloudWatchException):
            raise CloudWatchException("Erro no CloudWatch")
        
        # Verifica log
        assert any("CloudWatchException" in record.message for record in caplog.records)


class TestRabbitMQExceptions:
    """Testes para exceções RabbitMQ"""
    
    def test_rabbitmq_connection_error(self, caplog):
        """Testa RabbitMQConnectionError"""
        import logging
        caplog.set_level(logging.ERROR)
        
        with pytest.raises(RabbitMQConnectionError) as exc_info:
            raise RabbitMQConnectionError(
                details={"host": "localhost", "port": 5672}
            )
        
        exc = exc_info.value
        assert exc.code == "RABBITMQ_CONNECTION"
    
    def test_rabbitmq_publish_error(self, caplog):
        """Testa RabbitMQPublishError"""
        import logging
        caplog.set_level(logging.ERROR)
        
        with pytest.raises(RabbitMQPublishError):
            raise RabbitMQPublishError("Falha ao publicar")


class TestGenericExceptions:
    """Testes para exceções genéricas"""
    
    def test_validation_error(self, caplog):
        """Testa ValidationError"""
        import logging
        caplog.set_level(logging.ERROR)
        
        with pytest.raises(ValidationError) as exc_info:
            raise ValidationError("Email inválido", field="email")
        
        exc = exc_info.value
        assert exc.code == "VALIDATION_ERROR"
        assert exc.details["field"] == "email"
    
    def test_not_found_error(self, caplog):
        """Testa NotFoundError"""
        import logging
        caplog.set_level(logging.ERROR)
        
        with pytest.raises(NotFoundError) as exc_info:
            raise NotFoundError("Cliente", identifier="12345")
        
        exc = exc_info.value
        assert exc.code == "NOT_FOUND"
        assert exc.details["resource"] == "Cliente"
        assert exc.details["identifier"] == "12345"
    
    def test_already_exists_error(self, caplog):
        """Testa AlreadyExistsError"""
        import logging
        caplog.set_level(logging.ERROR)
        
        with pytest.raises(AlreadyExistsError) as exc_info:
            raise AlreadyExistsError("Email", identifier="user@example.com")
        
        exc = exc_info.value
        assert exc.code == "ALREADY_EXISTS"


class TestCustomExceptionFactory:
    """Testes para factory de exceções customizadas"""
    
    def test_create_custom_exception(self):
        """Testa criação de exceção customizada"""
        PaymentError = create_custom_exception(
            name="PaymentError",
            default_message="Erro no pagamento",
            default_code="PAY_001"
        )
        
        with pytest.raises(PaymentError) as exc_info:
            raise PaymentError("Cartão recusado", log_error=False)
        
        exc = exc_info.value
        assert exc.__class__.__name__ == "PaymentError"
        assert exc.code == "PAY_001"
        assert exc.message == "Cartão recusado"
    
    def test_custom_exception_with_details(self, caplog):
        """Testa exceção customizada com detalhes"""
        import logging
        caplog.set_level(logging.ERROR)
        
        AuthError = create_custom_exception(
            name="AuthError",
            default_code="AUTH_001"
        )
        
        with pytest.raises(AuthError):
            raise AuthError(
                "Token expirado",
                details={"user_id": 123}
            )
        
        # Verifica log
        assert any("AuthError" in record.message for record in caplog.records)

