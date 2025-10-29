"""
Gerenciamento de sessões SQLAlchemy - Unificado
"""
from typing import Optional, Generator, Literal
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from .models.base import Base
from ..settings import settings


DatabaseType = Literal["tdax", "automations"]


class DatabaseSessionManager:
    """
    Gerenciador de sessões SQLAlchemy unificado.
    Suporta múltiplos bancos de dados através do parâmetro db_type.
    """
    
    def __init__(
        self,
        db_type: Optional[DatabaseType] = None,
        database_url: Optional[str] = None,
        echo: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ):
        """
        Inicializa o gerenciador de sessões.
        
        Args:
            db_type: Tipo do banco ("tdax", "automations" ou None para env)
            database_url: URL de conexão (sobrescreve db_type)
            echo: Se True, mostra SQL queries no console
            pool_size: Tamanho do pool de conexões
            max_overflow: Conexões extras permitidas
        """
        # Se não forneceu URL, usa settings baseado em db_type
        if database_url is None:
            if db_type == "tdax":
                database_url = settings.database_url_tdax
            elif db_type == "automations":
                database_url = settings.database_url_automation
            else:
                # None = usa DATABASE_URL genérico ou tdax como padrão
                database_url = settings.database_url
        
        self.db_type = db_type
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
    
    def get_session(self) -> Session:
        """Retorna uma nova sessão"""
        return self.SessionLocal()
    
    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        """
        Context manager para sessão com auto-commit e rollback.
        
        Exemplo:
            manager = DatabaseSessionManager("tdax")
            with manager.session_scope() as session:
                clientes = session.query(Cliente).all()
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


# ==========================================
# INSTÂNCIAS GLOBAIS (lazy loading)
# ==========================================

_managers: dict[Optional[DatabaseType], DatabaseSessionManager] = {}


def get_manager(db_type: Optional[DatabaseType] = "tdax") -> DatabaseSessionManager:
    """
    Retorna ou cria um gerenciador para o banco especificado.
    
    Args:
        db_type: "tdax", "automations" ou None
    
    Returns:
        DatabaseSessionManager configurado
    
    Exemplo:
        manager = get_manager("tdax")
        with manager.session_scope() as session:
            ...
    """
    if db_type not in _managers:
        _managers[db_type] = DatabaseSessionManager(db_type=db_type)
    
    return _managers[db_type]


# ==========================================
# FUNÇÕES DE CONVENIÊNCIA
# ==========================================

@contextmanager
def get_session(
    db_type: Optional[DatabaseType] = "tdax"
) -> Generator[Session, None, None]:
    """
    Context manager para obter uma sessão.
    
    Args:
        db_type: "tdax", "automations" ou None
    
    Exemplo:
        # TDAX
        with get_session("tdax") as session:
            clientes = session.query(Cliente).all()
        
        # Automations
        with get_session("automations") as session:
            jobs = session.query(Job).all()
        
        # Padrão (tdax)
        with get_session() as session:
            ...
    """
    manager = get_manager(db_type)
    with manager.session_scope() as session:
        yield session


# ==========================================
# ALIASES PARA COMPATIBILIDADE
# ==========================================

@contextmanager
def get_tdax_session() -> Generator[Session, None, None]:
    """Alias para get_session("tdax")"""
    with get_session("tdax") as session:
        yield session


@contextmanager
def get_automations_session() -> Generator[Session, None, None]:
    """Alias para get_session("automations")"""
    with get_session("automations") as session:
        yield session


def get_tdax_manager() -> DatabaseSessionManager:
    """Alias para get_manager("tdax")"""
    return get_manager("tdax")


def get_automations_manager() -> DatabaseSessionManager:
    """Alias para get_manager("automations")"""
    return get_manager("automations")


# ==========================================
# FASTAPI DEPENDENCIES
# ==========================================

def get_db_dependency(
    db_type: DatabaseType = "tdax"
) -> Generator[Session, None, None]:
    """
    Dependency genérico para FastAPI.
    
    Uso:
        from functools import partial
        
        # TDAX
        @app.get("/clientes")
        def get_clientes(db: Session = Depends(get_db_dependency)):
            return db.query(Cliente).all()
        
        # Automations
        get_automations_db = partial(get_db_dependency, db_type="automations")
        
        @app.get("/jobs")
        def get_jobs(db: Session = Depends(get_automations_db)):
            return db.query(Job).all()
    """
    manager = get_manager(db_type)
    session = manager.get_session()
    try:
        yield session
    finally:
        session.close()


# Aliases específicos
def get_tdax_db_dependency() -> Generator[Session, None, None]:
    """FastAPI dependency para TDAX"""
    return get_db_dependency(db_type="tdax")


def get_automations_db_dependency() -> Generator[Session, None, None]:
    """FastAPI dependency para Automations"""
    return get_db_dependency(db_type="automations")