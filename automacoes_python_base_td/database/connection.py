"""
Conexões PostgreSQL com psycopg2
"""
import os
from typing import Optional, List, Tuple, Any, Dict
from contextlib import contextmanager
import psycopg2
from psycopg2.extras import RealDictCursor
from ..settings import DatabaseSettings


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
        settings: Optional[DatabaseSettings] = None,
    ):
        """
        Inicializa a conexão com o banco de dados.
        """
        if settings:
            self.host = host or settings.db_host
            self.port = port or settings.db_port
            self.database = database or settings.db_name
            self.user = user or settings.db_user
            self.password = password or settings.db_password
        else:
            self.host = host or os.getenv("DB_HOST", "localhost")
            self.port = port or int(os.getenv("DB_PORT", "5432"))
            self.database = database or os.getenv("DB_NAME", "postgres")
            self.user = user or os.getenv("DB_USER", "postgres")
            self.password = password or os.getenv("DB_PASSWORD", "")
        
        self._connection = None
    
    def connect(self):
        """Estabelece conexão com o banco de dados"""
        if self._connection is None or self._connection.closed:
            self._connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
        return self._connection
    
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
    conn = db.connect()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
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
    connection_params = connection_params or {}
    with get_connection(**connection_params) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.rowcount


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

