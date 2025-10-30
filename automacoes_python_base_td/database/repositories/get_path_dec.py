"""
Repository para buscar caminhos de arquivos DCTF
"""
from typing import Optional
from ..session import get_session
from ..repositories.crud import crud_factory
from ...database.models.tdax import DctfDownloadUnit


# Instância CRUD
dctf_download_crud = crud_factory(DctfDownloadUnit)


def get_path_aws_dec(id_download: int) -> Optional[DctfDownloadUnit]:
    """
    Busca o caminho do arquivo .dec no S3.

    Args:
        id_download: ID do registro na tabela dctf_download_unit

    Returns:
        Instância DctfDownloadUnit ou None
    """
    with get_session("tdax") as session:
        return dctf_download_crud.get(session, id=id_download)


def get_dctf_download_by_filters(**filters) -> list[DctfDownloadUnit]:
    """
    Buscar DCTF downloads por filtros

    Args:
        **filters: Filtros de busca

    Returns:
        Lista de DctfDownloadUnit
    """
    with get_session("tdax") as session:
        return dctf_download_crud.filter(session, **filters)
