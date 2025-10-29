"""
Módulo de models do banco de dados.

Organizado por banco de dados:
- tdax: Models do banco TDAX
- automations: Models do banco de Automações

Para usar os models, importe diretamente dos submódulos:

    from automacoes_python_base_td.database.models.tdax import Cliente, Produto
    from automacoes_python_base_td.database.models.automations import AutomationJob
    
Ou importe tudo:

    from automacoes_python_base_td.database import models
    
    # Acessar
    models.tdax.Cliente
    models.automations.AutomationJob

================================================================================
COMO CRIAR MODELS
================================================================================

1. TDAX - Models do banco TDAX
   
   Crie arquivo em: database/models/tdax/cliente.py
   
   from sqlalchemy import Column, String, Boolean
   from ...base import BaseModel
   
   class Cliente(BaseModel):
       __tablename__ = "tdax_clientes"
       
       codigo = Column(String(20), unique=True, nullable=False)
       nome = Column(String(100), nullable=False)
       ativo = Column(Boolean, default=True)

   Importe em: database/models/tdax/__init__.py
   
   from .cliente import Cliente
   __all__ = ["Cliente"]

2. AUTOMATIONS - Models de Automações
   
   Crie arquivo em: database/models/automations/automation_job.py
   
   from sqlalchemy import Column, String, DateTime, Boolean
   from ...base import BaseModel
   
   class AutomationJob(BaseModel):
       __tablename__ = "automation_jobs"
       
       name = Column(String(100), nullable=False)
       status = Column(String(20), default="pending")
       last_run = Column(DateTime)
       active = Column(Boolean, default=True)

   Importe em: database/models/automations/__init__.py
   
   from .automation_job import AutomationJob
   __all__ = ["AutomationJob"]

================================================================================
USAR COM CRUD GENÉRICO
================================================================================

from automacoes_python_base_td import crud_factory, get_session
from automacoes_python_base_td.database.models.tdax import Cliente
from automacoes_python_base_td.database.models.automations import AutomationJob

# CRUD para cada model
cliente_crud = crud_factory(Cliente)
job_crud = crud_factory(AutomationJob)

# Usar
with get_session() as session:
    # TDAX
    cliente = cliente_crud.create(session, {
        "codigo": "CLI001",
        "nome": "João Silva"
    })
    
    # Automations
    job = job_crud.create(session, {
        "name": "Import Data",
        "status": "running"
    })
"""

# Submódulos disponíveis
from . import tdax
from . import automations
from .base import Base, BaseModel

__all__ = [
    "tdax",
    "automations",
    # SQLAlchemy - Base
    "Base",
    "BaseModel",
]
