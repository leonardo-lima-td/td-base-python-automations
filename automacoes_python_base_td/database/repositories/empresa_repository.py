"""
Repository para operações com Empresas usando CRUD genérico
"""
from typing import Optional
from ..session import get_session
from ..repositories.crud import crud_factory
from ...database.models.tdax import Empresas


# Instância CRUD
empresa_crud = crud_factory(Empresas)


def check_cnpj_exists_return_id(cnpj: str) -> Optional[int]:
    """
    Verifica se o CNPJ existe na tabela e retorna o ID

    Args:
        cnpj: CNPJ da empresa

    Returns:
        ID da empresa ou None se não encontrado
    """
    with get_session("tdax") as session:
        empresas = empresa_crud.filter(session, cnpj=cnpj, limit=1)
        return empresas[0].id if empresas else None


def get_empresa_by_cnpj(cnpj: str) -> Optional[Empresas]:
    """
    Buscar empresa por CNPJ

    Args:
        cnpj: CNPJ da empresa

    Returns:
        Instância Empresas ou None
    """
    with get_session("tdax") as session:
        empresas = empresa_crud.filter(session, cnpj=cnpj, limit=1)
        return empresas[0] if empresas else None


def get_empresa_by_id(empresa_id: int) -> Optional[Empresas]:
    """
    Buscar empresa por ID

    Args:
        empresa_id: ID da empresa

    Returns:
        Instância Empresas ou None
    """
    with get_session("tdax") as session:
        return empresa_crud.get(session, id=empresa_id)