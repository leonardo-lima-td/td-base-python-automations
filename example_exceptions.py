"""
Exemplos de uso das exceções customizáveis
"""
from automacoes_python_base_td import (
    # Base
    BaseAppException,
    # Database
    DatabaseException,
    DatabaseConnectionError,
    DatabaseQueryError,
    ModelNotFoundError,
    # AWS
    AWSException,
    S3Exception,
    CloudWatchException,
    # RabbitMQ
    RabbitMQException,
    RabbitMQConnectionError,
    RabbitMQPublishError,
    RabbitMQConsumeError,
    # Settings
    SettingsException,
    ConfigurationError,
    # Generic
    ValidationError,
    NotFoundError,
    AlreadyExistsError,
)
from automacoes_python_base_td.core.exceptions import create_custom_exception


def exemplo_exceptions_basicas():
    """Exemplos de exceções básicas"""
    
    print("\n=== 1. Exception Base Customizável ===")
    try:
        raise BaseAppException(
            "Erro genérico",
            code="GEN_001",
            details={"user_id": 123, "action": "save"}
        )
    except BaseAppException as e:
        print(f"Erro: {e}")
        print(f"Dicionário: {e.to_dict()}")
    
    print("\n=== 2. Database Exceptions ===")
    try:
        raise DatabaseConnectionError(
            "Não foi possível conectar ao PostgreSQL",
            details={"host": "localhost", "port": 5432}
        )
    except DatabaseConnectionError as e:
        print(f"Erro DB: {e}")
    
    try:
        raise ModelNotFoundError("User", 999)
    except ModelNotFoundError as e:
        print(f"Model não encontrado: {e}")
        print(f"Details: {e.details}")
    
    print("\n=== 3. AWS Exceptions ===")
    try:
        raise S3Exception(
            "Erro ao fazer upload",
            details={"bucket": "my-bucket", "key": "file.txt"}
        )
    except S3Exception as e:
        print(f"Erro S3: {e}")
    
    print("\n=== 4. RabbitMQ Exceptions ===")
    try:
        raise RabbitMQPublishError(
            "Falha ao publicar mensagem",
            details={"queue": "tasks", "message_id": "abc123"}
        )
    except RabbitMQPublishError as e:
        print(f"Erro RabbitMQ: {e}")
    
    print("\n=== 5. Generic Exceptions ===")
    try:
        raise ValidationError(
            "Email inválido",
            field="email",
            details={"value": "invalid@"}
        )
    except ValidationError as e:
        print(f"Validação: {e}")
    
    try:
        raise NotFoundError("Cliente", identifier="12345")
    except NotFoundError as e:
        print(f"Não encontrado: {e}")
    
    try:
        raise AlreadyExistsError("Email", identifier="user@example.com")
    except AlreadyExistsError as e:
        print(f"Já existe: {e}")


def exemplo_custom_exception():
    """Exemplo de criação de exceção customizada"""
    
    print("\n=== 6. Custom Exception (Factory) ===")
    
    # Criar exceção customizada para pagamentos
    PaymentError = create_custom_exception(
        name="PaymentError",
        default_message="Erro ao processar pagamento",
        default_code="PAY_001"
    )
    
    try:
        raise PaymentError(
            "Cartão de crédito recusado",
            details={"card": "****1234", "amount": 150.50}
        )
    except PaymentError as e:
        print(f"Erro de pagamento: {e}")
        print(f"JSON: {e.to_dict()}")
    
    # Criar exceção customizada para autenticação
    AuthenticationError = create_custom_exception(
        name="AuthenticationError",
        base_class=BaseAppException,
        default_message="Falha na autenticação",
        default_code="AUTH_001"
    )
    
    try:
        raise AuthenticationError(
            "Token expirado",
            details={"user_id": 123, "expired_at": "2025-10-28"}
        )
    except AuthenticationError as e:
        print(f"Erro de autenticação: {e}")


def exemplo_uso_em_funcao():
    """Exemplo de uso em funções"""
    
    print("\n=== 7. Uso em funções ===")
    
    def buscar_usuario(user_id: int):
        """Simula busca de usuário"""
        if user_id < 0:
            raise ValidationError(
                "ID deve ser positivo",
                field="user_id",
                details={"value": user_id}
            )
        
        if user_id == 999:
            raise NotFoundError("Usuário", identifier=user_id)
        
        return {"id": user_id, "name": "João"}
    
    # Teste 1: ID inválido
    try:
        user = buscar_usuario(-1)
    except ValidationError as e:
        print(f"❌ {e}")
    
    # Teste 2: Usuário não encontrado
    try:
        user = buscar_usuario(999)
    except NotFoundError as e:
        print(f"❌ {e}")
    
    # Teste 3: Sucesso
    try:
        user = buscar_usuario(1)
        print(f"✅ Usuário encontrado: {user}")
    except BaseAppException as e:
        print(f"❌ {e}")


def exemplo_hierarquia_exceptions():
    """Exemplo de hierarquia de exceções"""
    
    print("\n=== 8. Hierarquia de Exceções ===")
    
    def operacao_banco():
        raise DatabaseQueryError("SELECT falhou")
    
    # Capturar exceção específica
    try:
        operacao_banco()
    except DatabaseQueryError as e:
        print(f"Query error específico: {e}")
    
    # Capturar categoria de exceções
    try:
        operacao_banco()
    except DatabaseException as e:
        print(f"Qualquer erro de database: {e}")
    
    # Capturar todas as exceções do pacote
    try:
        operacao_banco()
    except BaseAppException as e:
        print(f"Qualquer erro do pacote: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("EXEMPLOS DE EXCEÇÕES CUSTOMIZÁVEIS")
    print("=" * 60)
    
    exemplo_exceptions_basicas()
    exemplo_custom_exception()
    exemplo_uso_em_funcao()
    exemplo_hierarquia_exceptions()
    
    print("\n" + "=" * 60)
    print("✅ Todos os exemplos executados com sucesso!")
    print("=" * 60)

