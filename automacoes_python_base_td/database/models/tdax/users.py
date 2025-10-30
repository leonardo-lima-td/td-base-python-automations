from sqlalchemy import Column, BigInteger, String, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship
from ..base import BaseModel


class Users(BaseModel):
    __tablename__ = "users"
    schema = "public"

    
    # id = Column(BigInteger, primary_key=True, autoincrement=True)
    password = Column(String(128), nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    is_superuser = Column(Boolean, nullable=False)
    username = Column(String(150), nullable=False, unique=True)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(254), nullable=False)
    is_staff = Column(Boolean, nullable=False)
    is_active = Column(Boolean, nullable=False)
    date_joined = Column(DateTime(timezone=True), nullable=False)
    default_organization_id = Column(BigInteger, ForeignKey('organizacoes.id', ondelete='SET NULL'), nullable=True)
    
    # Relacionamentos
    default_organization = relationship("Organizacoes", back_populates="users")
    certificates = relationship("Certificates", back_populates="responsible")
    