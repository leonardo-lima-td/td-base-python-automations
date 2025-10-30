"""
Repository para operações com Privilégios usando CRUD genérico
"""
from typing import Optional
from ..session import get_session
from ..repositories.crud import crud_factory
from ...database.models.tdax import Privilegios
from ...core.exceptions import DatabaseQueryError


# Instância CRUD
privilegios_crud = crud_factory(Privilegios)


def check_cnpj_exists(cnpj: str) -> bool:
    """
    Verifica se o CNPJ existe na tabela

    Args:
        cnpj: CNPJ a verificar

    Returns:
        True se existe, False caso contrário
    """
    with get_session("tdax") as session:
        return privilegios_crud.count(session, cnpj=cnpj) > 0


def insert_privilegios(cnpj: str, json_file: str, empresa_id: int) -> Privilegios:
    """
    Insere novo registro de privilégios

    Args:
        cnpj: CNPJ da empresa
        json_file: Conteúdo do arquivo JSON
        empresa_id: ID da empresa

    Returns:
        Instância Privilegios criada
    """
    with get_session("tdax") as session:
        return privilegios_crud.create(session, {
            "cnpj": cnpj,
            "json_file": json_file,
            "empresa_id": empresa_id
        })


def get_privilegios_by_cnpj(cnpj: str) -> Optional[Privilegios]:
    """
    Busca privilégios por CNPJ

    Args:
        cnpj: CNPJ a buscar

    Returns:
        Instância Privilegios ou None
    """
    with get_session("tdax") as session:
        privilegios = privilegios_crud.filter(session, cnpj=cnpj, limit=1)
        return privilegios[0] if privilegios else None


def insert_or_update_privilegios(cnpj: str, json_file: str, empresa_id: int) -> Privilegios:
    """
    Insere novo registro ou atualiza se já existir

    Args:
        cnpj: CNPJ da empresa
        json_file: Conteúdo do arquivo JSON
        empresa_id: ID da empresa

    Returns:
        Instância Privilegios criada ou atualizada
    """
    try:
        with get_session("tdax") as session:
            # Usa upsert por CNPJ (campo único)
            return privilegios_crud.upsert(session,
                {"json_file": json_file, "empresa_id": empresa_id},
                cnpj=cnpj
            )
    except DatabaseQueryError:
        raise
