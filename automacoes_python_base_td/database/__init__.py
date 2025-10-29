"""
Módulo de Database - PostgreSQL e SQLAlchemy
"""
# PostgreSQL (psycopg2)
from .connection import (
    get_connection,
    execute_query,
    execute_many,
    fetch_all,
    fetch_one,
    DatabaseConnection,
)

# SQLAlchemy - Base e BaseModel
from .models.base import Base, BaseModel

# SQLAlchemy - Session Managers
from .session import (
    # Gerenciadores
    DatabaseSessionManager,
    TdaxSessionManager,
    AutomationsSessionManager,
    # Inicialização
    init_tdax_db,
    init_automations_db,
    init_all_databases,
    # Obter managers
    get_tdax_manager,
    get_automations_manager,
    # Sessões
    get_tdax_session,
    get_automations_session,
    # FastAPI Dependencies
    get_tdax_db_dependency,
    get_automations_db_dependency,
    # Compatibilidade (deprecated)
    init_db,
    get_db_manager,
    get_session,
    get_db_dependency,
)

# Repositories CRUD
from .repositories import CRUDBase, crud_factory

__all__ = [
    # PostgreSQL
    "get_connection",
    "execute_query",
    "execute_many",
    "fetch_all",
    "fetch_one",
    "DatabaseConnection",
    # SQLAlchemy - Base
    "Base",
    "BaseModel",
    # SQLAlchemy - Gerenciadores
    "DatabaseSessionManager",
    "TdaxSessionManager",
    "AutomationsSessionManager",
    # SQLAlchemy - Inicialização
    "init_tdax_db",
    "init_automations_db",
    "init_all_databases",
    # SQLAlchemy - Obter Managers
    "get_tdax_manager",
    "get_automations_manager",
    # SQLAlchemy - Sessões
    "get_tdax_session",
    "get_automations_session",
    # SQLAlchemy - FastAPI
    "get_tdax_db_dependency",
    "get_automations_db_dependency",
    # SQLAlchemy - Compatibilidade (deprecated)
    "init_db",
    "get_db_manager",
    "get_session",
    "get_db_dependency",
    # CRUD
    "CRUDBase",
    "crud_factory",
]

