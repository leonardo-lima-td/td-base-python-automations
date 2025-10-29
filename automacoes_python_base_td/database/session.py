"""
Gerenciamento de sessões SQLAlchemy - TDAX e Automations
"""
import os
from typing import Optional, Generator
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from .models.base import Base
from ..settings import settings


class DatabaseSessionManager:
    """
    Gerenciador de sessões SQLAlchemy genérico
    """
    
    def __init__(
        self,
        database_url: str,
        echo: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ):
        """
        Inicializa o gerenciador de sessões.
        
        Args:
            database_url: URL de conexão do banco
            echo: Se True, mostra SQL queries no console
            pool_size: Tamanho do pool de conexões
            max_overflow: Conexões extras permitidas
        """
        self.database_url = database_url
        
        self.engine = create_engine(
            self.database_url,
            echo=echo,
            poolclass=QueuePool,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_pre_ping=True,
        )
        
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
        )
    
    def create_tables(self):
        """Cria todas as tabelas baseadas nos models definidos"""
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self) -> Session:
        """Retorna uma nova sessão"""
        return self.SessionLocal()
    
    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        """
        Context manager para sessão com auto-commit e rollback.
        
        Exemplo:
            with db_manager.session_scope() as session:
                user = session.query(User).first()
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


class TdaxSessionManager(DatabaseSessionManager):
    """
    Gerenciador de sessões para o banco TDAX
    """
    
    def __init__(
        self,
        database_url: Optional[str] = None,
        echo: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ):
        """
        Inicializa o gerenciador de sessões TDAX.
        
        Args:
            database_url: URL de conexão (padrão: TDAX_DATABASE_URL env)
            echo: Mostrar queries SQL
            pool_size: Tamanho do pool
            max_overflow: Conexões extras
        """
        if database_url is None:
            database_url = os.getenv(
                "TDAX_DATABASE_URL",
                "postgresql://postgres:postgres@localhost:5432/tdax"
            )
        
        super().__init__(
            database_url=database_url,
            echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )


class AutomationsSessionManager(DatabaseSessionManager):
    """
    Gerenciador de sessões para o banco Automations
    """
    
    def __init__(
        self,
        database_url: Optional[str] = None,
        echo: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ):
        """
        Inicializa o gerenciador de sessões Automations.
        
        Args:
            database_url: URL de conexão (padrão: AUTOMATIONS_DATABASE_URL env)
            echo: Mostrar queries SQL
            pool_size: Tamanho do pool
            max_overflow: Conexões extras
        """
        if database_url is None:
            database_url = os.getenv(
                "AUTOMATIONS_DATABASE_URL",
                "postgresql://postgres:postgres@localhost:5432/automations"
            )
        
        super().__init__(
            database_url=database_url,
            echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )


# Instâncias globais
_tdax_manager: Optional[TdaxSessionManager] = None
_automations_manager: Optional[AutomationsSessionManager] = None


def get_tdax_manager() -> TdaxSessionManager:
    """Retorna o gerenciador TDAX"""
    if _tdax_manager is None:
        raise RuntimeError(
            "Banco TDAX não foi inicializado. Chame init_tdax_db() primeiro."
        )
    return _tdax_manager


def get_automations_manager() -> AutomationsSessionManager:
    """Retorna o gerenciador Automations"""
    if _automations_manager is None:
        raise RuntimeError(
            "Banco Automations não foi inicializado. Chame init_automations_db() primeiro."
        )
    return _automations_manager


@contextmanager
def get_tdax_session() -> Generator[Session, None, None]:
    """
    Context manager para obter uma sessão TDAX.
    
    Exemplo:
        with get_tdax_session() as session:
            cliente = session.query(Cliente).filter_by(id=1).first()
    """
    manager = get_tdax_manager()
    with manager.session_scope() as session:
        yield session


@contextmanager
def get_automations_session() -> Generator[Session, None, None]:
    """
    Context manager para obter uma sessão Automations.
    
    Exemplo:
        with get_automations_session() as session:
            job = session.query(AutomationJob).filter_by(id=1).first()
    """
    manager = get_automations_manager()
    with manager.session_scope() as session:
        yield session


# Dependency injection para FastAPI
def get_tdax_db_dependency() -> Generator[Session, None, None]:
    """
    Dependency para usar com FastAPI - TDAX.
    
    Uso no FastAPI:
        from fastapi import Depends
        
        @app.get("/clientes")
        def get_clientes(db: Session = Depends(get_tdax_db_dependency)):
            return db.query(Cliente).all()
    """
    manager = get_tdax_manager()
    session = manager.get_session()
    try:
        yield session
    finally:
        session.close()


def get_automations_db_dependency() -> Generator[Session, None, None]:
    """
    Dependency para usar com FastAPI - Automations.
    
    Uso no FastAPI:
        from fastapi import Depends
        
        @app.get("/jobs")
        def get_jobs(db: Session = Depends(get_automations_db_dependency)):
            return db.query(AutomationJob).all()
    """
    manager = get_automations_manager()
    session = manager.get_session()
    try:
        yield session
    finally:
        session.close()


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """DEPRECATED: Use get_tdax_session() ou get_automations_session()"""
    with get_tdax_session() as session:
        yield session

