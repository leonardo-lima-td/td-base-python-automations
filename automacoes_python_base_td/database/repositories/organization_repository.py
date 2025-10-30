"""
Repository para operações com organizações usando joins complexos
"""
from typing import Optional, Tuple
from ..session import get_session
from ..repositories.crud import crud_factory
from ...database.models.tdax import Organizacoes, Certificates, DctfRetificacao
from ...utils import write_file, create_dir, slugify
from ...core.exceptions import DatabaseQueryError
from loguru import logger


# Instâncias CRUD para operações simples
organizacoes_crud = crud_factory(Organizacoes)
certificates_crud = crud_factory(Certificates)
retificacao_crud = crud_factory(DctfRetificacao)


def get_organization_certificate(org_id: int) -> Tuple[Optional[str], Optional[str]]:
    """
    Busca informações do certificado da organização (apenas dados, não salva arquivo).

    Args:
        org_id: ID da organização

    Returns:
        Tuple[Optional[str], Optional[str]]: Nome do arquivo e senha do certificado

    Raises:
        DatabaseQueryError: Se houver erro na consulta
    """
    try:
        with get_session("tdax") as session:
            # Join complexo entre Organizacoes e Certificates
            result = session.query(Organizacoes).join(
                Certificates,
                Organizacoes.certificate_id == Certificates.id
            ).filter(
                Organizacoes.id == org_id
            ).first()

            if not result:
                logger.warning(f"Organização não encontrada com ID {org_id}")
                return None, None

            if not result.certificate:
                logger.warning(f"Certificado não encontrado para organização {org_id}")
                return None, None

            return result.certificate.file_name, result.certificate.password

    except Exception as e:
        logger.error(f"Erro ao buscar certificado da organização {org_id}: {e}")
        raise DatabaseQueryError(f"Erro ao buscar certificado da organização: {e}")


def get_organization_from_retificacao(retificacao_id: int) -> Optional[int]:
    """
    Busca ID da organização através do ID da retificação.

    Args:
        retificacao_id: ID da retificação

    Returns:
        ID da organização ou None se não encontrada

    Raises:
        DatabaseQueryError: Se houver erro na consulta
    """
    try:
        with get_session("tdax") as session:
            # Join complexo entre DctfRetificacao e Organizacoes
            result = session.query(DctfRetificacao).filter(
                DctfRetificacao.id == retificacao_id
            ).first()

            if not result:
                logger.warning(f"Retificação não encontrada com ID {retificacao_id}")
                return None

            return result.organizacao_id

    except Exception as e:
        logger.error(f"Erro ao buscar organização da retificação {retificacao_id}: {e}")
        raise DatabaseQueryError(f"Erro ao buscar organização da retificação: {e}")


def save_organization_certificate_file(org_id: int, cert_dir: str = "files") -> Tuple[Optional[str], Optional[str]]:
    """
    Busca e salva o arquivo de certificado da organização usando utils.

    Args:
        org_id: ID da organização
        cert_dir: Diretório onde salvar (relativo à raiz do projeto)

    Returns:
        Tuple[Optional[str], Optional[str]]: Caminho do arquivo salvo e senha

    Raises:
        DatabaseQueryError: Se houver erro na operação
    """
    try:
        with get_session("tdax") as session:
            # Join complexo para buscar organização com certificado
            result = session.query(Organizacoes).join(
                Certificates,
                Organizacoes.certificate_id == Certificates.id
            ).filter(
                Organizacoes.id == org_id
            ).first()

            if not result or not result.certificate:
                logger.warning(f"Certificado não encontrado para organização {org_id}")
                return None, None

            # Salva arquivo usando utils
            cert_path = _save_certificate_to_file(result.certificate, cert_dir)

            if cert_path:
                logger.info(f"Certificado salvo para organização {org_id}: {cert_path}")
                return cert_path, result.certificate.password
            else:
                return None, None

    except Exception as e:
        logger.error(f"Erro ao salvar certificado da organização {org_id}: {e}")
        raise DatabaseQueryError(f"Erro ao salvar certificado da organização: {e}")


def _save_certificate_to_file(certificate: Certificates, cert_dir: str) -> Optional[str]:
    """
    Salva arquivo de certificado usando utils padronizados.

    Args:
        certificate: Instância do certificado
        cert_dir: Diretório onde salvar

    Returns:
        Caminho do arquivo salvo ou None em caso de erro
    """
    try:
        # Garante que o diretório existe
        create_dir(cert_dir)

        # Monta nome do arquivo (slugify para evitar problemas)
        file_name = slugify(certificate.file_name)
        cert_path = f"{cert_dir}/{file_name}"

        # Salva o conteúdo do certificado (eval para bytes)
        cert_content = eval(certificate.description)
        success = write_file(cert_path, cert_content, mode='wb')

        if success:
            return cert_path
        else:
            logger.error(f"Falha ao salvar certificado: {cert_path}")
            return None

    except Exception as e:
        logger.error(f"Erro ao salvar arquivo de certificado: {e}")
        return None


def get_organization_by_id(org_id: int) -> Optional[Organizacoes]:
    """
    Busca organização por ID (operação simples via CRUD).

    Args:
        org_id: ID da organização

    Returns:
        Instância Organizacoes ou None
    """
    with get_session("tdax") as session:
        return organizacoes_crud.get(session, id=org_id)


def get_organizations_by_filters(**filters) -> list[Organizacoes]:
    """
    Buscar organizações por filtros diversos.

    Args:
        **filters: Filtros de busca

    Returns:
        Lista de Organizacoes
    """
    with get_session("tdax") as session:
        return organizacoes_crud.filter(session, **filters)


def get_certificate_organizations() -> list[tuple[Organizacoes, Certificates]]:
    """
    Busca organizações que têm certificados (join complexo).

    Returns:
        Lista de tuplas (Organizacao, Certificate)
    """
    try:
        with get_session("tdax") as session:
            results = session.query(Organizacoes).join(
                Certificates,
                Organizacoes.certificate_id == Certificates.id
            ).all()

            return [(org, org.certificate) for org in results if org.certificate]

    except Exception as e:
        logger.error(f"Erro ao buscar organizações com certificados: {e}")
        return []


# ==========================================
# FUNÇÕES DE COMPATIBILIDADE LEGADA
# ==========================================

def get_organizacao_by_id(org_id: int) -> Optional[Organizacoes]:
    """
    Função de compatibilidade legada.

    DEPRECATED: Use get_organization_by_id() ao invés desta.

    Args:
        org_id: ID da organização

    Returns:
        Instância Organizacoes ou None
    """
    logger.warning("get_organizacao_by_id() está deprecated. Use get_organization_by_id()")
    return get_organization_by_id(org_id)

