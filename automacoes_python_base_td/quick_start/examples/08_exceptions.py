"""
EXEMPLO 8: EXCEÇÕES
===================

Como usar e criar exceções customizadas com log automático.

PRÉ-REQUISITOS:
- Pacote instalado: pip install automacoes-python-base-td
"""

from automacoes_python_base_td.core.exceptions import (
    DatabaseConnectionError,
    DatabaseQueryError,
    ModelNotFoundError,
    S3Exception,
    RabbitMQConnectionError,
    ValidationError,
    NotFoundError,
    AlreadyExistsError,
    create_custom_exception
)
from automacoes_python_base_td.logger import get_logger

logger = get_logger()

# ====================================================================
# USAR EXCEÇÕES DO PACOTE
# ====================================================================

def buscar_usuario(user_id):
    """Busca usuário no banco"""
    logger.info(f"Buscando usuário #{user_id}...")
    
    # Simular busca no banco
    if user_id == 999:
        # Lançar exceção (log automático)
        raise ModelNotFoundError("User", user_id)
    
    return {"id": user_id, "name": "João", "email": "joao@example.com"}


def validar_email(email):
    """Valida formato de email"""
    logger.debug(f"Validando email: {email}")
    
    if "@" not in email:
        raise ValidationError(
            "Formato de email inválido",
            field="email",
            value=email
        )
    
    return True


def criar_usuario(email):
    """Cria novo usuário"""
    logger.info(f"Criando usuário: {email}")
    
    # Verificar se já existe
    if usuario_existe(email):
        raise AlreadyExistsError("Email", identifier=email)
    
    # Criar usuário...
    logger.info("✅ Usuário criado!")
    return {"email": email, "id": 123}


def usuario_existe(email):
    """Simula verificação de usuário"""
    return email == "admin@example.com"


# ====================================================================
# CRIAR SUAS PRÓPRIAS EXCEÇÕES
# ====================================================================

# Criar exceção para erros de pagamento
PaymentError = create_custom_exception(
    name="PaymentError",
    default_message="Erro ao processar pagamento",
    default_code="PAY_001"
)

# Criar exceção para erros de estoque
StockError = create_custom_exception(
    name="StockError",
    default_message="Erro no controle de estoque",
    default_code="STOCK_001"
)


def processar_pagamento(valor, cartao):
    """Processa pagamento (pode lançar PaymentError)"""
    logger.info(f"Processando pagamento de R$ {valor:.2f}")
    
    if valor <= 0:
        raise PaymentError(
            "Valor inválido para pagamento",
            details={"valor": valor}
        )
    
    if not cartao:
        raise PaymentError(
            "Cartão não informado",
            code="PAY_002"
        )
    
    # Processar pagamento...
    logger.info("✅ Pagamento aprovado!")
    return True


def atualizar_estoque(produto_id, quantidade):
    """Atualiza estoque (pode lançar StockError)"""
    logger.info(f"Atualizando estoque: produto {produto_id}, qtd {quantidade}")
    
    # Simular verificação de estoque
    estoque_atual = 5
    
    if quantidade > estoque_atual:
        raise StockError(
            "Estoque insuficiente",
            details={
                "produto_id": produto_id,
                "solicitado": quantidade,
                "disponivel": estoque_atual
            }
        )
    
    logger.info("✅ Estoque atualizado!")
    return True


# ====================================================================
# TRATAMENTO COMPLETO DE ERROS
# ====================================================================

