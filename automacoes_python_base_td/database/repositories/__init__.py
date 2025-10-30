"""
Repositories refatorados usando CRUD genérico e session adequada
"""
from .crud import CRUDBase, crud_factory

# Repositories refatorados
from .certificate_repository import (
    get_certificate,
    get_certificate_from_org_id,
    get_certificate_by_filters,
    get_certificate_info,
)
from .dctf_repository import (
    get_dctf_by_id,
    update_status_by_id,
    get_dctf_all_by_id,
)
from .empresa_repository import (
    check_cnpj_exists_return_id,
    get_empresa_by_cnpj,
    get_empresa_by_id,
)
from .get_path_dec import (
    get_path_aws_dec,
    get_dctf_download_by_filters,
)
from .privilegios_repository import (
    check_cnpj_exists,
    insert_privilegios,
    get_privilegios_by_cnpj,
    insert_or_update_privilegios,
)
from .sped_repository import (
    save_sped_retificado,
    get_sped_retificado_by_id,
    get_sped_retificado_by_filters,
)

# Legado (ainda não refatorado)
from .get_cookies import (
    get_info_cookies,
    get_latest_session,
    validate_session_validity,
    get_session_by_filters,
    is_session_valid,
)
from .organization_repository import (
    get_organizacao_by_id,  # Mantém compatibilidade
    get_organization_certificate,
    get_organization_from_retificacao,
    save_organization_certificate_file,
    get_organization_by_id,
    get_organizations_by_filters,
    get_certificate_organizations,
)
from .session_repository import (
    save_session,
    get_session,
    get_latest_session,
    delete_session,
    update_session_cookies,
    get_sessions_by_filters,
    count_sessions,
)


__all__ = [
    # CRUD Genérico
    'CRUDBase',
    'crud_factory',

    # Certificate Repository (refatorado)
    'get_certificate',
    'get_certificate_from_org_id',
    'get_certificate_by_filters',
    'get_certificate_info',

    # DCTF Repository (refatorado)
    'get_dctf_by_id',
    'update_status_by_id',
    'get_dctf_all_by_id',

    # Empresa Repository (refatorado)
    'check_cnpj_exists_return_id',
    'get_empresa_by_cnpj',
    'get_empresa_by_id',

    # Get Path DEC (refatorado)
    'get_path_aws_dec',
    'get_dctf_download_by_filters',

    # Privilégios Repository (refatorado)
    'check_cnpj_exists',
    'insert_privilegios',
    'get_privilegios_by_cnpj',
    'insert_or_update_privilegios',

    # SPED Repository (refatorado)
    'save_sped_retificado',
    'get_sped_retificado_by_id',
    'get_sped_retificado_by_filters',

    # Legado (não refatorado ainda)
    'get_info_cookies',
    'get_latest_session',
    'validate_session_validity',
    'get_session_by_filters',
    'is_session_valid',
    'get_organizacao_by_id',  # Compatibilidade legada
    'get_organization_certificate',
    'get_organization_from_retificacao',
    'save_organization_certificate_file',
    'get_organization_by_id',
    'get_organizations_by_filters',
    'get_certificate_organizations',
    'save_session',
    'get_session',
    'get_latest_session',
    'delete_session',
    'update_session_cookies',
    'get_sessions_by_filters',
    'count_sessions',
]