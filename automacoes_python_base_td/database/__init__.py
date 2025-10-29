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

# SQLAlchemy - Session Manager Unificado
from .session import (
    DatabaseType,
    DatabaseSessionManager,
    get_manager,
    get_session,
    # Aliases para compatibilidade
    get_tdax_session,
    get_automations_session,
    get_tdax_manager,
    get_automations_manager,
    # FastAPI Dependencies
    get_db_dependency,
    get_tdax_db_dependency,
    get_automations_db_dependency,
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
    # SQLAlchemy - Session Manager
    "DatabaseType",
    "DatabaseSessionManager",
    "get_manager",
    "get_session",
    # SQLAlchemy - Aliases (compatibilidade)
    "get_tdax_session",
    "get_automations_session",
    "get_tdax_manager",
    "get_automations_manager",
    # SQLAlchemy - FastAPI
    "get_db_dependency",
    "get_tdax_db_dependency",
    "get_automations_db_dependency",
    # CRUD
    "CRUDBase",
    "crud_factory",
]

