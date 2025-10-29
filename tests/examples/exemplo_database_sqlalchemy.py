"""
Exemplo de uso do Database com SQLAlchemy
"""
from automacoes_python_base_td import (
    Base, BaseModel, init_db, get_session, CRUDBase, crud_factory, logger
)
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Definir um modelo
class User(BaseModel):
    __tablename__ = "users_example"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Inicializar o banco (cria as tabelas)
# init_db()  # Descomente para criar as tabelas

# Usar CRUD
logger.info("=== Exemplo de CRUD com SQLAlchemy ===")

# Criar instância de CRUD
user_crud = crud_factory(User)

# Exemplo de uso com session
with get_session() as session:
    # Criar usuário
    # new_user = user_crud.create(
    #     session,
    #     obj_in={"name": "João Silva", "email": "joao@example.com"}
    # )
    # logger.success(f"Usuário criado: {new_user.id}")
    
    # Buscar todos
    users = user_crud.get_multi(session, skip=0, limit=10)
    logger.info(f"Total de usuários: {len(users)}")
    
    # Buscar por ID
    # user = user_crud.get(session, id=1)
    # if user:
    #     logger.info(f"Usuário encontrado: {user.name}")
    
    # Atualizar
    # updated_user = user_crud.update(
    #     session,
    #     db_obj=user,
    #     obj_in={"name": "João da Silva"}
    # )
    # logger.success(f"Usuário atualizado: {updated_user.name}")
    
    # Deletar
    # user_crud.delete(session, id=1)
    # logger.success("Usuário deletado")

logger.info("Operações concluídas!")

