"""
Repository para operações com certificados usando utils
"""
from typing import Tuple, Optional
from pathlib import Path
from ..session import get_session
from ..repositories.crud import crud_factory
from ...database.models.tdax import Certificates, Organizacoes
from ...utils import write_file, create_dir, slugify
from ...core.exceptions import ModelNotFoundError


# Instância CRUD
certificates_crud = crud_factory(Certificates)


def _save_certificate_file(certificate: Certificates, cert_dir: str) -> Optional[str]:
    """
    Salva o arquivo de certificado usando utils

    Args:
        certificate: Instância do certificado
        cert_dir: Diretório onde salvar

    Returns:
        Caminho do arquivo salvo ou None em caso de erro
    """
    try:
        # Garante que o diretório existe
        cert_dir_path = Path(cert_dir)
        create_dir(str(cert_dir_path))

        # Monta nome do arquivo (slugify para evitar problemas)
        file_name = slugify(certificate.file_name)
        cert_path = cert_dir_path / file_name

        # Salva o conteúdo do certificado (eval para bytes)
        cert_content = eval(certificate.description)
        success = write_file(str(cert_path), cert_content, mode='wb')

        if success:
            return str(cert_path)
        else:
            return None

    except Exception as e:
        return None


def get_certificate(org_id: int, cert_dir: str = "files") -> Tuple[Optional[str], Optional[str]]:
    """
    Busca o certificado no banco por ID, salva como arquivo .pfx e retorna caminho e senha.

    Args:
        org_id: ID do certificado
        cert_dir: Diretório onde salvar (relativo à raiz do projeto)

    Returns:
        Tuple[caminho_do_arquivo, senha] ou (None, None)
    """
    try:
        with get_session("tdax") as session:
            certificate = certificates_crud.get(session, id=org_id)

            if certificate is None:
                return None, None

            # Salva o arquivo usando utils
            cert_path = _save_certificate_file(certificate, cert_dir)

            if cert_path:
                return cert_path, certificate.password
            else:
                return None, None

    except ModelNotFoundError:
        return None, None
    except Exception as e:
        return None, None


def get_certificate_from_org_id(org_id: int, cert_dir: str = "files") -> Tuple[Optional[str], Optional[str]]:
    """
    Busca o certificado no banco por organização, salva como arquivo .pfx e retorna caminho e senha.

    Args:
        org_id: ID da organização
        cert_dir: Diretório onde salvar (relativo à raiz do projeto)

    Returns:
        Tuple[caminho_do_arquivo, senha] ou (None, None)
    """
    try:
        with get_session("tdax") as session:
            # Busca organização com join no certificado
            result = session.query(Organizacoes).join(
                Certificates,
                Organizacoes.certificate_id == Certificates.id
            ).filter(Organizacoes.id == org_id).first()

            if not result or not result.certificate:
                return None, None

            # Salva o arquivo usando utils
            cert_path = _save_certificate_file(result.certificate, cert_dir)

            if cert_path:
                return cert_path, result.certificate.password
            else:
                return None, None

    except Exception as e:
        return None, None


def get_certificate_by_filters(cert_dir: str = "files", **filters) -> list[Certificates]:
    """
    Buscar certificados por filtros

    Args:
        cert_dir: Diretório onde salvar (não usado nesta função)
        **filters: Filtros de busca

    Returns:
        Lista de Certificates
    """
    with get_session("tdax") as session:
        return certificates_crud.filter(session, **filters)


def get_certificate_info(org_id: int) -> Optional[Certificates]:
    """
    Busca informações do certificado sem salvar arquivo

    Args:
        org_id: ID da organização

    Returns:
        Instância Certificates ou None
    """
    try:
        with get_session("tdax") as session:
            # Busca organização com join no certificado
            result = session.query(Organizacoes).join(
                Certificates,
                Organizacoes.certificate_id == Certificates.id
            ).filter(Organizacoes.id == org_id).first()

            return result.certificate if result else None

    except Exception as e:
        return None
