"""
EXEMPLO 2: DATABASE BÁSICO
===========================

Como fazer queries SQL diretas usando psycopg2.
Útil para queries simples ou legado.

PRÉ-REQUISITOS:
- Pacote instalado: pip install automacoes-python-base-td
- Variáveis no .env: DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
"""

from automacoes_python_base_td.database import (
    DatabaseConnection,
    get_connection,
    execute_query
)
from automacoes_python_base_td.logger import get_logger

logger = get_logger()

# ====================================================================
# OPÇÃO 1: Classe DatabaseConnection
# ====================================================================

def exemplo_connection_basica():
    """Exemplo usando DatabaseConnection diretamente"""
    logger.info("Conectando ao banco...")
    
    db = DatabaseConnection()  # Usa configurações do .env
    conn = db.connect()
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE ativo = TRUE")
    total = cursor.fetchone()[0]
    
    logger.info(f"Total de usuários ativos: {total}")
    
    db.close()


# ====================================================================
# OPÇÃO 2: Context Manager (RECOMENDADO)
# ====================================================================

def exemplo_context_manager():
    """Exemplo usando context manager (auto commit/rollback)"""
    logger.info("Buscando usuários...")
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email FROM users LIMIT 10")
        users = cursor.fetchall()
        
        for user in users:
            logger.info(f"  👤 {user[0]}: {user[1]} ({user[2]})")


# ====================================================================
# OPÇÃO 3: Helper execute_query
# ====================================================================

def exemplo_execute_query():
    """Exemplo usando função helper para INSERT/UPDATE/DELETE"""
    logger.info("Inserindo novo usuário...")
    
    # INSERT
    rows_affected = execute_query(
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        ("João Silva", "joao@example.com")
    )
    logger.info(f"✅ {rows_affected} linha(s) inserida(s)")
    
    # UPDATE
    rows_affected = execute_query(
        "UPDATE users SET ativo = %s WHERE email = %s",
        (True, "joao@example.com")
    )
    logger.info(f"✅ {rows_affected} linha(s) atualizada(s)")


# ====================================================================
# EXECUTAR EXEMPLOS
# ====================================================================

if __name__ == "__main__":
    logger.info("=== Exemplo Database Básico ===")
    
    # Descomente os exemplos que quiser testar:
    # exemplo_connection_basica()
    # exemplo_context_manager()
    # exemplo_execute_query()
    
    logger.info("✅ Exemplos concluídos!")
