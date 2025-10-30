"""
Repository para operações com sessões do governo usando CRUD genérico
"""
from typing import Optional, Dict, Any
from ..session import get_session
from ..repositories.crud import crud_factory
from ...database.models.tdax import SessionGov
from ...core.exceptions import DatabaseQueryError


# Instância CRUD
session_crud = crud_factory(SessionGov)


def save_session(site: str, cookies_data: Dict[str, Any], org_id: Optional[int] = None) -> SessionGov:
    """
    Salva uma nova sessão, deletando sessões anteriores para o mesmo site/org.

    Esta função implementa uma lógica de upsert onde só pode existir uma sessão
    por combinação site/org_id. Antes de criar a nova, deleta as antigas.

    Args:
        site: Nome do site
        cookies_data: Dados dos cookies
        org_id: ID da organização (opcional)

    Returns:
        SessionGov: Sessão criada

    Raises:
        DatabaseQueryError: Se houver erro na operação
    """
    try:
        with get_session("tdax") as session:
            # Primeiro, deleta sessões existentes para o mesmo site/org
            delete_session(site, org_id, session)

            # Cria nova sessão
            new_session = session_crud.create(session, {
                "site": site,
                "cookies_data": cookies_data,
                "org_id": org_id,
            })

            return new_session

    except DatabaseQueryError:
        raise
    except Exception as e:
        raise DatabaseQueryError(f"Erro ao salvar sessão: {e}")


def get_session(site: str, org_id: Optional[int] = None) -> Optional[SessionGov]:
    """
    Busca uma sessão por site e organização.

    Args:
        site: Nome do site
        org_id: ID da organização (opcional)

    Returns:
        SessionGov ou None se não encontrada
    """
    try:
        with get_session("tdax") as session:
            filters = {"site": site}
            if org_id is not None:
                filters["org_id"] = org_id

            sessions = session_crud.filter(session, limit=1, **filters)
            return sessions[0] if sessions else None

    except Exception as e:
        return None


def get_latest_session(site: str, org_id: Optional[int] = None) -> Optional[SessionGov]:
    """
    Busca a sessão mais recente por site e organização.
    Útil quando podem existir múltiplas sessões.

    Args:
        site: Nome do site
        org_id: ID da organização (opcional)

    Returns:
        SessionGov ou None se não encontrada
    """
    try:
        with get_session("tdax") as session:
            # Como usamos upsert, normalmente só existe uma sessão
            # Mas caso haja múltiplas, pegamos a mais recente
            return get_session(site, org_id)

    except Exception as e:
        return None


def delete_session(site: str, org_id: Optional[int] = None, session=None) -> bool:
    """
    Deleta sessões por site e organização.

    Args:
        site: Nome do site
        org_id: ID da organização (opcional)
        session: Sessão SQLAlchemy (opcional, se não fornecida, cria uma nova)

    Returns:
        bool: True se deletou alguma sessão, False caso contrário
    """
    try:
        should_close_session = session is None

        if session is None:
            session = get_session("tdax").__enter__()

        try:
            filters = {"site": site}
            if org_id is not None:
                filters["org_id"] = org_id

            # Conta quantas sessões serão deletadas
            count_before = session_crud.count(session, **filters)

            if count_before > 0:
                # Deleta todas as sessões que correspondem aos filtros
                sessions_to_delete = session_crud.filter(session, **filters)
                for sess in sessions_to_delete:
                    session.delete(sess)

                session.commit()
                return True
            else:
                return False

        finally:
            if should_close_session and session:
                session.__exit__(None, None, None)

    except Exception as e:
        if should_close_session and session:
            session.__exit__(type(e), e, e.__traceback__)
        return False


def update_session_cookies(site: str, cookies_data: Dict[str, Any], org_id: Optional[int] = None) -> Optional[SessionGov]:
    """
    Atualiza apenas os cookies de uma sessão existente.

    Args:
        site: Nome do site
        cookies_data: Novos dados dos cookies
        org_id: ID da organização (opcional)

    Returns:
        SessionGov atualizada ou None se não encontrada
    """
    try:
        with get_session("tdax") as session:
            existing_session = get_session(site, org_id)

            if existing_session:
                return session_crud.update(session, existing_session.id, {
                    "cookies_data": cookies_data
                })
            else:
                return None

    except DatabaseQueryError:
        raise
    except Exception as e:
        return None


def get_sessions_by_filters(**filters) -> list[SessionGov]:
    """
    Buscar sessões por filtros diversos.

    Args:
        **filters: Filtros de busca

    Returns:
        Lista de SessionGov
    """
    with get_session("tdax") as session:
        return session_crud.filter(session, **filters)


def count_sessions(site: Optional[str] = None, org_id: Optional[int] = None) -> int:
    """
    Conta sessões por filtros.

    Args:
        site: Nome do site (opcional)
        org_id: ID da organização (opcional)

    Returns:
        int: Número de sessões encontradas
    """
    filters = {}
    if site:
        filters["site"] = site
    if org_id is not None:
        filters["org_id"] = org_id

    with get_session("tdax") as session:
        return session_crud.count(session, **filters)