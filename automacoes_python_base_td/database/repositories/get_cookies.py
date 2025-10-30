"""
Repository para operações com cookies de sessão usando CRUD genérico
"""
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from ..session import get_session
from ..repositories.crud import crud_factory
from ...database.models.tdax import SessionGov
from ...core.exceptions import DatabaseQueryError


# Instância CRUD
session_crud = crud_factory(SessionGov)


def _get_current_time_brasilia() -> datetime:
    """
    Obtém a hora atual no timezone de Brasília.

    Returns:
        datetime: Hora atual em Brasília
    """
    brasilia_tz = ZoneInfo('America/Sao_Paulo')
    return datetime.now(brasilia_tz)


def _convert_to_brasilia_timezone(utc_datetime: datetime) -> datetime:
    """
    Converte datetime UTC para timezone de Brasília.

    Args:
        utc_datetime: Datetime em UTC

    Returns:
        datetime: Datetime convertido para Brasília
    """
    brasilia_tz = ZoneInfo('America/Sao_Paulo')
    return utc_datetime.replace(tzinfo=ZoneInfo('UTC')).astimezone(brasilia_tz)


def _get_validity_limit(current_time: datetime, minutes: int = 15) -> datetime:
    """
    Calcula o limite de validade (hora atual - X minutos).

    Args:
        current_time: Hora atual
        minutes: Minutos para subtrair

    Returns:
        datetime: Limite de validade
    """
    return current_time - timedelta(minutes=minutes)


def _validate_cookie_expiration(session_updated: datetime, validity_limit: datetime) -> bool:
    """
    Valida se os cookies estão dentro do prazo de validade.

    Args:
        session_updated: Quando a sessão foi atualizada
        validity_limit: Limite de validade

    Returns:
        bool: True se válido, False se expirado
    """
    return session_updated >= validity_limit


def get_latest_session(org_id: int, site: str) -> Optional[SessionGov]:
    """
    Busca a sessão mais recente para uma organização e site.

    Args:
        org_id: ID da organização
        site: Nome do site

    Returns:
        SessionGov ou None
    """
    try:
        with get_session("tdax") as session:
            return session_crud.filter(
                session,
                org_id=org_id,
                site=site,
                limit=1
            )[0] if session_crud.filter(session, org_id=org_id, site=site, limit=1) else None

    except DatabaseQueryError as e:
        return None


def validate_session_validity(session_updated_utc: datetime, validity_minutes: int = 15) -> tuple[bool, Optional[timedelta]]:
    """
    Valida se uma sessão está dentro do prazo de validade.

    Args:
        session_updated_utc: Data de atualização da sessão (UTC)
        validity_minutes: Minutos de validade

    Returns:
        tuple: (is_valid, time_difference)
    """
    try:
        current_brasilia = _get_current_time_brasilia()
        validity_limit = _get_validity_limit(current_brasilia, validity_minutes)

        session_updated_brasilia = _convert_to_brasilia_timezone(session_updated_utc)
        is_valid = _validate_cookie_expiration(session_updated_brasilia, validity_limit)

        time_difference = current_brasilia - session_updated_brasilia if not is_valid else None

        return is_valid, time_difference

    except Exception as e:
        return False, None


def get_info_cookies(org_id: int, site: str, validity_minutes: int = 15) -> Optional[Dict[str, Any]]:
    """
    Busca e valida cookies de sessão para uma organização e site.

    Args:
        org_id: ID da organização
        site: Nome do site
        validity_minutes: Minutos de validade dos cookies

    Returns:
        Dict com cookies ou None se inválido/não encontrado
    """
    try:
        # Busca a sessão mais recente
        latest_session = get_latest_session(org_id, site)

        if not latest_session:
            return None

        # Valida se está dentro do prazo
        is_valid, time_diff = validate_session_validity(
            latest_session.updated_at,
            validity_minutes
        )

        if not is_valid:
            return None

        return latest_session.cookies_data

    except Exception as e:
        return None


def get_session_by_filters(**filters) -> list[SessionGov]:
    """
    Buscar sessões por filtros diversos.

    Args:
        **filters: Filtros de busca

    Returns:
        Lista de SessionGov
    """
    with get_session("tdax") as session:
        return session_crud.filter(session, **filters)


def is_session_valid(org_id: int, site: str, validity_minutes: int = 15) -> bool:
    """
    Verifica se existe uma sessão válida (sem retornar os dados).

    Args:
        org_id: ID da organização
        site: Nome do site
        validity_minutes: Minutos de validade

    Returns:
        bool: True se existe sessão válida
    """
    cookies = get_info_cookies(org_id, site, validity_minutes)
    return cookies is not None
        