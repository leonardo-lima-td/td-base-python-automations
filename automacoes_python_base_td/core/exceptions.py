"""
Exceções customizáveis para o pacote
"""
from typing import Optional, Dict, Any
from loguru import logger


class BaseAppException(Exception):
    """
    Exception base customizável para toda a aplicação.
    
    Permite criar exceções personalizadas facilmente.
    
    Attributes:
        message: Mensagem de erro
        code: Código de erro (opcional)
        details: Detalhes adicionais (opcional)
    
    Exemplo:
        raise BaseAppException(
            "Erro ao processar", 
            code="PROC_001",
            details={"user_id": 123, "action": "save"}
        )
    """
    
    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        log_error: bool = True,
    ):
        self.message = message
        self.code = code
        self.details = details or {}
        
        # Log automático do erro
        if log_error:
            self._log_error()
        
        super().__init__(self.message)
    
    def _log_error(self):
        """Emite log de erro automaticamente"""
        log_msg = self.message
        if self.code:
            log_msg = f"[{self.code}] {log_msg}"
        
        logger.error(
            f"{self.__class__.__name__}: {log_msg}",
            extra={"code": self.code, "details": self.details}
        )
    
    def __str__(self):
        parts = [self.message]
        if self.code:
            parts.append(f"[{self.code}]")
        if self.details:
            parts.append(f"Details: {self.details}")
        return " ".join(parts)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte a exceção para dicionário"""
        return {
            "error": self.__class__.__name__,
            "message": self.message,
            "code": self.code,
            "details": self.details,
        }


# ==================== DATABASE EXCEPTIONS ====================

class DatabaseException(BaseAppException):
    """Exceção genérica de banco de dados"""
    pass


class DatabaseConnectionError(DatabaseException):
    """Erro de conexão com o banco de dados"""
    
    def __init__(self, message: str = "Erro ao conectar ao banco de dados", **kwargs):
        super().__init__(message, code="DB_CONNECTION", **kwargs)


class DatabaseQueryError(DatabaseException):
    """Erro ao executar query no banco de dados"""
    
    def __init__(self, message: str = "Erro ao executar query", **kwargs):
        super().__init__(message, code="DB_QUERY", **kwargs)


class ModelNotFoundError(DatabaseException):
    """Model não encontrado no banco de dados"""
    
    def __init__(self, model_name: str, id: Any, **kwargs):
        message = f"{model_name} com id={id} não encontrado"
        super().__init__(message, code="MODEL_NOT_FOUND", details={"model": model_name, "id": id})


# ==================== AWS EXCEPTIONS ====================

class AWSException(BaseAppException):
    """Exceção genérica de AWS"""
    pass


class S3Exception(AWSException):
    """Erro relacionado ao S3"""
    
    def __init__(self, message: str = "Erro no S3", **kwargs):
        super().__init__(message, code="S3_ERROR", **kwargs)


class CloudWatchException(AWSException):
    """Erro relacionado ao CloudWatch"""
    
    def __init__(self, message: str = "Erro no CloudWatch", **kwargs):
        super().__init__(message, code="CLOUDWATCH_ERROR", **kwargs)


# ==================== RABBITMQ EXCEPTIONS ====================

class RabbitMQException(BaseAppException):
    """Exceção genérica de RabbitMQ"""
    pass


class RabbitMQConnectionError(RabbitMQException):
    """Erro de conexão com RabbitMQ"""
    
    def __init__(self, message: str = "Erro ao conectar ao RabbitMQ", **kwargs):
        super().__init__(message, code="RABBITMQ_CONNECTION", **kwargs)


class RabbitMQPublishError(RabbitMQException):
    """Erro ao publicar mensagem no RabbitMQ"""
    
    def __init__(self, message: str = "Erro ao publicar mensagem", **kwargs):
        super().__init__(message, code="RABBITMQ_PUBLISH", **kwargs)


class RabbitMQConsumeError(RabbitMQException):
    """Erro ao consumir mensagem do RabbitMQ"""
    
    def __init__(self, message: str = "Erro ao consumir mensagem", **kwargs):
        super().__init__(message, code="RABBITMQ_CONSUME", **kwargs)


# ==================== SETTINGS EXCEPTIONS ====================

class SettingsException(BaseAppException):
    """Exceção genérica de configurações"""
    pass


class ConfigurationError(SettingsException):
    """Erro de configuração"""
    
    def __init__(self, message: str = "Erro de configuração", **kwargs):
        super().__init__(message, code="CONFIG_ERROR", **kwargs)


# ==================== GENERIC EXCEPTIONS ====================

class ValidationError(BaseAppException):
    """Erro de validação de dados"""
    
    def __init__(self, message: str = "Erro de validação", field: Optional[str] = None, **kwargs):
        details = kwargs.get("details", {})
        if field:
            details["field"] = field
        super().__init__(message, code="VALIDATION_ERROR", details=details, **kwargs)


class NotFoundError(BaseAppException):
    """Recurso não encontrado"""
    
    def __init__(self, resource: str, identifier: Any = None, **kwargs):
        message = f"{resource} não encontrado"
        if identifier:
            message += f": {identifier}"
        details = {"resource": resource}
        if identifier:
            details["identifier"] = identifier
        super().__init__(message, code="NOT_FOUND", details=details)


class AlreadyExistsError(BaseAppException):
    """Recurso já existe"""
    
    def __init__(self, resource: str, identifier: Any = None, **kwargs):
        message = f"{resource} já existe"
        if identifier:
            message += f": {identifier}"
        details = {"resource": resource}
        if identifier:
            details["identifier"] = identifier
        super().__init__(message, code="ALREADY_EXISTS", details=details)


# ==================== CUSTOM EXCEPTION FACTORY ====================

def create_custom_exception(
    name: str,
    base_class: type = BaseAppException,
    default_message: str = "Erro customizado",
    default_code: Optional[str] = None,
) -> type:
    """
    Factory para criar exceções customizadas dinamicamente.
    
    Args:
        name: Nome da exceção
        base_class: Classe base (padrão: BaseAppException)
        default_message: Mensagem padrão
        default_code: Código padrão
    
    Returns:
        Nova classe de exceção
    
    Exemplo:
        PaymentError = create_custom_exception(
            name="PaymentError",
            default_message="Erro no pagamento",
            default_code="PAYMENT_ERROR"
        )
        
        raise PaymentError("Cartão recusado", details={"card": "****1234"})
    """
    
    def __init__(self, message: str = default_message, **kwargs):
        code = kwargs.pop("code", default_code)
        super(self.__class__, self).__init__(message, code=code, **kwargs)
    
    return type(name, (base_class,), {"__init__": __init__})

