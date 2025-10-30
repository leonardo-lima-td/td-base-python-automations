"""
Repository para operações SPED usando CRUD genérico
"""
from typing import Union
from ..session import get_session
from ..repositories.crud import crud_factory
from ...database.models.tdax import SpedRetificado
from ...core.exceptions import ModelNotFoundError, DatabaseQueryError


# Instância CRUD
sped_crud = crud_factory(SpedRetificado)


def save_sped_retificado(sped_retificado_id: Union[str, int, None] = None, **campos) -> Union[SpedRetificado, bool]:
    """
    Função única para insert ou update na tabela speds_retificados.

    Args:
        sped_retificado_id: ID do registro (se None, faz INSERT, senão faz UPDATE)
        **campos: Campos e valores a serem salvos (ex: status_validacao="ERRO", traceback="...")

    Returns:
        SpedRetificado: Registro criado ou atualizado, ou False em caso de erro
    """
    try:
        with get_session("tdax") as session:
            if sped_retificado_id is not None:
                # UPDATE: usa o upsert do CRUD
                sped = sped_crud.upsert(session, campos, id=int(sped_retificado_id))
                return sped
            else:
                sped = sped_crud.create(session, campos)
                return sped

    except ModelNotFoundError:
        return False
    except DatabaseQueryError as e:
        return False
    except Exception as e:
        return False


def get_sped_retificado_by_id(sped_retificado_id: Union[str, int]) -> Union[SpedRetificado, None]:
    """
    Buscar SPED retificado por ID

    Args:
        sped_retificado_id: ID do registro

    Returns:
        SpedRetificado ou None
    """
    with get_session("tdax") as session:
        return sped_crud.get(session, id=int(sped_retificado_id))


def get_sped_retificado_by_filters(**filters) -> list[SpedRetificado]:
    """
    Buscar SPEDs retificados por filtros

    Args:
        **filters: Filtros de busca

    Returns:
        Lista de SpedRetificado
    """
    with get_session("tdax") as session:
        return sped_crud.filter(session, **filters)
