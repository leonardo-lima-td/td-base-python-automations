"""
Conexões PostgreSQL com psycopg2
"""
import os
from typing import Optional, List, Tuple, Any, Dict
from contextlib import contextmanager
import psycopg2
from psycopg2.extras import RealDictCursor
from ..settings import settings
from ..core.exceptions import DatabaseConnectionError, DatabaseQueryError


class DatabaseConnection:
    """
    Classe para gerenciar conexões com PostgreSQL
    """
    
    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
    ):
        """
        Inicializa a conexão com o banco de dados.
        Se não fornecidos, usa valores do settings global.
        """
        # Usa settings global como fallback
        self.host = host or settings.db_host
        self.port = port or settings.db_port
        self.database = database or settings.db_name
        self.user = user or settings.db_user
        self.password = password or settings.db_password
        
        self._connection = None
    
    def connect(self):
        """Estabelece conexão com o banco de dados"""
        try:
            if self._connection is None or self._connection.closed:
                self._connection = psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    database=self.database,
                    user=self.user,
                    password=self.password
                )
            return self._connection
        except psycopg2.Error as e:
            raise DatabaseConnectionError(
                f"Falha ao conectar ao banco de dados",
                details={
                    "host": self.host,
                    "port": self.port,
                    "database": self.database,
                    "error": str(e)
                }
            ) from e
    
    def close(self):
        """Fecha a conexão com o banco de dados"""
        if self._connection and not self._connection.closed:
            self._connection.close()
    
    def __enter__(self):
        return self.connect()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


@contextmanager
def get_connection(
    host: Optional[str] = None,
    port: Optional[int] = None,
    database: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
):
    """
    Context manager para conexão com banco de dados PostgreSQL.
    
    Exemplo:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
    """
    db = DatabaseConnection(host, port, database, user, password)
    try:
        conn = db.connect()
        yield conn
        conn.commit()
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        raise DatabaseQueryError(
            "Erro ao executar operação no banco",
            details={"error": str(e)}
        ) from e
    except DatabaseConnectionError:
        raise
    finally:
        db.close()


def execute_query(
    query: str,
    params: Optional[Tuple] = None,
    connection_params: Optional[Dict[str, Any]] = None,
) -> int:
    """
    Executa uma query SQL (INSERT, UPDATE, DELETE) e retorna o número de linhas afetadas.
    """
    try:
        connection_params = connection_params or {}
        with get_connection(**connection_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.rowcount
    except (DatabaseConnectionError, DatabaseQueryError):
        raise
    except Exception as e:
        raise DatabaseQueryError(
            "Erro ao executar query",
            details={"query": query[:100], "error": str(e)}
        ) from e


def execute_many(
    query: str,
    params_list: List[Tuple],
    connection_params: Optional[Dict[str, Any]] = None,
) -> int:
    """
    Executa múltiplas queries SQL com diferentes parâmetros.
    """
    connection_params = connection_params or {}
    with get_connection(**connection_params) as conn:
        with conn.cursor() as cursor:
            cursor.executemany(query, params_list)
            return cursor.rowcount


def fetch_all(
    query: str,
    params: Optional[Tuple] = None,
    connection_params: Optional[Dict[str, Any]] = None,
    as_dict: bool = True,
) -> List:
    """
    Executa uma query SELECT e retorna todos os resultados.
    """
    connection_params = connection_params or {}
    with get_connection(**connection_params) as conn:
        cursor_factory = RealDictCursor if as_dict else None
        with conn.cursor(cursor_factory=cursor_factory) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()


def fetch_one(
    query: str,
    params: Optional[Tuple] = None,
    connection_params: Optional[Dict[str, Any]] = None,
    as_dict: bool = True,
) -> Optional[Any]:
    """
    Executa uma query SELECT e retorna apenas um resultado.
    """
    connection_params = connection_params or {}
    with get_connection(**connection_params) as conn:
        cursor_factory = RealDictCursor if as_dict else None
        with conn.cursor(cursor_factory=cursor_factory) as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()

