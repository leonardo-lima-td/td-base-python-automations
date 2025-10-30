"""
Repository para operações DCTF usando CRUD genérico
"""
from typing import Optional
from ..session import get_session
from ..repositories.crud import crud_factory
from ...database.models.tdax import DctfDownloadAll, DctfDownloadUnit, DctfRetificacao
from ...core.exceptions import ModelNotFoundError


# Instâncias CRUD
dctf_download_crud = crud_factory(DctfDownloadUnit)
dctf_all_crud = crud_factory(DctfDownloadAll)
dctf_retificacao_crud = crud_factory(DctfRetificacao)


def get_dctf_by_id(dctf_id: int) -> Optional[DctfDownloadUnit]:
    """
    Buscar DCTF por ID (unit - mês específico)

    Args:
        dctf_id: ID do registro na tabela dctf_download_unit

    Returns:
        Instância DctfDownloadUnit ou None
    """
    with get_session("tdax") as session:
        return dctf_download_crud.get(session, id=dctf_id)


def update_status_by_id(dctf_id: int, new_status: str) -> Optional[DctfRetificacao]:
    """
    Atualizar status por ID

    Args:
        dctf_id: ID do registro na tabela dctf_retificacao
        new_status: Novo status

    Returns:
        Instância DctfRetificacao atualizada ou None
    """
    with get_session("tdax") as session:
        return dctf_retificacao_crud.update(session, id=dctf_id, data={"status": new_status})


def get_dctf_all_by_id(dctf_id: int) -> Optional[DctfDownloadAll]:
    """
    Buscar DCTF All por ID

    Args:
        dctf_id: ID do registro na tabela dctf_download_all

    Returns:
        Instância DctfDownloadAll ou None
    """
    with get_session("tdax") as session:
        return dctf_all_crud.get(session, id=dctf_id)