def processar_pedido_completo(pedido_id, user_id, items, valor, cartao):
    """
    Processa pedido completo com tratamento de erros.
    Demonstra uso de múltiplas exceções.
    """
    logger.info(f"=" * 50)
    logger.info(f"🛒 Processando pedido #{pedido_id}")
    logger.info(f"=" * 50)
    
    try:
        # 1. Buscar usuário
        logger.info("📝 Etapa 1: Verificar usuário")
        usuario = buscar_usuario(user_id)
        logger.info(f"   ✅ Usuário: {usuario['name']}")
        
        # 2. Validar email
        logger.info("📝 Etapa 2: Validar email")
        validar_email(usuario['email'])
        logger.info("   ✅ Email válido")
        
        # 3. Verificar estoque
        logger.info("📝 Etapa 3: Verificar estoque")
        for item in items:
            atualizar_estoque(item['produto_id'], item['quantidade'])
        logger.info("   ✅ Estoque OK")
        
        # 4. Processar pagamento
        logger.info("📝 Etapa 4: Processar pagamento")
        processar_pagamento(valor, cartao)
        logger.info("   ✅ Pagamento aprovado")
        
        logger.info(f"=" * 50)
        logger.info(f"✅ Pedido #{pedido_id} CONCLUÍDO!")
        logger.info(f"=" * 50)
        return {"status": "sucesso", "pedido_id": pedido_id}
        
    except ModelNotFoundError as e:
        logger.error(f"❌ Usuário não encontrado: {e.details}")
        return {"status": "erro", "motivo": "usuario_nao_encontrado"}
        
    except ValidationError as e:
        logger.error(f"❌ Validação falhou: {e.message}")
        return {"status": "erro", "motivo": "validacao_falhou"}
        
    except StockError as e:
        logger.error(f"❌ Estoque insuficiente: {e.details}")
        return {"status": "erro", "motivo": "estoque_insuficiente"}
        
    except PaymentError as e:
        logger.error(f"❌ Pagamento falhou: {e.message}")
        return {"status": "erro", "motivo": "pagamento_recusado"}
        
    except Exception as e:
        logger.critical(f"🔥 Erro inesperado: {e}")
        return {"status": "erro", "motivo": "erro_interno"}


# ====================================================================
# EXECUTAR EXEMPLOS
# ====================================================================

if __name__ == "__main__":
    logger.info("=== Exemplo de Exceções ===\n")
    
    # Teste 1: Usuário não encontrado
    logger.info("📝 Teste 1: Buscar usuário inexistente")
    try:
        buscar_usuario(999)
    except ModelNotFoundError:
        logger.warning("   ⚠️  Exceção capturada (esperado)\n")
    
    # Teste 2: Email inválido
    logger.info("📝 Teste 2: Validar email inválido")
    try:
        validar_email("email_sem_arroba")
    except ValidationError:
        logger.warning("   ⚠️  Exceção capturada (esperado)\n")
    
    # Teste 3: Usuário já existe
    logger.info("📝 Teste 3: Criar usuário duplicado")
    try:
        criar_usuario("admin@example.com")
    except AlreadyExistsError:
        logger.warning("   ⚠️  Exceção capturada (esperado)\n")
    
    # Teste 4: Pagamento inválido
    logger.info("📝 Teste 4: Pagamento com valor negativo")
    try:
        processar_pagamento(-100, "1234")
    except PaymentError:
        logger.warning("   ⚠️  Exceção capturada (esperado)\n")
    
    # Teste 5: Estoque insuficiente
    logger.info("📝 Teste 5: Atualizar estoque insuficiente")
    try:
        atualizar_estoque(produto_id=1, quantidade=10)
    except StockError:
        logger.warning("   ⚠️  Exceção capturada (esperado)\n")
    
    # Teste 6: Pedido completo (COM SUCESSO)
    logger.info("📝 Teste 6: Pedido completo válido")
    resultado = processar_pedido_completo(
        pedido_id=12345,
        user_id=1,
        items=[{"produto_id": 1, "quantidade": 2}],
        valor=150.00,
        cartao="1234-5678"
    )
    logger.info(f"   Resultado: {resultado}\n")
    
    # Teste 7: Pedido completo (COM ERRO)
    logger.info("📝 Teste 7: Pedido com estoque insuficiente")
    resultado = processar_pedido_completo(
        pedido_id=12346,
        user_id=1,
        items=[{"produto_id": 1, "quantidade": 20}],  # Muito produto!
        valor=150.00,
        cartao="1234-5678"
    )
    logger.info(f"   Resultado: {resultado}\n")
    
    logger.info("=" * 50)
    logger.info("✅ Todos os testes de exceção concluídos!")
    logger.info("=" * 50)
