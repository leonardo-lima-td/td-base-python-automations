"""
Base models para SQLAlchemy
"""
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base


# Base para os models
Base = declarative_base()


class BaseModel(Base):
    """
    Model base com campos comuns para todas as tabelas.
    Inclui: id, ativo, created_at, updated_at
    
    Exemplo:
        class User(BaseModel):
            __tablename__ = "users"
            
            name = Column(String(100))
            email = Column(String(100))
    """
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    ativo = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    def to_dict(self):
        """Converte o model para dicionário"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"

