"""
Exemplos de uso do pacote automacoes-python-base-td
"""

# Exemplo 1: Buscar dados do banco
def exemplo_fetch_all():
    from automacoes_python_base_td import fetch_all
    
    # Buscar todos os usuários maiores de 18 anos
    users = fetch_all("SELECT * FROM users WHERE age > %s", (18,))
    
    for user in users:
        print(f"Nome: {user['name']}, Email: {user['email']}")


# Exemplo 2: Buscar um único registro
def exemplo_fetch_one():
    from automacoes_python_base_td import fetch_one
    
    # Buscar um usuário específico
    user = fetch_one("SELECT * FROM users WHERE id = %s", (1,))
    
    if user:
        print(f"Usuário encontrado: {user['name']}")
    else:
        print("Usuário não encontrado")


# Exemplo 3: Inserir dados
def exemplo_insert():
    from automacoes_python_base_td import execute_query
    
    # Inserir um novo usuário
    affected = execute_query(
        "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)",
        ("João Silva", "joao@example.com", 25)
    )
    
    print(f"{affected} registro(s) inserido(s)")


# Exemplo 4: Inserir múltiplos registros
def exemplo_insert_many():
    from automacoes_python_base_td import execute_many
    
    users_data = [
        ("Maria Santos", "maria@example.com", 30),
        ("Pedro Oliveira", "pedro@example.com", 28),
        ("Ana Costa", "ana@example.com", 35),
    ]
    
    affected = execute_many(
        "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)",
        users_data
    )
    
    print(f"{affected} registro(s) inserido(s)")


# Exemplo 5: Usar context manager
def exemplo_context_manager():
    from automacoes_python_base_td import get_connection
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Criar uma tabela temporária
        cursor.execute("""
            CREATE TEMP TABLE temp_users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100)
            )
        """)
        
        # Inserir dados
        cursor.execute(
            "INSERT INTO temp_users (name, email) VALUES (%s, %s)",
            ("Teste", "teste@example.com")
        )
        
        # Buscar dados
        cursor.execute("SELECT * FROM temp_users")
        results = cursor.fetchall()
        
        for row in results:
            print(row)


# Exemplo 6: Usar classe DatabaseConnection
def exemplo_database_connection():
    from automacoes_python_base_td import DatabaseConnection
    
    # Criar conexão com parâmetros personalizados
    db = DatabaseConnection(
        host="localhost",
        port=5432,
        database="mydb",
        user="myuser",
        password="mypass"
    )
    
    # Usar como context manager
    with db as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT version()")
        version = cursor.fetchone()
        print(f"PostgreSQL version: {version[0]}")


# Exemplo 7: Usar funções utilitárias
def exemplo_utils():
    from automacoes_python_base_td.utils import get_env, format_timestamp, log_message
    
    # Obter variável de ambiente
    db_host = get_env("DB_HOST", default="localhost")
    print(f"Database host: {db_host}")
    
    # Formatar timestamp
    timestamp = format_timestamp()
    print(f"Timestamp: {timestamp}")
    
    # Log de mensagens
    log_message("Iniciando processamento")
    log_message("Processamento concluído com sucesso", level="INFO")
    log_message("Atenção: limite próximo", level="WARNING")


# Exemplo 8: Transação completa
def exemplo_transacao():
    from automacoes_python_base_td import get_connection
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        try:
            # Múltiplas operações em uma transação
            cursor.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id",
                ("Novo Usuário", "novo@example.com")
            )
            user_id = cursor.fetchone()[0]
            
            cursor.execute(
                "INSERT INTO user_permissions (user_id, permission) VALUES (%s, %s)",
                (user_id, "read")
            )
            
            # Se tudo correr bem, o commit é feito automaticamente
            print(f"Usuário criado com ID: {user_id}")
            
        except Exception as e:
            # Se houver erro, o rollback é feito automaticamente
            print(f"Erro: {e}")
            raise


if __name__ == "__main__":
    print("=" * 50)
    print("EXEMPLOS DE USO - automacoes-python-base-td")
    print("=" * 50)
    
    # Descomente os exemplos que deseja executar
    # NOTA: Certifique-se de ter um banco PostgreSQL configurado
    
    # exemplo_fetch_all()
    # exemplo_fetch_one()
    # exemplo_insert()
    # exemplo_insert_many()
    # exemplo_context_manager()
    # exemplo_database_connection()
    exemplo_utils()
    # exemplo_transacao()

