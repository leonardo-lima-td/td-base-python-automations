from sqlalchemy import Column, Integer, Text, TIMESTAMP, func, ForeignKey, Enum
from sqlalchemy.orm import relationship
from ..base import BaseModel
import enum

# Enum Python correspondente ao ENUM do banco
class StatusRetificacaoEnum(str, enum.Enum):
    retificando = "retificando"
    retificado = "retificado"
    erro = "erro"

class DctfRetificacao(BaseModel):
    __tablename__ = "dctf_retificacoes"

    # id = Column(Integer, primary_key=True)
    path_s3 = Column(Text)
    status = Column(
        Enum(StatusRetificacaoEnum, name="status_retificacao_enum"),
        default=StatusRetificacaoEnum.retificando,
        nullable=False
    )
    id_dctf_download_unit = Column(Integer, ForeignKey("dctf_download_unit.id"))
    error_message = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relacionamento com DctfDownloadUnit (cada retificação é de um mês específico)
    dctf_download_unit = relationship("DctfDownloadUnit", backref="retificacoes")
