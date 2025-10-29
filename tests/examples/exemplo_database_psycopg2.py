"""
Exemplo de uso do Database com psycopg2
"""
from automacoes_python_base_td import DatabaseConnection, fetch_all, fetch_one, execute_query
from automacoes_python_base_td import logger
from dotenv import load_dotenv

load_dotenv()

# Forma 1: Usando a classe DatabaseConnection (com context manager)
logger.info("=== Exemplo 1: DatabaseConnection ===")

with DatabaseConnection() as db:
    # Buscar todos os registros
    certs = db.fetch_all("SELECT * FROM certificates LIMIT 5")
    logger.info(f"Registros encontrados: {len(certs)}")
    
    for cert in certs:
        logger.info(f"Certificado: {cert}")

# Forma 2: Usando funções diretas
logger.info("\n=== Exemplo 2: Funções diretas ===")

# Fetch all
results = fetch_all("SELECT * FROM certificates LIMIT 3")
logger.info(f"Total de registros: {len(results)}")

# Fetch one
one_result = fetch_one("SELECT * FROM certificates LIMIT 1")
logger.info(f"Um registro: {one_result}")

# Execute query (INSERT, UPDATE, DELETE)
# execute_query(
#     "UPDATE certificates SET status = %s WHERE id = %s",
#     ("active", 1)
# )
# logger.success("Registro atualizado com sucesso!")

