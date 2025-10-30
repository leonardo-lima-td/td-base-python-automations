from sqlalchemy import Column, Integer, String, BigInteger, Text, TIMESTAMP, func, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..base import BaseModel
import enum

# Enum Python correspondente ao ENUM do banco
class StatusDownloadEnum(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    success = "success"
    failed = "failed"
    empty = "empty"


# Tabela PAI - representa toda a requisição de download (60 meses)
class DctfDownloadAll(BaseModel):
    __tablename__ = "dctf_download_all"

    # id = Column(Integer, primary_key=True)
    organization_cnpj = Column(String(18), nullable=False)
    procuracao_tax_id = Column(String(18))  # CNPJ da empresa (procuração)
    start_period = Column(String(7), nullable=False)  # YYYY-MM
    end_period = Column(String(7), nullable=False)    # YYYY-MM
    total_months = Column(Integer, nullable=False)
    months_completed = Column(Integer, default=0)
    procuracao_is_active = Column(Boolean, default=True)
    error_message = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamento com os meses individuais
    months = relationship("DctfDownloadUnit", back_populates="dctf_download_all", cascade="all, delete-orphan")


# Tabela FILHA - representa cada mês individual
class DctfDownloadUnit(BaseModel):
    __tablename__ = "dctf_download_unit"

    # id = Column(Integer, primary_key=True)
    dctf_download_all_id = Column(Integer, ForeignKey("dctf_download_all.id"), nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    status = Column(
        String(50),
        default="pending",
        nullable=False,
    )
    file_size_bytes = Column(BigInteger)
    path_s3 = Column(Text)
    error_message = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamento com a tabela pai
    dctf_download_all = relationship("DctfDownloadAll", back_populates="months")
