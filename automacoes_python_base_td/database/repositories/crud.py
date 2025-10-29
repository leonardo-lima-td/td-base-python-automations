"""
CRUD genérico para qualquer model SQLAlchemy (plug and play)
"""
from typing import TypeVar, Generic, Type, Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models.base import Base
from ...core.exceptions import DatabaseQueryError, ModelNotFoundError


ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase(Generic[ModelType]):
    """
    CRUD genérico para qualquer model SQLAlchemy.
    Plug and play - funciona com qualquer model!
    
    IMPORTANTE: O model deve ter a coluna 'ativo' (Boolean) para soft delete.
    
    Exemplo:
        # Criar CRUD para o model User
        user_crud = CRUDBase(User)
        
        # CREATE
        user = user_crud.create(session, {"name": "João", "email": "joao@example.com"})
        
        # READ (por padrão, só retorna ativos)
        user = user_crud.get(session, id=1)
        users = user_crud.get_all(session)
        users = user_crud.filter(session, name="João")
        
        # READ (incluindo inativos)
        user = user_crud.get(session, id=1, include_inactive=True)
        users = user_crud.get_all(session, include_inactive=True)
        
        # UPDATE
        updated_user = user_crud.update(session, id=1, data={"name": "João Silva"})
        
        # DELETE (soft delete - marca ativo=False)
        user_crud.delete(session, id=1)
        
        # DELETE (hard delete - remove fisicamente)
        user_crud.hard_delete(session, id=1)
    """
    
    def __init__(self, model: Type[ModelType]):
        """
        Inicializa o CRUD com o model.
        
        Args:
            model: Classe do model SQLAlchemy
        """
        self.model = model
    
    def get(self, session: Session, id: int, include_inactive: bool = False) -> Optional[ModelType]:
        """
        Busca um registro por ID.
        
        Args:
            session: Sessão SQLAlchemy
            id: ID do registro
            include_inactive: Se True, inclui registros inativos
        
        Returns:
            Instância do model ou None
        """
        query = session.query(self.model).filter(self.model.id == id)
        if not include_inactive and hasattr(self.model, 'ativo'):
            query = query.filter(self.model.ativo == True)
        return query.first()
    
    def get_all(
        self,
        session: Session,
        skip: int = 0,
        limit: int = 100,
        include_inactive: bool = False,
    ) -> List[ModelType]:
        """
        Busca todos os registros com paginação.
        
        Args:
            session: Sessão SQLAlchemy
            skip: Número de registros para pular
            limit: Número máximo de registros
            include_inactive: Se True, inclui registros inativos
        
        Returns:
            Lista de instâncias do model
        """
        query = session.query(self.model)
        if not include_inactive and hasattr(self.model, 'ativo'):
            query = query.filter(self.model.ativo == True)
        return query.offset(skip).limit(limit).all()
    
    def filter(
        self,
        session: Session,
        skip: int = 0,
        limit: int = 100,
        include_inactive: bool = False,
        **filters
    ) -> List[ModelType]:
        """
        Busca registros com filtros.
        
        Args:
            session: Sessão SQLAlchemy
            skip: Número de registros para pular
            limit: Número máximo de registros
            include_inactive: Se True, inclui registros inativos
            **filters: Filtros (ex: name="João", active=True)
        
        Returns:
            Lista de instâncias do model
        
        Exemplo:
            users = user_crud.filter(session, name="João", active=True)
        """
        query = session.query(self.model)
        if not include_inactive and hasattr(self.model, 'ativo'):
            query = query.filter(self.model.ativo == True)
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.offset(skip).limit(limit).all()
    
    def create(self, session: Session, data: Dict[str, Any]) -> ModelType:
        """
        Cria um novo registro.
        
        Args:
            session: Sessão SQLAlchemy
            data: Dicionário com os dados
        
        Returns:
            Instância do model criada
        
        Exemplo:
            user = user_crud.create(session, {"name": "João", "email": "joao@example.com"})
        """
        try:
            obj = self.model(**data)
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseQueryError(
                f"Erro ao criar {self.model.__name__}",
                details={"model": self.model.__name__, "data": data, "error": str(e)}
            ) from e
    
    def create_many(self, session: Session, data_list: List[Dict[str, Any]]) -> List[ModelType]:
        """
        Cria múltiplos registros.
        
        Args:
            session: Sessão SQLAlchemy
            data_list: Lista de dicionários com os dados
        
        Returns:
            Lista de instâncias do model criadas
        """
        try:
            objects = [self.model(**data) for data in data_list]
            session.add_all(objects)
            session.commit()
            for obj in objects:
                session.refresh(obj)
            return objects
        except SQLAlchemyError as e:
            session.rollback()
            raise e
    
    def update(
        self,
        session: Session,
        id: int,
        data: Dict[str, Any]
    ) -> Optional[ModelType]:
        """
        Atualiza um registro.
        
        Args:
            session: Sessão SQLAlchemy
            id: ID do registro
            data: Dicionário com os dados para atualizar
        
        Returns:
            Instância do model atualizada ou None
        
        Exemplo:
            user = user_crud.update(session, 1, {"name": "João Silva"})
        """
        try:
            obj = self.get(session, id)
            if not obj:
                raise ModelNotFoundError(self.model.__name__, id)
            
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            session.commit()
            session.refresh(obj)
            return obj
        except ModelNotFoundError:
            raise
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseQueryError(
                f"Erro ao atualizar {self.model.__name__}",
                details={"model": self.model.__name__, "id": id, "data": data, "error": str(e)}
            ) from e
    
    def delete(self, session: Session, id: int) -> bool:
        """
        Deleta logicamente um registro (marca ativo=False).
        
        Args:
            session: Sessão SQLAlchemy
            id: ID do registro
        
        Returns:
            True se deletado, False se não encontrado
        
        Exemplo:
            deleted = user_crud.delete(session, 1)
        """
        try:
            obj = self.get(session, id)
            if not obj:
                raise ModelNotFoundError(self.model.__name__, id)
            
            if not hasattr(obj, 'ativo'):
                raise DatabaseQueryError(
                    f"Model {self.model.__name__} não possui coluna 'ativo' para soft delete",
                    details={"model": self.model.__name__, "id": id}
                )
            
            obj.ativo = False
            session.commit()
            session.refresh(obj)
            return True
        except (ModelNotFoundError, DatabaseQueryError):
            raise
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseQueryError(
                f"Erro ao deletar {self.model.__name__}",
                details={"model": self.model.__name__, "id": id, "error": str(e)}
            ) from e
    
    def count(self, session: Session, include_inactive: bool = False, **filters) -> int:
        """
        Conta o número de registros.
        
        Args:
            session: Sessão SQLAlchemy
            include_inactive: Se True, inclui registros inativos
            **filters: Filtros opcionais
        
        Returns:
            Número de registros
        """
        query = session.query(self.model)
        if not include_inactive and hasattr(self.model, 'ativo'):
            query = query.filter(self.model.ativo == True)
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.count()
    
    def exists(self, session: Session, id: int, include_inactive: bool = False) -> bool:
        """
        Verifica se um registro existe.
        
        Args:
            session: Sessão SQLAlchemy
            id: ID do registro
            include_inactive: Se True, inclui registros inativos
        
        Returns:
            True se existe, False caso contrário
        """
        query = session.query(self.model).filter(self.model.id == id)
        if not include_inactive and hasattr(self.model, 'ativo'):
            query = query.filter(self.model.ativo == True)
        return query.first() is not None


def crud_factory(model: Type[ModelType]) -> CRUDBase[ModelType]:
    """
    Factory para criar instâncias de CRUD para qualquer model.
    
    Args:
        model: Classe do model SQLAlchemy
    
    Returns:
        Instância de CRUDBase configurada para o model
    
    Exemplo:
        from models import User, Product
        
        user_crud = crud_factory(User)
        product_crud = crud_factory(Product)
        
        with get_session() as session:
            user = user_crud.get(session, id=1)
            products = product_crud.get_all(session)
    """
    return CRUDBase(model)

